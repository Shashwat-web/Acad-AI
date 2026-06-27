"""
AcadAI – Session memory
Manages conversation history, grounding scores, and weak-topic tracking.
All state lives in st.session_state so it persists for the browser session.
"""

import re
from datetime import datetime
from typing import List, Dict

from utils import clean_text, quote, tokenize, keyword_overlap


# ── Conversation turns ─────────────────────────────────────────────────────────

def build_memory_context(max_turns: int = 4) -> str:
    """
    Return a formatted string of the last *max_turns* conversation turns
    to pass as context to the LLM.
    """
    try:
        import streamlit as st
        history = st.session_state.get("chat_history", [])[-max_turns:]
    except Exception:
        return ""

    blocks = []
    for i, item in enumerate(history, 1):
        blocks.append(
            f"Turn {i}: Student asked: {item.get('question','')}\n"
            f"AcadAI answered: {quote(item.get('answer',''), 450)}\n"
            f"Subject: {item.get('subject','GENERAL')} | "
            f"Grounding: {item.get('grounding','—')}%"
        )
    return "\n\n".join(blocks)


def store_conversation_turn(
    query: str,
    answer: str,
    route: str = "RAG",
    db_rows: List[Dict] = None,
    grounding_score: float = 0.0,
) -> None:

    try:
        import streamlit as st
    except Exception:
        return

    subject = "GENERAL"

    if db_rows:
        subject = str(db_rows[0].get("subject", "GENERAL"))

    st.session_state.setdefault("chat_history", []).append({
        "question": query,
        "answer": answer,
        "route": route,
        "subject": subject,
        "grounding": grounding_score,
        "sources": [],
        "traces": [],
    })

    st.session_state.setdefault("history", []).append({
        "question": query,
        "answer": answer,
    })

    st.session_state["chat_history"] = st.session_state["chat_history"][-30:]
    st.session_state["history"] = st.session_state["history"][-30:]


    # Also store in the simpler 'history' list used by the Memory tab
    st.session_state.setdefault("history", []).append({
        "question": query,
        "answer":   answer,
    })
    st.session_state["history"]      = st.session_state["history"][-30:]


# ── Grounding ──────────────────────────────────────────────────────────────────

def _answer_sentences(answer: str) -> List[str]:
    cleaned = re.sub(r"\s+", " ", answer or "").strip()
    parts   = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", cleaned)
    return [p.strip() for p in parts if len(p.strip().split()) >= 5]


def calculate_grounding_report(answer: str, evidence_rows: List[Dict]) -> Dict:
    """
    Sentence-level grounding check: what fraction of the answer sentences
    are supported by the retrieved evidence?

    Returns
    -------
    dict with keys: score, supported, total, unsupported, status
    """
    evidence_text = clean_text(
        " ".join(str(r.get("text") or r.get("evidence") or "") for r in evidence_rows)
    )
    sents = _answer_sentences(answer)

    if not sents or not evidence_text:
        return {
            "score": 0.0, "supported": 0, "total": len(sents),
            "unsupported": sents[:5], "status": "No evidence",
        }

    supported, unsupported = 0, []
    for sent in sents:
        overlap      = keyword_overlap(sent, evidence_text)
        sent_terms   = [t for t in tokenize(sent) if len(t) > 3]
        hits         = sum(1 for t in set(sent_terms) if t in evidence_text.lower())
        support_ratio = hits / max(1, len(set(sent_terms)))
        if overlap >= 0.18 or support_ratio >= 0.28:
            supported += 1
        else:
            unsupported.append(sent)

    score  = round((supported / max(1, len(sents))) * 100, 1)
    status = (
        "Strongly grounded"   if score >= 75 else
        "Partially grounded"  if score >= 45 else
        "Weakly grounded"
    )
    return {
        "score":       score,
        "supported":   supported,
        "total":       len(sents),
        "unsupported": unsupported[:6],
        "status":      status,
    }


# ── Weak topic tracking ────────────────────────────────────────────────────────

def update_weak_topic(topic: str, amount: int = 1) -> None:
    topic = clean_text(topic or "General")[:80]
    try:
        import streamlit as st
        weak = st.session_state.setdefault("weak_topics", {})
        weak[topic] = int(weak.get(topic, 0)) + amount
    except Exception:
        pass


def adaptive_difficulty(default_level: str = "intermediate") -> str:
    """
    Infer a difficulty level from the last 5 quiz attempt scores.
    Falls back to *default_level* when there is insufficient data.
    """
    try:
        import streamlit as st
        attempts = st.session_state.get("quiz_attempts", [])[-5:]
    except Exception:
        return default_level

    scores = [a.get("score") for a in attempts if isinstance(a.get("score"), (int, float))]
    if len(scores) < 2:
        return default_level
    avg = sum(scores) / len(scores)
    if avg >= 8:
        return "advanced"
    if avg <= 5:
        return "beginner"
    return "intermediate"