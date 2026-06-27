"""
AcadAI – Memory tab
View conversation history, weak topics, saved flashcards, and session stats.
"""

import streamlit as st

from ui.components import (
    render_hero, section_header, metric_card,
    render_flashcards, banner, empty_state,
)


def render_memory_tab() -> None:
    render_hero(
        title="Memory",
        subtitle="Review your study session: conversations, weak topics, and saved flashcards.",
        badge="Session History",
    )

    history   = st.session_state.get("history", [])
    attempts  = st.session_state.get("quiz_attempts", [])
    saved_fc  = st.session_state.get("saved_flashcards", [])
    weak      = st.session_state.get("weak_topics", {})

    # ── Stats row ──────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Questions asked", str(len(history)), accent="primary")
    with col2:
        metric_card("Quizzes taken", str(len(attempts)), accent="amber")
    with col3:
        avg = (
            int(sum(a["score"] / a["total"] * 100 for a in attempts) / len(attempts))
            if attempts else 0
        )
        metric_card("Avg quiz score", f"{avg}%", accent="green" if avg >= 70 else "red")
    with col4:
        metric_card("Saved flashcards", str(len(saved_fc)), accent="primary")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Conversation history ───────────────────────────────────────────────────
    section_header("💬", "Conversation history")
    if history:
        for i, turn in enumerate(reversed(history), 1):
            with st.expander(f"Turn {len(history) - i + 1}: {turn.get('question','')[:70]}…"):
                st.markdown(
                    f'<div class="chat-user">{turn.get("question","")}</div>'
                    f'<div class="chat-ai"  >{turn.get("answer","")}</div>',
                    unsafe_allow_html=True,
                )
    else:
        empty_state("💬", "No conversations yet", "Ask a question in the Ask tab first.")

    # ── Weak topics ────────────────────────────────────────────────────────────
    if weak:
        section_header("⚠️", "Weak topics")
        for topic, count in sorted(weak.items(), key=lambda x: -x[1]):
            st.markdown(
                f'<div class="card" style="display:flex;justify-content:space-between;'
                f'align-items:center;padding:12px 18px;margin-bottom:6px">'
                f'<span style="font-size:0.9rem">{topic}</span>'
                f'<span class="subject-badge">{count}×</span></div>',
                unsafe_allow_html=True,
            )

    # ── Saved flashcards ───────────────────────────────────────────────────────
    section_header("🃏", f"Saved flashcards ({len(saved_fc)})")
    if saved_fc:
        render_flashcards(saved_fc)
        if st.button("🗑️ Clear saved flashcards", key="mem_clear_fc"):
            st.session_state["saved_flashcards"] = []
            banner("Flashcards cleared.", kind="info")
            st.rerun()
    else:
        empty_state("🃏", "No saved flashcards", "Generate flashcards in Study Tools and save them here.")

    # ── Quiz history ───────────────────────────────────────────────────────────
    if attempts:
        section_header("📊", "Quiz history")
        for a in reversed(attempts):
            pct   = int(a["score"] / a["total"] * 100) if a["total"] else 0
            color = "var(--green)" if pct >= 70 else "var(--accent)" if pct >= 50 else "var(--red)"
            st.markdown(
                f'<div class="card" style="display:flex;justify-content:space-between;'
                f'align-items:center;padding:12px 18px;margin-bottom:6px">'
                f'<span style="font-weight:600">{a.get("subject","")}</span>'
                f'<span style="color:{color};font-weight:700">{a["score"]}/{a["total"]} ({pct}%)</span></div>',
                unsafe_allow_html=True,
            )

    # ── Clear session ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Clear entire session", key="mem_clear_all"):
        for key in ["history", "chat_history", "quiz_attempts", "weak_topics",
                    "saved_flashcards", "quiz_questions", "quiz_results",
                    "rn_result", "eq_result", "fc_cards", "roadmap_result"]:
            st.session_state.pop(key, None)
        banner("Session cleared.", kind="info")
        st.rerun()