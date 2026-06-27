"""
AcadAI – Flashcard tool
Generates Q/A flashcards and parses the raw LLM output into structured dicts.
"""

import re
from typing import List, Dict, Tuple

from llm.mistral import call_llm
from utils import clean_text


def generate_flashcards(
    subject: str,
    topic: str = "",
    num: int = 10,
    evidence_rows: List[Dict] = None,
) -> str:
    """
    Ask Mistral to generate *num* Q/A flashcards.
    Returns the raw LLM text (or an offline fallback string).
    """
    evidence = ""
    if evidence_rows:
        evidence = "\n\n".join(
            f"[{r.get('doc_id')}] {r.get('evidence','')}" for r in evidence_rows[:10]
        )

    system = (
        "You are AcadAI's Flashcard Agent. Create concise exam flashcards. "
        "Return in Q/A format like:\n"
        "Q1. <question>\nA1. <answer>\n\nQ2. ...\nA2. ...\n"
        "Keep answers short and accurate."
    )
    label = f"{subject} — {topic}" if topic else subject
    prompt = f"Subject/Topic: {label}\nNumber of flashcards: {num}"
    if evidence:
        prompt += f"\nEvidence:\n{evidence}"

    out = call_llm(prompt, system)
    if out:
        return out

    # Offline fallback
    return "\n".join(
        f"Q{i}. What is an important point about {label}?\n"
        f"A{i}. Review the retrieved evidence and write the definition/example."
        for i in range(1, num + 1)
    )


def parse_flashcards_text(text: str) -> List[Dict]:
    """
    Parse raw Q/A flashcard text into a list of dicts with keys 'q' and 'a'.
    Supports the canonical Q1./A1. format and a line-based fallback.
    """
    text = text or ""
    pairs: List[Tuple[str, str]] = []

    pattern = re.compile(
        r"(?:^|\n)\s*(?:Q\s*\d+\.?|Question\s*\d+\.?|Q\.?)[\s:-]*(.*?)"
        r"\s*(?:\n|\s+)A\s*\d*\.?[\s:-]*(.*?)"
        r"(?=(?:\n\s*(?:Q\s*\d+\.?|Question\s*\d+\.?|Q\.?)[\s:-])|\Z)",
        flags=re.I | re.S,
    )
    for m in pattern.finditer(text):
        q = clean_text(m.group(1))
        a = clean_text(m.group(2))
        if q and a:
            pairs.append((q, a))

    if pairs:
        return [{"q": q, "a": a} for q, a in pairs[:25]]

    # Line-based fallback
    lines  = [l.strip() for l in text.split("\n") if l.strip()]
    result = []
    i = 0
    while i < len(lines) - 1:
        q_line = lines[i].lstrip("0123456789.) QqAa.:-").strip()
        a_line = lines[i + 1].lstrip("0123456789.) QqAa.:-").strip()
        if q_line and a_line:
            result.append({"q": q_line, "a": a_line})
        i += 2
    return result[:25]