"""
AcadAI – UI Styles
Dark-academic theme: deep navy canvas, indigo primary, amber accent, Inter + Sora typography.
"""

import streamlit as st


def inject_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root tokens ───────────────────────────────────────────── */
:root {
  --bg:          #0F1117;
  --surface:     #181C27;
  --surface2:    #1E2336;
  --border:      #2A2F45;
  --primary:     #6C63FF;
  --primary-dim: #3D3880;
  --accent:      #F5A623;
  --accent-dim:  #7A5210;
  --green:       #3DDC84;
  --red:         #FF5C6A;
  --text:        #E8EAF0;
  --muted:       #7B82A0;
  --display:     'Sora', sans-serif;
  --body:        'Inter', sans-serif;
  --mono:        'JetBrains Mono', monospace;
  --radius:      12px;
  --radius-sm:   8px;
  --shadow:      0 4px 24px rgba(0,0,0,0.45);
}

/* ── Global reset ──────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--body) !important;
}

[data-testid="stSidebar"] {
  background-color: var(--surface) !important;
  border-right: 1px solid var(--border);
}

/* ── Hide Streamlit chrome ─────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Tab strip ─────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 4px 6px;
  gap: 4px;
  border-bottom: none !important;
  box-shadow: var(--shadow);
}
[data-testid="stTabs"] [role="tab"] {
  font-family: var(--body);
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--muted) !important;
  background: transparent;
  border: none !important;
  border-radius: var(--radius-sm);
  padding: 8px 14px;
  transition: all 0.18s ease;
}
[data-testid="stTabs"] [role="tab"]:hover {
  color: var(--text) !important;
  background: var(--surface2);
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  color: var(--text) !important;
  background: linear-gradient(135deg, var(--primary-dim), #2D2B6B);
  box-shadow: 0 0 0 1px var(--primary);
}

/* ── Buttons ───────────────────────────────────────────────── */
[data-testid="stButton"] > button {
  background: linear-gradient(135deg, var(--primary), #8B83FF) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--body) !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
  padding: 10px 22px !important;
  transition: opacity 0.15s, transform 0.1s;
  cursor: pointer;
}
[data-testid="stButton"] > button:hover {
  opacity: 0.88;
  transform: translateY(-1px);
}
[data-testid="stButton"] > button:active { transform: translateY(0); }

/* Secondary / ghost buttons */
button[kind="secondary"] {
  background: transparent !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
}
button[kind="secondary"]:hover {
  border-color: var(--primary) !important;
  color: var(--primary) !important;
}

/* ── Inputs & text areas ───────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] select {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-family: var(--body) !important;
  font-size: 0.9rem !important;
  transition: border-color 0.15s;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px rgba(108,99,255,0.18) !important;
  outline: none !important;
}

/* ── Metric cards ──────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 22px;
}
[data-testid="stMetricLabel"] {
  color: var(--muted) !important;
  font-size: 0.75rem !important;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
[data-testid="stMetricValue"] {
  color: var(--text) !important;
  font-family: var(--display) !important;
  font-size: 1.9rem !important;
  font-weight: 700 !important;
}
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* ── Expanders ─────────────────────────────────────────────── */
[data-testid="stExpander"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  margin-bottom: 10px;
}
[data-testid="stExpander"] summary {
  font-family: var(--body) !important;
  font-weight: 600 !important;
  color: var(--text) !important;
}

/* ── Dividers ──────────────────────────────────────────────── */
hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 18px 0;
}

/* ── Progress bar ──────────────────────────────────────────── */
[data-testid="stProgress"] > div > div {
  background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
  border-radius: 99px;
}

/* ── Spinners & alerts ─────────────────────────────────────── */
[data-testid="stAlert"] {
  border-radius: var(--radius-sm) !important;
  font-family: var(--body) !important;
}

/* ── Custom component classes ──────────────────────────────── */

/* Hero banner */
.acadai-hero {
  background: linear-gradient(135deg, #13172B 0%, #1A1040 50%, #13172B 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 36px 40px 32px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
}
.acadai-hero::before {
  content: '';
  position: absolute;
  top: -60px; right: -80px;
  width: 280px; height: 280px;
  background: radial-gradient(circle, rgba(108,99,255,0.18) 0%, transparent 70%);
  pointer-events: none;
}
.acadai-hero h1 {
  font-family: var(--display) !important;
  font-size: 2rem !important;
  font-weight: 700 !important;
  color: var(--text) !important;
  margin: 0 0 6px !important;
}
.acadai-hero p {
  color: var(--muted);
  font-size: 0.95rem;
  margin: 0;
}
.acadai-hero .badge {
  display: inline-block;
  background: rgba(108,99,255,0.18);
  border: 1px solid var(--primary);
  color: #A09FFF;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border-radius: 99px;
  padding: 3px 10px;
  margin-bottom: 14px;
}

/* Section header */
.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 24px 0 14px;
}
.section-header .icon {
  font-size: 1.2rem;
  line-height: 1;
}
.section-header h3 {
  font-family: var(--display) !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  color: var(--text) !important;
  margin: 0 !important;
}
.section-header .line {
  flex: 1;
  height: 1px;
  background: var(--border);
}

/* Cards */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 22px;
  margin-bottom: 12px;
  transition: border-color 0.18s, box-shadow 0.18s;
}
.card:hover { border-color: var(--primary-dim); box-shadow: var(--shadow); }
.card.accent-top { border-top: 3px solid var(--primary); }
.card.accent-amber { border-top: 3px solid var(--accent); }
.card.accent-green { border-top: 3px solid var(--green); }

/* Source pill */
.source-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(108,99,255,0.12);
  border: 1px solid var(--primary-dim);
  color: #A09FFF;
  font-family: var(--mono);
  font-size: 0.7rem;
  border-radius: 99px;
  padding: 3px 10px;
  margin: 3px 3px 3px 0;
  box-shadow: 0 0 6px rgba(108,99,255,0.12);
}

/* Subject badge — glowing pill (signature element) */
.subject-badge {
  display: inline-block;
  background: rgba(245,166,35,0.12);
  border: 1px solid var(--accent-dim);
  color: var(--accent);
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border-radius: 99px;
  padding: 3px 10px;
  box-shadow: 0 0 8px rgba(245,166,35,0.2);
  margin-right: 6px;
}

/* Chat bubbles */
.chat-user {
  background: linear-gradient(135deg, var(--primary-dim), #2D2B6B);
  border: 1px solid var(--primary);
  border-radius: 14px 14px 4px 14px;
  padding: 12px 16px;
  margin: 10px 0 10px 20%;
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--text);
}
.chat-ai {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px 14px 14px 4px;
  padding: 14px 18px;
  margin: 10px 20% 10px 0;
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--text);
}
.chat-label {
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted);
  margin-bottom: 5px;
}

/* Quiz option */
.quiz-option {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  margin: 6px 0;
  cursor: pointer;
  font-size: 0.9rem;
  transition: border-color 0.15s, background 0.15s;
}
.quiz-option:hover { border-color: var(--primary); background: rgba(108,99,255,0.07); }
.quiz-option.correct { border-color: var(--green) !important; background: rgba(61,220,132,0.08) !important; }
.quiz-option.wrong   { border-color: var(--red)   !important; background: rgba(255,92,106,0.08) !important; }

/* Flashcard */
.flashcard {
  background: linear-gradient(135deg, var(--surface) 0%, var(--surface2) 100%);
  border: 1px solid var(--border);
  border-left: 4px solid var(--primary);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 10px;
}
.flashcard .q {
  font-family: var(--display);
  font-weight: 600;
  color: var(--text);
  font-size: 0.9rem;
  margin-bottom: 10px;
}
.flashcard .a {
  color: var(--muted);
  font-size: 0.88rem;
  line-height: 1.55;
  border-top: 1px solid var(--border);
  padding-top: 10px;
}

/* Roadmap step */
.roadmap-step {
  display: flex;
  gap: 16px;
  margin-bottom: 14px;
  align-items: flex-start;
}
.roadmap-step .num {
  min-width: 32px; height: 32px;
  background: var(--primary-dim);
  border: 1px solid var(--primary);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--display);
  font-weight: 700;
  font-size: 0.78rem;
  color: #A09FFF;
  flex-shrink: 0;
}
.roadmap-step .body {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  flex: 1;
  font-size: 0.88rem;
  line-height: 1.55;
}

/* Code block */
pre, code {
  font-family: var(--mono) !important;
  background: #0A0C14 !important;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 0.82rem !important;
  color: #CBD5E1 !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary-dim); }
</style>
""",
        unsafe_allow_html=True,
    )