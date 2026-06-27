"""
AcadAI – Study Tools tab
Flashcards, revision notes, and exam questions in one place.
"""

import streamlit as st

from ui.components import (
    render_hero, section_header, render_flashcards, banner, empty_state,
)


def render_study_tools_tab() -> None:
    render_hero(
        title="Study Tools",
        subtitle="Generate flashcards, revision notes, and exam questions from your topic or PDFs.",
        badge="Study Suite",
    )

    tool = st.radio(
        "What would you like?",
        ["Flashcards", "Revision Notes", "Exam Questions"],
        horizontal=True,
        key="study_tool_sel",
    )

    from config import SUBJECT_KEYWORDS
    col_sub, col_topic = st.columns(2)
    with col_sub:
        subject = st.selectbox("Subject", sorted(SUBJECT_KEYWORDS.keys()), key="st_subject")
    with col_topic:
        topic = st.text_input("Specific topic (optional)", placeholder="e.g. Deadlocks", key="st_topic")

    # ── Flashcards ─────────────────────────────────────────────────────────────
    if tool == "Flashcards":
        num = st.slider("Number of cards", 5, 30, 10, key="st_fc_num")
        if st.button("⚡ Generate flashcards", key="st_fc_gen"):
            with st.spinner("Generating…"):
                try:
                    from tools.flashcards import generate_flashcards, parse_flashcards_text
                    raw   = generate_flashcards(subject=subject, topic=topic, num=num)
                    cards = parse_flashcards_text(raw)
                    st.session_state["fc_cards"] = cards
                except Exception as e:
                    banner(f"Error: {e}", kind="error")

        cards = st.session_state.get("fc_cards", [])
        if cards:
            section_header("🃏", f"{len(cards)} Flashcards")
            render_flashcards(cards)
            if st.button("💾 Save to collection", key="st_fc_save"):
                saved = st.session_state.get("saved_flashcards", [])
                saved.extend(cards)
                st.session_state["saved_flashcards"] = saved
                banner(f"Saved {len(cards)} cards to your collection.", kind="success")
        else:
            empty_state("🃏", "No flashcards yet", "Click 'Generate flashcards' to create some.")

    # ── Revision Notes ─────────────────────────────────────────────────────────
    elif tool == "Revision Notes":
        depth = st.selectbox("Depth", ["Quick overview", "Standard", "Comprehensive"], key="st_rn_depth")
        if st.button("📝 Generate notes", key="st_rn_gen"):
            with st.spinner("Writing notes…"):
                try:
                    from tools.study import generate_revision_notes
                    notes = generate_revision_notes(subject=subject, topic=topic, depth=depth)
                    st.session_state["rn_result"] = notes
                except Exception as e:
                    banner(f"Error: {e}", kind="error")

        notes = st.session_state.get("rn_result", "")
        if notes:
            section_header("📝", "Revision Notes")
            st.markdown(
                f'<div class="card accent-top" style="font-size:0.9rem;line-height:1.7;white-space:pre-wrap">{notes}</div>',
                unsafe_allow_html=True,
            )
        else:
            empty_state("📝", "No notes yet", "Select options and click 'Generate notes'.")

    # ── Exam Questions ─────────────────────────────────────────────────────────
    else:
        col_n, col_marks = st.columns(2)
        with col_n:
            num_q = st.slider("Number of questions", 3, 20, 8, key="st_eq_num")
        with col_marks:
            marks = st.selectbox("Marks per question", ["2", "5", "10", "Mixed"], key="st_eq_marks")

        if st.button("📄 Generate exam questions", key="st_eq_gen"):
            with st.spinner("Composing questions…"):
                try:
                    from tools.study import generate_exam_questions
                    qs = generate_exam_questions(
                        subject=subject, topic=topic, num=num_q, marks=marks
                    )
                    st.session_state["eq_result"] = qs
                except Exception as e:
                    banner(f"Error: {e}", kind="error")

        qs = st.session_state.get("eq_result", "")
        if qs:
            section_header("📄", "Exam Questions")
            for i, line in enumerate(qs.split("\n"), 1):
                line = line.strip()
                if not line:
                    continue
                clean = line.lstrip("0123456789.)- ").strip()
                st.markdown(
                    f'<div class="card" style="margin-bottom:8px;font-size:0.9rem">'
                    f'<span style="color:var(--primary);font-weight:600">Q{i}.</span> {clean}</div>',
                    unsafe_allow_html=True,
                )
        else:
            empty_state("📄", "No questions yet", "Click 'Generate exam questions' to start.")