"""
AcadAI – Viva Practice tab
Interactive oral-exam simulation with follow-up questions and scoring.
"""

import streamlit as st

from ui.components import (
    render_hero, section_header, chat_message,
    subject_badge, banner, empty_state,
)


def render_viva_tab() -> None:
    render_hero(
        title="Viva Practice",
        subtitle="Simulate an oral examination. Answer questions, get instant feedback and a score.",
        badge="Oral Exam Mode",
    )

    # ── Subject selector ───────────────────────────────────────────────────────
    from config import SUBJECT_KEYWORDS
    subjects = ["Auto-detect"] + sorted(SUBJECT_KEYWORDS.keys())

    col_sub, col_diff = st.columns(2)
    with col_sub:
        subject = st.selectbox("Subject", subjects, key="viva_subject")
    with col_diff:
        difficulty = st.selectbox(
            "Difficulty", ["Easy", "Medium", "Hard", "Mixed"], key="viva_diff"
        )

    if st.button("🎤 Start new viva session", key="viva_start"):
        st.session_state["viva_history"] = []
        st.session_state["viva_active"]  = True
        st.session_state["viva_subject_sel"] = subject
        st.session_state["viva_diff_sel"]    = difficulty
        st.rerun()

    # ── Active session ─────────────────────────────────────────────────────────
    if not st.session_state.get("viva_active"):
        empty_state(
            "🎤",
            "No active viva session",
            "Choose a subject and press 'Start new viva session' above.",
        )
        return

    viva_hist = st.session_state.get("viva_history", [])
    sel_sub   = st.session_state.get("viva_subject_sel", "Auto-detect")

    if sel_sub != "Auto-detect":
        subject_badge(sel_sub)

    # Render previous turns
    for turn in viva_hist:
        chat_message("ai",   turn["question"])
        chat_message("user", turn["student_answer"])
        if turn.get("feedback"):
            st.markdown(
                f'<div class="card accent-top" style="font-size:0.88rem;line-height:1.6">'
                f'<strong style="color:var(--primary)">Feedback</strong><br>{turn["feedback"]}</div>',
                unsafe_allow_html=True,
            )

    # Ask next question
    section_header("❓", "Examiner's question")
    if st.button("Generate next question", key="viva_gen_q"):
        with st.spinner("Preparing question…"):
            try:
                from tools.quiz import generate_quiz
                topic = sel_sub if sel_sub != "Auto-detect" else ""
                qs = generate_quiz(
                    topic=topic,
                    num_questions=1,
                    difficulty=st.session_state.get("viva_diff_sel", "Medium"),
                    as_viva=True,
                )
                st.session_state["viva_current_q"] = qs[0] if qs else "Explain a concept from your notes."
            except Exception as e:
                banner(f"Could not generate question: {e}", kind="error")

    current_q = st.session_state.get("viva_current_q", "")
    if current_q:
        chat_message("ai", current_q)
        answer = st.text_area(
            "Your answer", placeholder="Type your answer here…",
            key="viva_ans", height=110
        )
        if st.button("Submit answer", key="viva_submit"):
            if answer.strip():
                with st.spinner("Evaluating…"):
                    try:
                        from tools.quiz import evaluate_quiz_answer
                        feedback = evaluate_quiz_answer(current_q, answer)
                        viva_hist.append({
                            "question":       current_q,
                            "student_answer": answer,
                            "feedback":       feedback,
                        })
                        st.session_state["viva_history"]    = viva_hist
                        st.session_state["viva_current_q"]  = ""
                        st.rerun()
                    except Exception as e:
                        banner(f"Evaluation error: {e}", kind="error")
            else:
                banner("Please type an answer before submitting.", kind="warning")

    if viva_hist and st.button("End session & see score", key="viva_end"):
        total  = len(viva_hist)
        scored = sum(1 for t in viva_hist if t.get("feedback", "").lower().startswith("correct"))
        pct    = int(scored / total * 100) if total else 0
        banner(f"Session complete — {scored}/{total} correct ({pct}%)", kind="success")
        st.session_state["viva_active"] = False