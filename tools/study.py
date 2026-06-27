"""
AcadAI – Study tools
Revision notes and exam question generators.
"""

from typing import List, Dict

from llm.mistral import call_llm


def _profile_summary() -> str:
    try:
        import streamlit as st
        profile = st.session_state.get("student_profile", {})
        weak    = st.session_state.get("weak_topics", {})
    except Exception:
        profile, weak = {}, {}
    weak_sorted = sorted(weak.items(), key=lambda x: x[1], reverse=True)[:6]
    weak_text   = ", ".join(f"{k} ({v})" for k, v in weak_sorted) or "None tracked yet"
    return (
        f"Level: {profile.get('preferred_level','intermediate')} | "
        f"Goal: {profile.get('goal','exam preparation')} | "
        f"Weak topics: {weak_text}"
    )


def generate_revision_notes(
    subject: str,
    topic: str = "",
    depth: str = "Standard",
    evidence_rows: List[Dict] = None,
) -> str:
    """
    Generate high-yield revision notes for *subject* / *topic*.

    Parameters
    ----------
    depth : 'Quick overview' | 'Standard' | 'Comprehensive'
    """
    evidence = ""
    if evidence_rows:
        evidence = "\n\n".join(
            f"[{r.get('doc_id')}] {r.get('evidence','')}" for r in evidence_rows[:12]
        )

    system = (
        "You are AcadAI's Exam Revision Agent. Create high-yield B.Tech revision material. "
        "Use only the evidence when possible. "
        "Include: key definitions, formulas, important points, and likely exam questions."
    )
    label  = f"{subject} — {topic}" if topic else subject
    prompt = (
        f"Topic: {label}\n"
        f"Depth: {depth}\n"
        f"Student profile: {_profile_summary()}"
    )
    if evidence:
        prompt += f"\nEvidence:\n{evidence}"

    out = call_llm(prompt, system)
    if out:
        return out

    return (
        f"**{depth} notes for {label}**\n\n"
        "- Key definitions\n"
        "- Important formulas and rules\n"
        "- Common exam questions\n"
        "- Practice examples\n\n"
        "_Add your MISTRAL_API_KEY for AI-generated notes._"
    )


def generate_exam_questions(
    subject: str,
    topic: str = "",
    num: int = 8,
    marks: str = "Mixed",
    evidence_rows: List[Dict] = None,
) -> str:
    """
    Generate likely B.Tech exam questions grouped by marks.

    Parameters
    ----------
    marks : '2' | '5' | '10' | 'Mixed'
    """
    evidence = ""
    if evidence_rows:
        evidence = "\n\n".join(
            f"[{r.get('doc_id')}] {r.get('evidence','')}" for r in evidence_rows[:10]
        )

    system = (
        "You are AcadAI's PYQ/Exam Question Agent. "
        "Generate likely B.Tech exam questions. "
        "Group them as: 2-mark, 5-mark, 10-mark, and viva questions."
    )
    label  = f"{subject} — {topic}" if topic else subject
    prompt = f"Topic: {label}\nNumber of questions: {num}\nMarks per question: {marks}"
    if evidence:
        prompt += f"\nEvidence:\n{evidence}"

    out = call_llm(prompt, system)
    if out:
        return out

    return (
        f"**Likely questions for {label}:**\n\n"
        "2-mark: Define key terms.\n"
        "5-mark: Explain with a worked example.\n"
        "10-mark: Discuss the complete concept with diagrams / steps.\n"
        "Viva: Be ready to justify your answers.\n\n"
        "_Add your MISTRAL_API_KEY for AI-generated questions._"
    )