"""
AcadAI – Main entry point.
Only st.set_page_config + tab wiring live here. All logic is in sub-modules.
"""

import streamlit as st

# ── Page config (must be first Streamlit call) ─────────────────────────────────
st.set_page_config(
    page_title="AcadAI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports ────────────────────────────────────────────────────────────────────
from ui.styles import inject_css
from ui.tabs.ask import render_ask_tab
from ui.tabs.viva import render_viva_tab
from ui.tabs.roadmap import render_roadmap_tab
from ui.tabs.study_tools import render_study_tools_tab
from ui.tabs.evaluation import render_evaluation_tab
from ui.tabs.memory import render_memory_tab

# ── CSS ────────────────────────────────────────────────────────────────────────
inject_css()

# ── Session-state defaults ─────────────────────────────────────────────────────
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("history", [])
st.session_state.setdefault("student_profile", {})
st.session_state.setdefault("quiz_attempts", [])
st.session_state.setdefault("weak_topics", {})
st.session_state.setdefault("saved_flashcards", [])

# ── Tab layout ─────────────────────────────────────────────────────────────────
tab_ask, tab_viva, tab_roadmap, tab_study, tab_eval, tab_memory = st.tabs([
    "💬 Ask AcadAI",
    "🎤 Viva Practice",
    "🗺️ Learning Roadmap",
    "📚 Study Tools",
    "📊 Evaluation",
    "🧠 Memory",
])

with tab_ask:
    render_ask_tab()

with tab_viva:
    render_viva_tab()

with tab_roadmap:
    render_roadmap_tab()

with tab_study:
    render_study_tools_tab()

with tab_eval:
    render_evaluation_tab()

with tab_memory:
    render_memory_tab()