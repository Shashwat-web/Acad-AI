"""
AcadAI – Configuration
All constants, environment variables, and subject keyword maps live here.
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# ── App identity ───────────────────────────────────────────────────────────────
APP_TITLE = "AcadAI"

# ── Retrieval defaults ─────────────────────────────────────────────────────────
DEFAULT_TOP_K: int = 4  # Lightweight default for local/laptop use
DEFAULT_FAISS_DIR: str = os.getenv(
    "DEFAULT_FAISS_DIR",
    "./knowledge_base/vector_store"
)
DEFAULT_EMBEDDING_MODEL: str = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)
DEFAULT_CANDIDATE_K: int = int(os.getenv("FAISS_CANDIDATE_K", "50"))
DEFAULT_MIN_HYBRID_SCORE: float = float(os.getenv("MIN_HYBRID_SCORE", "0.25"))
DEFAULT_CROSS_ENCODER_MODEL: str = os.getenv(
    "CROSS_ENCODER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

# ── Subject keyword map ────────────────────────────────────────────────────────
# Used as soft signals when index.pkl has no true metadata.
SUBJECT_KEYWORDS: dict = {
    "CN": [
        "qos", "quality of service", "bandwidth", "latency", "jitter", "packet", "routing",
        "tcp", "udp", "ip", "network", "congestion", "subnet", "subnetting", "subnet mask",
        "cidr", "vlsm", "classless", "classful", "network address", "broadcast address",
        "host address", "default gateway", "ipv4", "ip address", "prefix", "slash notation",
        "supernetting", "lan", "wan", "osi", "dns", "http",
    ],
    "OS": [
        "operating system", "deadlock", "paging", "segmentation", "process", "thread",
        "scheduler", "memory management", "semaphore", "mutex", "cpu scheduling", "virtual memory",
    ],
    "DBMS": [
        "dbms", "database", "sql", "normalization", "transaction", "acid", "primary key",
        "foreign key", "join", "relational", "schema", "er diagram", "indexing",
    ],
    "DSA": [
        "algorithm", "data structure", "tree", "graph", "recursion", "dynamic programming",
        "stack", "queue", "array", "linked list", "sorting", "searching",
    ],
    "PYTHON": [
        "python", "function", "def ", "list", "tuple", "dictionary",
        "pandas", "numpy", "regex", "regular expression",
    ],
    "WEB": [
        "web technology", "html", "css", "javascript", "react", "node", "http",
        "dom", "browser", "frontend", "backend", "servlet", "php",
    ],
    "SE": [
        "software engineering", "sdlc", "waterfall", "agile", "scrum", "requirement",
        "testing", "uml", "use case", "software design", "maintenance",
    ],
    "ML": [
        "machine learning", "ml", "classification", "regression", "clustering", "neural",
        "svm", "decision tree", "reinforcement learning", "training", "feature",
    ],
    "DWM": [
        "data warehousing", "data mining", "olap", "etl", "star schema", "snowflake",
        "association rule", "apriori", "classification", "clustering",
    ],
    "DA": [
        "data analytics", "analytics", "visualization", "statistics", "mean", "median",
        "variance", "correlation", "dashboard", "power bi", "tableau",
    ],
    "HV": [
        "human values", "ethics", "value education", "professional ethics",
        "harmony", "society", "human conduct",
    ],
}

# ── Subject query hint map (for query-side subject detection) ──────────────────
SUBJECT_QUERY_HINTS: dict = {
    "CN": [
        "subnet", "subnetting", "cidr", "vlsm", "ip address", "ipv4", "subnet mask",
        "network address", "broadcast address", "host address", "qos", "routing",
        "tcp", "udp", "osi", "dns",
    ],
    "OS": [
        "operating system", "deadlock", "paging", "segmentation", "process", "thread",
        "semaphore", "scheduling", "virtual memory",
    ],
    "DBMS": [
        "dbms", "database", "sql", "normalization", "transaction", "acid",
        "primary key", "foreign key", "join", "er diagram",
    ],
    "DSA": [
        "algorithm", "data structure", "recursion", "tree", "graph",
        "dynamic programming", "array", "linked list", "sorting",
    ],
    "PYTHON": ["python", "regex", "pandas", "numpy", "dictionary", "tuple", "list comprehension"],
    "WEB": [
        "web technology", "html", "css", "javascript", "react", "node",
        "dom", "http", "frontend", "backend",
    ],
    "SE": ["software engineering", "sdlc", "agile", "waterfall", "uml", "testing", "requirement", "scrum"],
    "ML": ["machine learning", "classification", "regression", "clustering", "neural network", "svm", "decision tree"],
    "DWM": ["data warehouse", "data warehousing", "data mining", "olap", "etl", "star schema", "apriori"],
    "DA": ["data analytics", "visualization", "statistics", "correlation", "dashboard"],
    "HV": ["human values", "ethics", "harmony", "professional ethics"],
}

# ── Subject expansion strings (for query expansion during retrieval) ───────────
SUBJECT_EXPANSIONS: dict = {
    "CN": (
        "computer networks subnetting numericals ip addressing ipv4 cidr vlsm subnet mask "
        "network address broadcast address usable hosts host range prefix length class a class b "
        "class c classful classless host bits borrowed bits number of subnets hosts per subnet "
        "routing qos bandwidth latency jitter packet loss osi dns tcp udp"
    ),
    "OS": (
        "operating systems memory management process scheduling deadlock paging segmentation "
        "threads synchronization semaphores virtual memory cpu scheduling"
    ),
    "DBMS": (
        "database management system sql normalization transaction acid primary key foreign key "
        "joins relational schema er diagram indexing"
    ),
    "DSA": (
        "data structures algorithms complexity recursion graph tree dynamic programming "
        "stack queue array linked list sorting searching"
    ),
    "PYTHON": "python programming functions data types regex list tuple dictionary pandas numpy",
    "WEB": (
        "web technology html css javascript dom browser http client server "
        "frontend backend react node servlet php"
    ),
    "SE": (
        "software engineering sdlc waterfall agile scrum requirements testing "
        "uml use case software design maintenance"
    ),
    "ML": (
        "machine learning classification regression clustering neural network svm "
        "decision tree training feature model evaluation"
    ),
    "DWM": (
        "data warehousing data mining etl olap star schema snowflake schema "
        "association rule apriori classification clustering"
    ),
    "DA": (
        "data analytics statistics visualization correlation dashboard "
        "business intelligence power bi tableau"
    ),
    "HV": "human values ethics harmony society professional ethics value education",
}

# ── Academic synonym map (lightweight query expansion) ────────────────────────
ACADEMIC_SYNONYMS: dict = {
    "qos": "quality of service bandwidth latency jitter packet loss traffic prioritization",
    "subnet": (
        "subnetting ip addressing cidr vlsm subnet mask network address broadcast address "
        "usable hosts host range prefix length"
    ),
    "subnetting": (
        "ip addressing cidr vlsm subnet mask network address broadcast address "
        "usable hosts host range prefix length classful classless"
    ),
    "cidr": "classless inter domain routing prefix length subnet mask network address broadcast address host range",
    "vlsm": "variable length subnet mask subnetting cidr host requirement network allocation",
    "os": "operating system memory management process scheduling deadlock paging segmentation",
    "dbms": "database management system sql normalization transaction acid keys joins",
    "cn": "computer networks tcp ip routing congestion control quality of service subnetting cidr vlsm",
    "dsa": "data structures algorithms complexity recursion graph tree dynamic programming",
}