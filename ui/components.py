"""
AcadAI – Reusable UI components
All components use the dark-academic design tokens from styles.py.
"""

from __future__ import annotations
import streamlit as st


# ── Hero banner ────────────────────────────────────────────────────────────────

def render_hero(
    title: str,
    subtitle: str,
    badge: str | None = None,
) -> None:
    badge_html = f'<div class="badge">{badge}</div>' if badge else ""
    st.markdown(
        f"""
<div class="acadai-hero">
  {badge_html}
  <h1>{title}</h1>
  <p>{subtitle}</p>
</div>
""",
        unsafe_allow_html=True,
    )


# ── Section header ─────────────────────────────────────────────────────────────

def section_header(icon: str, title: str) -> None:
    st.markdown(
        f"""
<div class="section-header">
  <span class="icon">{icon}</span>
  <h3>{title}</h3>
  <div class="line"></div>
</div>
""",
        unsafe_allow_html=True,
    )


# ── Metric card ────────────────────────────────────────────────────────────────

def metric_card(label: str, value: str, delta: str | None = None, accent: str = "primary") -> None:
    delta_html = ""
    if delta:
        color = "#3DDC84" if delta.startswith("+") else "#FF5C6A"
        delta_html = f'<div style="color:{color};font-size:0.78rem;margin-top:4px">{delta}</div>'

    accent_colors = {
        "primary": "#6C63FF",
        "amber":   "#F5A623",
        "green":   "#3DDC84",
        "red":     "#FF5C6A",
    }
    top_color = accent_colors.get(accent, "#6C63FF")

    st.markdown(
        f"""
<div class="card" style="border-top:3px solid {top_color};padding:18px 20px">
  <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:6px">{label}</div>
  <div style="font-family:var(--display);font-size:1.7rem;font-weight:700;color:var(--text)">{value}</div>
  {delta_html}
</div>
""",
        unsafe_allow_html=True,
    )


# ── Source pills ───────────────────────────────────────────────────────────────

def source_pills(sources: list[str]) -> None:
    if not sources:
        return
    pills = "".join(
        f'<span class="source-pill">📄 {s}</span>' for s in sources
    )
    st.markdown(
        f'<div style="margin:10px 0 4px">{pills}</div>',
        unsafe_allow_html=True,
    )


# ── Subject badge ──────────────────────────────────────────────────────────────

def subject_badge(subject: str) -> None:
    st.markdown(
        f'<span class="subject-badge">{subject}</span>',
        unsafe_allow_html=True,
    )


# ── Chat message ───────────────────────────────────────────────────────────────

def chat_message(role: str, text: str) -> None:
    if role == "user":
        st.markdown(
            f'<div><div class="chat-label" style="text-align:right">You</div>'
            f'<div class="chat-user">{text}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div><div class="chat-label">AcadAI</div>'
            f'<div class="chat-ai">{text}</div></div>',
            unsafe_allow_html=True,
        )


# ── Flashcards ─────────────────────────────────────────────────────────────────

def render_flashcards(cards: list[dict]) -> None:
    """
    Render a list of flashcard dicts with keys 'q' and 'a'.
    Uses expander for the answer reveal.
    """
    for i, card in enumerate(cards, 1):
        st.markdown(
            f"""
<div class="flashcard">
  <div class="q">Q{i}. {card.get('q', '')}</div>
</div>
""",
            unsafe_allow_html=True,
        )
        with st.expander("Reveal answer"):
            st.markdown(
                f'<div style="color:var(--muted);font-size:0.88rem;line-height:1.6">{card.get("a","")}</div>',
                unsafe_allow_html=True,
            )


# ── Roadmap step ───────────────────────────────────────────────────────────────

def roadmap_step(number: int, text: str) -> None:
    st.markdown(
        f"""
<div class="roadmap-step">
  <div class="num">{number:02d}</div>
  <div class="body">{text}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ── Agent trace expander ───────────────────────────────────────────────────────

def render_agent_trace(traces: list) -> None:
    """Render AgentTrace objects inside a collapsible debug panel."""
    if not traces:
        return
    with st.expander("🔍 Agent trace", expanded=False):
        for t in traces:
            st.markdown(
                f"""
<div class="card" style="margin-bottom:8px;padding:12px 16px">
  <div style="display:flex;justify-content:space-between;margin-bottom:4px">
    <span style="font-family:var(--mono);font-size:0.75rem;color:var(--primary)">{t.agent}</span>
    <span style="font-size:0.72rem;color:var(--muted)">{t.latency:.2f}s</span>
  </div>
  <div style="font-size:0.78rem;color:var(--muted);margin-bottom:3px">{t.action}</div>
  <div style="font-size:0.85rem;color:var(--text)">{t.result}</div>
</div>
""",
                unsafe_allow_html=True,
            )


# ── Empty state ────────────────────────────────────────────────────────────────

def empty_state(icon: str, message: str, hint: str = "") -> None:
    hint_html = f'<p style="color:var(--muted);font-size:0.82rem;margin-top:6px">{hint}</p>' if hint else ""
    st.markdown(
        f"""
<div style="text-align:center;padding:48px 24px;color:var(--muted)">
  <div style="font-size:2.4rem;margin-bottom:14px">{icon}</div>
  <div style="font-size:0.95rem;font-weight:600;color:var(--text)">{message}</div>
  {hint_html}
</div>
""",
        unsafe_allow_html=True,
    )


# ── Info / warning / success banners ──────────────────────────────────────────

def banner(text: str, kind: str = "info") -> None:
    colors = {
        "info":    ("#6C63FF", "rgba(108,99,255,0.10)"),
        "success": ("#3DDC84", "rgba(61,220,132,0.10)"),
        "warning": ("#F5A623", "rgba(245,166,35,0.10)"),
        "error":   ("#FF5C6A", "rgba(255,92,106,0.10)"),
    }
    icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
    border, bg = colors.get(kind, colors["info"])
    icon = icons.get(kind, "ℹ️")
    st.markdown(
        f"""
<div style="background:{bg};border:1px solid {border};border-radius:8px;
            padding:12px 16px;margin:10px 0;font-size:0.88rem;color:var(--text)">
  {icon} {text}
</div>
""",
        unsafe_allow_html=True,
    )