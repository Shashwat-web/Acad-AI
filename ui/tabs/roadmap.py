"""
AcadAI – Learning Roadmap tab
Generates a personalised step-by-step study plan for a chosen subject/topic.
"""

import streamlit as st

from ui.components import render_hero, section_header, roadmap_step, banner, empty_state


def render_roadmap_tab() -> None:
    render_hero(
        title="Learning Roadmap",
        subtitle="Get a step-by-step plan tailored to your subject, goal, and time budget.",
        badge="AI Study Planner",
    )

    col_sub, col_days = st.columns(2)
    with col_sub:
        from config import SUBJECT_KEYWORDS
        subjects = sorted(SUBJECT_KEYWORDS.keys())
        subject = st.selectbox("Subject", subjects, key="rm_subject")
    with col_days:
        days = st.number_input("Days available", min_value=1, max_value=90, value=7, key="rm_days")

    goal = st.text_input(
        "Learning goal (optional)",
        placeholder="e.g. Master subnetting numericals for the exam",
        key="rm_goal",
    )

    col_level, col_hrs = st.columns(2)
    with col_level:
        level = st.selectbox("Current level", ["Beginner", "Intermediate", "Advanced"], key="rm_level")
    with col_hrs:
        hours = st.number_input("Hours/day", min_value=1, max_value=12, value=3, key="rm_hours")

    if st.button("🗺️ Generate roadmap", key="rm_gen"):
        with st.spinner("Building your roadmap…"):
            try:
                from tools.roadmap import generate_learning_roadmap
                roadmap_text = generate_learning_roadmap(
                    subject=subject,
                    days=int(days),
                    goal=goal,
                    level=level,
                    hours_per_day=int(hours),
                )
                st.session_state["roadmap_result"] = roadmap_text
                st.session_state["roadmap_subject"] = subject
            except Exception as e:
                banner(f"Could not generate roadmap: {e}", kind="error")

    result = st.session_state.get("roadmap_result", "")
    if not result:
        empty_state(
            "🗺️",
            "No roadmap generated yet",
            "Fill in the form above and click 'Generate roadmap'.",
        )
        return

    section_header("📋", f"Your {st.session_state.get('roadmap_subject','')} Roadmap")

    # Parse lines into numbered steps; fall back to raw markdown
    lines = [l.strip() for l in result.split("\n") if l.strip()]
    step_num = 1
    for line in lines:
        # Strip leading markdown list markers if present
        clean = line.lstrip("-•*0123456789.) ").strip()
        if clean:
            roadmap_step(step_num, clean)
            step_num += 1

    if st.button("📋 Copy roadmap", key="rm_copy"):
        st.code(result, language="")