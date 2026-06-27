"""
AcadAI – Data models
Chunk and AgentTrace are the two core dataclasses shared across the whole app.
"""

from dataclasses import dataclass, field


@dataclass
class Chunk:
    """A single text chunk extracted from a PDF or the demo corpus."""

    doc_id: str          # Unique identifier: "<source>::<page>.<idx>"
    source: str          # Original filename / document name
    page: int            # 1-based page number (0 when unknown)
    text: str            # Cleaned chunk text


@dataclass
class AgentTrace:
    """Lightweight audit record produced by each agent call."""

    agent: str           # Agent name, e.g. "router", "reasoning", "tutor"
    action: str          # Short label for what the agent did
    result: str          # Human-readable outcome / decision
    latency: float = 0.0 # Wall-clock seconds taken by this agent step


# ── Demo corpus ────────────────────────────────────────────────────────────────
# Used when no FAISS store and no uploaded PDFs are available.

DEMO_CHUNKS: list = [
    Chunk("dbms_notes.pdf::12", "dbms_notes.pdf", 12,
          "Normalization in DBMS is a design technique that organizes relations to reduce "
          "redundancy and avoid update, insertion, and deletion anomalies. First normal form "
          "removes repeating groups. Second normal form removes partial dependency. Third normal "
          "form removes transitive dependency."),
    Chunk("dbms_notes.pdf::13", "dbms_notes.pdf", 13,
          "A primary key uniquely identifies each row in a relation. A foreign key is an "
          "attribute in one relation that references the primary key of another relation and "
          "helps maintain referential integrity."),
    Chunk("os_notes.pdf::8", "os_notes.pdf", 8,
          "Deadlock is a condition where a set of processes are blocked because each process "
          "is holding a resource and waiting for another resource held by another process. "
          "The necessary conditions are mutual exclusion, hold and wait, no preemption, and "
          "circular wait."),
    Chunk("os_notes.pdf::18", "os_notes.pdf", 18,
          "Paging is a memory management scheme that divides logical memory into fixed-size "
          "pages and physical memory into frames. It removes external fragmentation and uses "
          "a page table to translate logical addresses into physical addresses."),
    Chunk("dsa_notes.pdf::21", "dsa_notes.pdf", 21,
          "Recursion is a programming technique where a function calls itself to solve smaller "
          "instances of the same problem. A recursive solution needs a base case and a recursive "
          "case, such as factorial n = n times factorial n minus 1."),
    Chunk("python_notes.pdf::5", "python_notes.pdf", 5,
          "Python functions are defined using the def keyword. A recursive function calls itself. "
          "Example: def factorial(n): return 1 if n<=1 else n*factorial(n-1). "
          "Base case prevents infinite recursion."),
    Chunk("os_notes.pdf::30", "os_notes.pdf", 30,
          "Process scheduling algorithms include FCFS (First Come First Served), SJF (Shortest "
          "Job First), Round Robin with time quantum, and Priority Scheduling. Round Robin is "
          "widely used in time-sharing systems."),
    Chunk("dbms_notes.pdf::40", "dbms_notes.pdf", 40,
          "SQL joins: INNER JOIN returns matching rows. LEFT JOIN returns all from left plus "
          "matches. RIGHT JOIN returns all from right plus matches. FULL OUTER JOIN returns all "
          "rows from both tables."),
]