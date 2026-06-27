"""
AcadAI – Quiz / Viva tool
Generates viva-style questions and evaluates student answers.
"""

from typing import List, Dict

from llm.mistral import call_llm


def generate_quiz(
    topic: str,
    difficulty: str = "Medium",
    num_questions: int = 5,
    evidence_rows: List[Dict] = None,
    as_viva: bool = False,
) -> List[str]:
    """
    Generate *num_questions* questions for *topic*.

    Parameters
    ----------
    topic          : Subject / concept name.
    difficulty     : Easy | Medium | Hard | Mixed.
    num_questions  : Number of questions to produce.
    evidence_rows  : Retrieved chunks to ground the questions (optional).
    as_viva        : If True, generate open-ended oral exam questions.

    Returns
    -------
    List of question strings.
    """
    evidence = ""
    if evidence_rows:
        evidence = "\n\n".join(
            f"[{r.get('doc_id')}] {r.get('evidence','')}" for r in evidence_rows[:8]
        )

    style = "viva-style open-ended oral exam" if as_viva else "MCQ/short-answer exam"
    system = (
        f"You are AcadAI's Quiz Agent. Generate exactly {num_questions} {style} questions "
        f"for a B.Tech student. Mix conceptual, applied, and one tricky question. "
        f"Return numbered questions only, no answers."
    )
    prompt = f"Topic: {topic}\nDifficulty: {difficulty}"
    if evidence:
        prompt += f"\nEvidence:\n{evidence}"

    out = call_llm(prompt, system)

    if out:
        lines = [l.strip() for l in out.split("\n") if l.strip()]
        questions = []
        for line in lines:
            clean = line.lstrip("0123456789.) ").strip()
            if clean:
                questions.append(clean)
        return questions[:num_questions]

    # Offline fallback
    return [
        f"Define {topic} in your own words.",
        f"Explain the main steps or components involved in {topic}.",
        f"Give one real-world or exam-oriented example of {topic}.",
        f"What is one common mistake students make about {topic}?",
        f"How would you compare {topic} with a related concept?",
    ][:num_questions]


def evaluate_quiz_answer(
    question: str,
    student_answer: str,
    topic: str = "",
    evidence_rows: List[Dict] = None,
) -> str:
    """
    Evaluate *student_answer* for *question*.
    Returns a feedback string starting with 'Correct' or 'Incorrect'.
    """
    evidence = ""
    if evidence_rows:
        evidence = "\n\n".join(
            f"[{r.get('doc_id')}] {r.get('evidence','')}" for r in evidence_rows[:8]
        )

    system = (
        "You are AcadAI's Viva Critic Agent. Evaluate the student's answer fairly. "
        "Begin your response with 'Correct' or 'Incorrect'. "
        "Then give: score out of 10, strengths, missing points, corrected answer, "
        "and one next practice suggestion. Use the provided evidence when possible."
    )
    prompt = f"Question: {question}\n\nStudent answer: {student_answer}"
    if topic:
        prompt = f"Topic: {topic}\n" + prompt
    if evidence:
        prompt += f"\n\nEvidence:\n{evidence}"

    out = call_llm(prompt, system)
    if out:
        return out
    return "Evaluation unavailable — add your MISTRAL_API_KEY to get detailed feedback."