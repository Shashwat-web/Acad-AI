"""
AcadAI – LLM layer
Wraps the Mistral AI chat completions endpoint.
All other modules call call_llm(); nothing else talks to the API directly.
"""

import os
import requests

from utils import clean_text


def call_llm(prompt: str, system: str = "") -> str:
    """
    Call Mistral AI chat completions.
    Returns the response text or an empty string on failure.
    """

    mistral_key = os.getenv("MISTRAL_API_KEY", "")

    if not mistral_key:
        try:
            import streamlit as st
            mistral_key = st.secrets.get("MISTRAL_API_KEY", "")
        except Exception:
            pass

    if not mistral_key:
        return ""

    model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

    try:
        import streamlit as st
        model = st.secrets.get("MISTRAL_MODEL", model)
    except Exception:
        pass

    messages = []

    if system:
        messages.append(
            {
                "role": "system",
                "content": system,
            }
        )

    messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {mistral_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "temperature": 0.1,
                "messages": messages,
            },
            timeout=10,
        )

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    except Exception:
        return ""


def llm_query_expansion(query: str) -> str:
    """
    Optional Mistral-powered query expansion.
    Returns the original query if expansion fails.
    """
    system = (
        "Expand this academic search query for retrieval. "
        "Return only a compact keyword-rich query. "
        "Include synonyms and related CS terms."
    )

    expanded = call_llm(query, system)
    expanded = clean_text(expanded)

    if not expanded or len(expanded) > 500:
        return query

    return clean_text(query + " " + expanded)