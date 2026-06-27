"""
AcadAI – Critic Agent
Evaluates the tutor's answer on Relevance, Completeness, Accuracy, Clarity.
Returns a structured score dict and an optional refinement suggestion.
"""

import json
import re
import time
from typing import Tuple, Dict

from models.chunk import AgentTrace
from llm.mistral import call_llm
from utils import keyword_overlap


def critic_agent(query: str, answer: str) -> Tuple[Dict, AgentTrace]:
    """
    Score *answer* against *query* on four dimensions.

    Returns
    -------
    (scores, AgentTrace)
    scores keys: relevance, completeness, accuracy, clarity, overall (all 0-10),
                 satisfactory (bool), feedback (str)
    """
    t0 = time.time()

    system = (
        "You are AcadAI's Critic Agent. Evaluate strictly on four dimensions. "
        "Return ONLY valid JSON with keys: relevance (0-10), completeness (0-10), "
        "accuracy (0-10), clarity (0-10), overall (0-10), "
        "satisfactory (true if overall>=7 else false), "
        "feedback (improvement note if not satisfactory, else empty string). No markdown."
    )
    raw    = call_llm(f"Query: {query}\n\nAnswer:\n{answer[:1500]}", system)
    scores: Dict = {}

    if raw:
        try:
            scores = json.loads(re.sub(r"```json|```", "", raw).strip())
        except Exception:
            pass

    # Heuristic fallback
    if not scores:
        words      = len(answer.split())
        has_example = any(kw in answer.lower() for kw in ["example", "e.g.", "for instance", "such as"])
        has_cite    = "[" in answer and "]" in answer
        rel         = min(10.0, 5 + keyword_overlap(query, answer) * 10)
        comp        = min(10.0, 4 + words / 80)
        acc         = 7.5
        cla         = 7.0 + (1.0 if has_example else 0) + (0.5 if has_cite else 0)
        overall     = round((rel + comp + acc + cla) / 4, 1)
        scores = {
            "relevance":    round(rel, 1),
            "completeness": round(comp, 1),
            "accuracy":     round(acc, 1),
            "clarity":      round(cla, 1),
            "overall":      overall,
            "satisfactory": overall >= 7.0,
            "feedback":     "" if overall >= 7.0 else "Add more examples and explicit source citations.",
        }

    trace = AgentTrace(
        agent="Critic Agent",
        action="Evaluated Relevance, Completeness, Accuracy, Clarity",
        result=(
            f"Overall: {scores.get('overall','?')}/10 | "
            f"Satisfactory: {scores.get('satisfactory','?')}"
        ),
        latency=time.time() - t0,
    )
    return scores, trace


def compute_metrics(
    route: str,
    evidence_count: int,
    latency: float,
    scores: Dict,
) -> Dict:
    """Build the metrics dict shown in the Evaluation tab."""
    return {
        "Answer route":   route,
        "Relevance":      f"{scores.get('relevance','—')}/10",
        "Completeness":   f"{scores.get('completeness','—')}/10",
        "Accuracy":       f"{scores.get('accuracy','—')}/10",
        "Clarity":        f"{scores.get('clarity','—')}/10",
        "Overall quality": f"{scores.get('overall','—')}/10",
        "Evidence used":  evidence_count,
        "Needs review":   "No" if scores.get("satisfactory") else "Yes",
        "Response time":  f"{latency:.2f}s",
    }