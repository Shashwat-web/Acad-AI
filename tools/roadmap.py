"""
AcadAI – Learning Roadmap tool
Generates a personalised day-wise B.Tech study plan via Mistral.
"""

from typing import List, Dict

from llm.mistral import call_llm


def _profile_summary() -> str:
    """Build a compact student profile string from session state."""
    try:
        import streamlit as st
        profile = st.session_state.get("student_profile", {})
        weak    = st.session_state.get("weak_topics", {})
    except Exception:
        profile, weak = {}, {}

    weak_sorted = sorted(weak.items(), key=lambda x: x[1], reverse=True)[:6]
    weak_text   = ", ".join(f"{k} ({v})" for k, v in weak_sorted) or "None tracked yet"
    return (
        f"Name: {profile.get('name','Student')} | "
        f"Semester: {profile.get('semester','B.Tech')} | "
        f"Branch: {profile.get('branch','CSE')} | "
        f"Level: {profile.get('preferred_level','intermediate')} | "
        f"Goal: {profile.get('goal','exam preparation')} | "
        f"Weak topics: {weak_text}"
    )


def generate_learning_roadmap(
    subject: str,
    days: int = 7,
    goal: str = "",
    level: str = "Intermediate",
    hours_per_day: int = 3,
    evidence_rows: List[Dict] = None,
) -> str:
    """
    Generate a day-wise study roadmap.

    Returns the LLM output string, or a plain offline fallback.
    """
    evidence = ""
    if evidence_rows:
        evidence = "\n\n".join(
            f"[{r.get('doc_id')}] {r.get('evidence','')}" for r in evidence_rows[:10]
        )

    system = (
        "You are AcadAI's Learning Roadmap Agent. "
        "Create a practical day-wise B.Tech study roadmap. "
        "Include daily topics, practice tasks, revision slots, and a mini-test suggestion. "
        "Format each day as: Day N: <plan>"
    )
    prompt = (
        f"Student profile: {_profile_summary()}\n"
        f"Subject: {subject}\n"
        f"Goal: {goal or 'Exam preparation'}\n"
        f"Days available: {days}\n"
        f"Level: {level}\n"
        f"Hours per day: {hours_per_day}"
    )
    if evidence:
        prompt += f"\nEvidence:\n{evidence}"

    out = call_llm(prompt, system)
    if out:
        return out

    # Offline fallback
    return "\n".join(
        f"Day {i}: Study {subject} subtopic {i}. "
        f"Make notes, solve 5 questions, revise previous day's mistakes."
        for i in range(1, days + 1)
    )