"""
AcadAI – Tutor Agent
Generates the final pedagogical answer using retrieved evidence, the
reasoning plan, and the student's difficulty level.
"""

import time
from typing import List, Dict, Tuple

from models.chunk import AgentTrace
from llm.mistral import call_llm


def tutor_agent(
    query: str,
    difficulty: str,
    context_rows: List[Dict],
    web_rows: List[Dict],
    route: str,
    plan: Dict,
) -> Tuple[str, AgentTrace]:
    """
    Generate the answer using the given route's evidence.

    Parameters
    ----------
    query        : Original user question.
    difficulty   : 'beginner' | 'intermediate' | 'advanced'
    context_rows : Retrieved DB/FAISS chunks (RAG route).
    web_rows     : Web-search results (Web Search route).
    route        : 'RAG' | 'Web Search' | 'Direct LLM'
    plan         : Output from reasoning_agent.

    Returns
    -------
    (answer_text, AgentTrace)
    """
    t0 = time.time()

    if route == "RAG":
        context_rows = context_rows[:3]

        evidence = "\n\n".join(
            f"[{r['doc_id']}] {r['evidence'][:220]}"
            for r in context_rows
        )
    elif route == "Web Search":
        evidence = "\n\n".join(
            f"[{r['doc_id']}] {r['title']}. {r['snippet']}" for r in web_rows
        )
    else:
        evidence = "Use your general knowledge."

    system = (
        "You are AcadAI's Tutor Agent — a pedagogically expert AI tutor. "
        "Generate a well-structured academic answer using ONLY the evidence provided. "
        "If evidence is weak or partially relevant, clearly say what is missing instead of guessing. "
        "Structure: (1) Concept explanation, (2) Step-by-step breakdown with worked examples, "
        "(3) Exam-oriented tips, (4) Explicit source citations. "
        "Adapt depth to the requested difficulty level."
    )
    concepts = ", ".join(plan.get("key_concepts", []))
    prompt = (
        f"Question: {query}\n\n"
        f"Difficulty: {difficulty}\n\n"
        f"Key Concepts:\n{concepts}\n\n"
        f"Retrieved Evidence:\n{evidence}\n\n"
        "Write a clear answer with:\n"
        "1. Definition\n"
        "2. Explanation\n"
        "3. Example (if applicable)\n"
        "4. Conclusion\n"
    )

    try:
        answer = call_llm(prompt, system)
    except Exception as e:
        print("\n========== MISTRAL ERROR ==========")
        print(type(e).__name__)
        print(e)
        print("===================================\n")
        answer = ""

        if hasattr(e, "response") and e.response is not None:
            try:
                print(e.response.text)
            except Exception:
                pass

        print("===================================\n")

    except Exception as e:
        print("\n========== MISTRAL ERROR ==========")
        print(type(e).__name__)
        print(e)
        print("===================================\n")

        answer = ""

        # ------------------------------------------------------------------
    # Graceful fallback when LLM is unavailable
    # ------------------------------------------------------------------
    if not answer:

        if route == "RAG" and context_rows:

            definition = context_rows[0]["evidence"]

            answer_parts = [
                f"# {query}\n",

                "## Definition\n",
                definition + "\n",

                "## Key Concepts\n"
            ]

            if concepts:
                for c in concepts.split(","):
                    answer_parts.append(f"- {c.strip()}")

            answer_parts.append("\n## Explanation\n")

            for r in context_rows:
                answer_parts.append(
                    f"- {r['evidence']}"
                )

            answer_parts.append("\n## Exam Tips\n")

            answer_parts.extend([
                "- Write the definition first.",
                "- Mention important concepts.",
                "- Add a neat example if applicable.",
                "- Draw a diagram wherever possible."
            ])

            answer_parts.append("\n## Sources\n")

            for r in context_rows:
                answer_parts.append(
                    f"- {r['source']} (Page {r['page']})"
                )

            answer = "\n".join(answer_parts)

        elif route == "Web Search" and web_rows:

            lines = [
                "# Web Search Results\n"
            ]

            for r in web_rows[:3]:
                lines.append(
                    f"- {r['title']}\n"
                    f"  {r['snippet']}\n"
                    f"  {r['url']}\n"
                )

            answer = "\n".join(lines)

        else:

            answer = (
                "I could not find sufficient information to answer this question.\n\n"
                "Try uploading more course PDFs or ask a more specific question."
            )

    trace = AgentTrace(
        agent="Tutor Agent",
        action="Generated pedagogical answer (step-by-step, examples, citations)",
        result=f"Route={route} | {len(context_rows or web_rows)} evidence chunks",
        latency=time.time() - t0,
    )
    return answer, trace


def refine_answer(
    query: str,
    answer: str,
    feedback: str,
    difficulty: str,
) -> str:
    """
    Refine *answer* based on Critic Agent feedback.
    Returns the original answer with an appended note when the API is unavailable.
    """
    system = (
        "You are AcadAI's Tutor Agent in a refinement pass. "
        "Improve the answer based on the Critic Agent's feedback. "
        "Keep all correct content; address only the stated weaknesses."
    )
    refined = call_llm(
        f"Original answer:\n{answer}\n\nCritic feedback:\n{feedback}\n\n"
        f"Query: {query}\nDifficulty: {difficulty}",
        system,
    )
    return refined if refined else answer + f"\n\n_Refinement note: {feedback}_"