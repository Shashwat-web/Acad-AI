"""
AcadAI – Evaluation tab
Take a quiz, see score, review weak topics.
"""

import streamlit as st

from ui.components import (
    render_hero, section_header, metric_card, banner, empty_state, subject_badge,
)


def render_evaluation_tab() -> None:
    render_hero(
        title="Evaluation",
        subtitle="Test your understanding with auto-graded quizzes and track your weak topics.",
        badge="Quiz & Analytics",
    )

    from config import SUBJECT_KEYWORDS
    col_sub, col_n, col_diff = st.columns(3)
    with col_sub:
        subject = st.selectbox("Subject", sorted(SUBJECT_KEYWORDS.keys()), key="ev_sub")
    with col_n:
        num_q = st.slider("Questions", 3, 20, 5, key="ev_num")
    with col_diff:
        diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Mixed"], key="ev_diff")

    if st.button("🚀 Start quiz", key="ev_start"):
        with st.spinner("Generating quiz…"):
            try:
                from tools.quiz import generate_quiz
                questions = generate_quiz(topic=subject, num_questions=num_q, difficulty=diff)
                st.session_state["quiz_questions"] = questions
                st.session_state["quiz_answers"]   = {}
                st.session_state["quiz_submitted"]  = False
                st.session_state["quiz_subject"]    = subject
            except Exception as e:
                banner(f"Could not generate quiz: {e}", kind="error")

    questions = st.session_state.get("quiz_questions", [])
    submitted = st.session_state.get("quiz_submitted", False)

    if not questions:
        empty_state("📊", "No quiz active", "Choose a subject and click 'Start quiz'.")
        return

    section_header("❓", f"{st.session_state.get('quiz_subject','')} Quiz")
    subject_badge(st.session_state.get("quiz_subject", ""))

    answers = st.session_state.get("quiz_answers", {})

    for i, q in enumerate(questions):
        q_text   = q.get("question", q) if isinstance(q, dict) else q
        options  = q.get("options", []) if isinstance(q, dict) else []
        st.markdown(
            f'<div class="card accent-top" style="margin-bottom:4px">'
            f'<span style="color:var(--primary);font-weight:700">Q{i+1}.</span> {q_text}</div>',
            unsafe_allow_html=True,
        )
        if options:
            ans = st.radio(
                f"q{i}", options,
                key=f"ev_q{i}",
                label_visibility="collapsed",
                disabled=submitted,
            )
            answers[i] = ans
        else:
            ans = st.text_input(
                f"Answer {i+1}", key=f"ev_qa{i}", disabled=submitted
            )
            answers[i] = ans

    st.session_state["quiz_answers"] = answers

    if not submitted and st.button("✅ Submit quiz", key="ev_submit"):
        with st.spinner("Grading…"):
            try:
                from tools.quiz import evaluate_quiz_answer
                results = []
                for i, q in enumerate(questions):
                    q_text = q.get("question", q) if isinstance(q, dict) else q
                    ans    = answers.get(i, "")
                    fb     = evaluate_quiz_answer(q_text, ans)
                    results.append(fb)
                st.session_state["quiz_results"]   = results
                st.session_state["quiz_submitted"]  = True

                correct = sum(1 for r in results if r.lower().startswith("correct"))
                attempt = {"subject": subject, "score": correct, "total": len(questions)}
                attempts = st.session_state.get("quiz_attempts", [])
                attempts.append(attempt)
                st.session_state["quiz_attempts"] = attempts
                st.rerun()
            except Exception as e:
                banner(f"Grading error: {e}", kind="error")

    if submitted:
        results = st.session_state.get("quiz_results", [])
        correct = sum(1 for r in results if r.lower().startswith("correct"))
        total   = len(questions)
        pct     = int(correct / total * 100) if total else 0

        st.markdown("<br>", unsafe_allow_html=True)
        section_header("📊", "Results")
        col1, col2, col3 = st.columns(3)
        with col1:
            metric_card("Score", f"{correct}/{total}", accent="primary")
        with col2:
            metric_card("Percentage", f"{pct}%",
                        accent="green" if pct >= 70 else "amber" if pct >= 50 else "red")
        with col3:
            metric_card("Wrong", f"{total - correct}", accent="red")

        section_header("📋", "Review")
        for i, (q, r) in enumerate(zip(questions, results)):
            q_text = q.get("question", q) if isinstance(q, dict) else q
            correct_ans = q.get("answer", "") if isinstance(q, dict) else ""
            is_ok  = r.lower().startswith("correct")
            color  = "var(--green)" if is_ok else "var(--red)"
            icon   = "✅" if is_ok else "❌"
            st.markdown(
                f'<div class="card" style="border-left:3px solid {color};margin-bottom:8px">'
                f'<div style="font-weight:600;font-size:0.88rem">{icon} Q{i+1}. {q_text}</div>'
                f'<div style="color:var(--muted);font-size:0.82rem;margin-top:6px">{r}</div>'
                + (f'<div style="color:{color};font-size:0.8rem;margin-top:4px">Answer: {correct_ans}</div>' if correct_ans else "")
                + '</div>',
                unsafe_allow_html=True,
            )