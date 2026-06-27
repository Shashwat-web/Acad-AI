"""
AcadAI – Shared utilities
Small pure functions used across every layer of the app.
No Streamlit imports; no heavy dependencies.
"""

import re
from typing import List


def clean_text(text: str) -> str:
    """Collapse internal whitespace and strip leading/trailing whitespace."""
    return re.sub(r"\s+", " ", text or "").strip()


def tokenize(text: str) -> List[str]:
    """
    Lowercase word tokenizer.
    Returns only alphanumeric tokens (including underscores) so punctuation
    does not pollute keyword sets.
    """
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def quote(text: str, limit: int = 260) -> str:
    """
    Truncate *text* to at most *limit* characters, breaking on a word
    boundary and appending an ellipsis when truncation occurs.
    """
    text = clean_text(text)
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."


def keyword_overlap(query: str, text: str) -> float:
    """
    Fraction of non-trivial query terms (length > 2) that appear in *text*.
    Returns 0.0 when the query contains no qualifying terms.

    Example
    -------
    >>> keyword_overlap("what is deadlock", "deadlock process hold wait")
    0.5   # "what" and "is" are ≤2 chars; "deadlock" matches → 1/2
    """
    query_terms = {t for t in tokenize(query) if len(t) > 2}
    if not query_terms:
        return 0.0
    return len(query_terms & set(tokenize(text))) / len(query_terms)