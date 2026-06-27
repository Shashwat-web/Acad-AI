"""
AcadAI – Subject detection helpers
Infer academic subject from query text or chunk content.
"""

from typing import List

from config import SUBJECT_KEYWORDS, SUBJECT_QUERY_HINTS, SUBJECT_EXPANSIONS, ACADEMIC_SYNONYMS
from utils import clean_text, tokenize


def infer_subject(text: str, source: str = "") -> str:
    """
    Infer the broad academic subject from chunk text + source filename.
    Returns 'GENERAL' when no subject matches.
    """
    hay = f"{source} {text}".lower()
    best_subject, best_score = "GENERAL", 0
    for subject, kws in SUBJECT_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in hay)
        if score > best_score:
            best_subject, best_score = subject, score
    return best_subject if best_score > 0 else "GENERAL"


def detect_query_subjects(query: str) -> List[str]:
    """
    Return a list of academic subjects that match keywords in *query*.
    Subnetting / IP queries are always mapped to CN even if 'network' is absent.
    """
    q = query.lower()
    subjects = [
        subject for subject, kws in SUBJECT_QUERY_HINTS.items()
        if any(kw in q for kw in kws)
    ]
    if any(x in q for x in ["subnet", "subnetting", "cidr", "vlsm",
                              "subnet mask", "broadcast address"]):
        if "CN" not in subjects:
            subjects.insert(0, "CN")
    return subjects


def is_subnetting_query(query: str) -> bool:
    q = query.lower()
    return any(x in q for x in [
        "subnet", "subnetting", "cidr", "vlsm", "subnet mask", "broadcast address",
        "network address", "host bits", "hosts per subnet", "borrow bits",
        "prefix length", "class a", "class b", "class c", "ip addressing",
    ])


def expand_query(query: str) -> str:
    """
    Lightweight query expansion: academic acronyms + subject-specific terms.
    """
    terms = tokenize(query)
    extras = [ACADEMIC_SYNONYMS[t] for t in terms if t in ACADEMIC_SYNONYMS]
    q = query.lower()
    if "quality of service" in q:
        extras.append(ACADEMIC_SYNONYMS.get("qos", ""))
    for subject in detect_query_subjects(query):
        extras.append(SUBJECT_EXPANSIONS.get(subject, ""))
    return clean_text(query + " " + " ".join(extras))


def source_subject_boost(source: str, wanted_subjects: List[str]) -> float:
    """
    Return a small score boost (0..0.24) when the chunk's filename hints
    match the query's detected subject(s).
    """
    s = (source or "").lower()
    source_aliases = {
        "CN":     ["cn", "network", "computer network", "data communication", "communication"],
        "OS":     ["os", "operating", "operating system"],
        "DBMS":   ["dbms", "database", "sql"],
        "DSA":    ["dsa", "data structure", "algorithm"],
        "PYTHON": ["python"],
        "WEB":    ["web", "html", "css", "javascript"],
        "SE":     ["software engineering", "se", "sdlc"],
        "ML":     ["machine learning", "ml", "techniques"],
        "DWM":    ["warehouse", "mining", "dwm"],
        "DA":     ["analytics"],
        "HV":     ["human values", "ethics"],
    }
    score = sum(
        0.12
        for subj in wanted_subjects
        if any(alias in s for alias in source_aliases.get(subj, []))
    )
    return min(score, 0.24)