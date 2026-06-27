"""
AcadAI – Reasoning Agent
Analyses the query and returns a structured solution plan (JSON via Mistral).
Falls back to a heuristic plan when the API is unavailable.
"""

import json
import re
import time
from typing import Tuple, Dict

from models.chunk import AgentTrace
from llm.mistral import call_llm
from utils import tokenize


def reasoning_agent(query: str) -> Tuple[Dict, AgentTrace]:
    """
    Fast rule-based reasoning agent.
    Builds a reasoning plan without calling an LLM.
    """

    t0 = time.time()

    tokens = tokenize(query.lower())

    # ----------------------------
    # Difficulty estimation
    # ----------------------------
    if len(tokens) < 6:
        difficulty = "beginner"
    elif len(tokens) < 15:
        difficulty = "intermediate"
    else:
        difficulty = "advanced"

    # ----------------------------
    # Key concepts
    # ----------------------------
    stop_words = {
        "what", "is", "the", "a", "an", "of",
        "in", "to", "and", "for", "explain",
        "define", "with", "using", "how",
        "does", "do", "are"
    }

    concepts = []

    for word in tokens:
        if len(word) > 3 and word not in stop_words:
            if word not in concepts:
                concepts.append(word)

    concepts = concepts[:6]

    # ----------------------------
    # Solution Plan
    # ----------------------------
    plan = {
        "key_concepts": concepts,
        "solution_plan": [
            "Identify the main concept.",
            "Retrieve relevant academic material.",
            "Generate a structured explanation.",
            "Provide examples if applicable.",
            "Cite supporting course material."
        ],
        "tools_needed": [
            "FAISS Retriever",
            "Tutor Agent"
        ],
        "difficulty_estimate": difficulty,
    }

    trace = AgentTrace(
        agent="Reasoning Agent",
        action="Generated reasoning plan locally",
        result=f"{len(concepts)} concepts | Difficulty={difficulty}",
        latency=time.time() - t0,
    )

    return plan, trace