"""
AcadAI – Router Agent
Decides whether the query should go to RAG, Web Search, or Direct LLM.
"""

import time
from typing import Tuple

from models.chunk import AgentTrace


REALTIME_KW = ["today", "latest", "current", "2024", "2025", "recent", "news", "price"]
GENERAL_KW  = ["who is", "what year", "define ", "meaning of", "capital of", "how many", "convert "]


def router_agent(
    query: str,
    db_match: bool,
    use_web: bool = False,
) -> Tuple[str, AgentTrace]:
    """
    Route the query to one of: 'RAG', 'Web Search', 'Direct LLM'.

    Parameters
    ----------
    query    : Raw user question.
    db_match : Whether the retriever found sufficiently relevant chunks.
    use_web  : Whether the web-search fallback is enabled.

    Returns
    -------
    (route, AgentTrace)
    """
    t0    = time.time()
    q_low = query.lower()

    if any(p in q_low for p in REALTIME_KW) and use_web:
        route = "Web Search"
    elif db_match:
        route = "RAG"
    elif any(p in q_low for p in GENERAL_KW):
        route = "Direct LLM"
    elif use_web:
        route = "Web Search"
    else:
        route = "RAG"

    trace = AgentTrace(
        agent="Router Agent",
        action="Classified query intent → Direct LLM / Web Search / RAG",
        result=f"Route → {route}",
        latency=time.time() - t0,
    )
    return route, trace