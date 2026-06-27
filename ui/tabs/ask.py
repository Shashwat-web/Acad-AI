"""
AcadAI – Ask tab
Main Q&A interface: PDF upload, question input, answer + citations.
"""

import streamlit as st

from ui.components import (
    render_hero, section_header, chat_message,
    source_pills, subject_badge, render_agent_trace, empty_state, banner,
)


def render_ask_tab() -> None:
    render_hero(
        title="Ask AcadAI",
        subtitle="Ask anything from your notes or uploaded PDFs — get sourced, reasoned answers.",
        badge="Powered by Mistral + FAISS",
    )

    # ── Sidebar-style upload inside the tab ───────────────────────────────────
    with st.expander("📂 Upload study materials (PDF)", expanded=False):
        uploaded = st.file_uploader(
            "Drop your PDFs here",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )
        if uploaded:
            from ingestion.pdf_ingestion import read_pdf_uploads, build_faiss_store

            chunks, skipped = read_pdf_uploads(uploaded)
            ok, msg = build_faiss_store(chunks)

            if ok:
                banner(msg, kind="success")
            else:
                banner(msg, kind="error")

            st.session_state["uploaded_files"] = uploaded

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Chat history ───────────────────────────────────────────────────────────
    history = st.session_state.get("chat_history", [])
    if history:
        section_header("💬", "Conversation")
        for turn in history:
            chat_message(
                "user",
                turn.get("question") or turn.get("query", "")
            )
            chat_message("ai", turn.get("answer", ""))
            if turn.get("sources"):
                source_pills(turn["sources"])
            if turn.get("subject"):
                subject_badge(turn["subject"])
            if turn.get("traces"):
                render_agent_trace(turn["traces"])
    else:
        empty_state(
            "🎓",
            "No conversation yet",
            "Type your first question below to get started.",
        )

    # ── Question input ─────────────────────────────────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    section_header("✏️", "Ask a question")

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        query = st.text_input(
            "Question",
            placeholder="e.g. Explain subnetting with CIDR notation…",
            label_visibility="collapsed",
            key="ask_input",
        )
    with col_btn:
        ask = st.button("Ask →", use_container_width=True)

    col_k, col_mode = st.columns(2)
    with col_k:
        top_k = st.slider("Sources to retrieve", 3, 15, 8, key="ask_topk")
    with col_mode:
        mode = st.selectbox(
            "Answer style",
            ["Detailed", "Concise", "Bullet points", "Exam-ready"],
            key="ask_mode",
        )

    if ask and query.strip():
        with st.spinner("Thinking…"):
            try:

                from agents.router import router_agent
                from agents.reasoning import reasoning_agent
                from agents.tutor import tutor_agent
                from retrieval.hybrid import retrieve_faiss
                from memory.session import (
                    build_memory_context,
                    store_conversation_turn,
                )
                from retrieval.faiss_store import load_faiss_store
                from config import DEFAULT_FAISS_DIR

                traces = []

                # -------------------------------------------------
                # Load FAISS
                # -------------------------------------------------
                index, faiss_chunks, err = load_faiss_store(DEFAULT_FAISS_DIR)

                if index is None:
                    raise Exception(err)

                # -------------------------------------------------
                # Retrieval
                # -------------------------------------------------

                results, retrieval_meta = retrieve_faiss(
                    query=query,
                    index=index,
                    chunks=faiss_chunks,
                    top_k=top_k,
                    use_cross_encoder=False,
                )

                # -------------------------------------------------
                # Memory
                # -------------------------------------------------
                mem = build_memory_context(
                    st.session_state.get("history", [])
                )

                db_match = retrieval_meta.get("match", False)

                # -------------------------------------------------
                # Router Agent
                # -------------------------------------------------

                route, router_trace = router_agent(
                    query=query,
                    db_match=db_match,
                )


                traces.append(router_trace)

                # -------------------------------------------------
                # Reasoning Agent
                # -------------------------------------------------
                plan, reasoning_trace = reasoning_agent(query)

                traces.append(reasoning_trace)

                difficulty = plan.get(
                    "difficulty_estimate",
                    "intermediate",
                )

                # -------------------------------------------------
                # Tutor Agent
                # -------------------------------------------------


                answer, tutor_trace = tutor_agent(
                    query=query,
                    difficulty=difficulty,
                    context_rows=results,
                    web_rows=[],
                    route=route,
                    plan=plan,
                )


                if answer.startswith("**Answer ("):
                    banner(
                        "AI enhancement is temporarily unavailable. "
                        "Showing a grounded answer from your course materials.",
                        kind="warning",
                    )

                traces.append(tutor_trace)

                # -------------------------------------------------
                # Save Conversation
                # -------------------------------------------------
                sources = list({r["source"] for r in results[:5]})

                subject = st.session_state.get(
                    "detected_subject",
                    "",
                )

                store_conversation_turn(
                    query=query,
                    answer=answer,
                    route=route,
                    db_rows=results,
                    grounding_score=0.0,
                )
                chat_history = st.session_state.get("chat_history", [])

                if chat_history:
                    chat_history[-1]["sources"] = sources
                    chat_history[-1]["subject"] = subject
                    chat_history[-1]["traces"] = traces

                st.session_state["chat_history"] = chat_history

                st.rerun()

            except Exception as exc:
                banner(f"Error: {exc}", kind="error")
