"""
AcadAI – Keyword / lexical retrieval
Fast fallbacks used when dense FAISS retrieval returns weak results.
"""

import numpy as np
from typing import List, Dict

from models.chunk import Chunk
from utils import clean_text, tokenize, quote, keyword_overlap
from retrieval.subject import (
    infer_subject, detect_query_subjects, is_subnetting_query,
    expand_query, source_subject_boost,
)


def _cn_keyword_score(text: str) -> float:
    tokens = [
        "subnet", "subnetting", "cidr", "vlsm", "subnet mask", "network address",
        "broadcast address", "host", "hosts", "ip address", "ipv4", "prefix",
        "classful", "classless", "routing", "network", "bits", "borrow",
    ]
    hay = text.lower()
    return sum(1 for t in tokens if t in hay) / max(1, len(tokens))


def _lexical_scores(query: str, texts: List[str]) -> np.ndarray:
    """TF-IDF cosine similarity over *texts* vs *query*."""
    if not texts:
        return np.array([], dtype="float32")
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        vec    = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=8000)
        matrix = vec.fit_transform([query] + texts)
        return cosine_similarity(matrix[0:1], matrix[1:]).ravel().astype("float32")
    except Exception:
        return np.zeros(len(texts), dtype="float32")


def keyword_fallback_search(
    query: str,
    chunks: List[Chunk],
    wanted_subjects: List[str],
    top_k: int = 30,
) -> List[Dict]:
    """
    Exact-hit + TF-IDF keyword search over *all* chunks.
    Used when semantic FAISS misses the topic entirely.
    """
    expanded = expand_query(query)
    q_set    = {t for t in tokenize(expanded) if len(t) > 2}
    rows     = []

    key_phrases = [
        "subnet mask", "network address", "broadcast address", "ip address",
        "primary key", "foreign key", "operating system", "machine learning",
        "software engineering", "data warehouse",
    ]

    for idx, c in enumerate(chunks):
        subject      = infer_subject(c.text, c.source)
        text_l       = c.text.lower()
        source_boost = source_subject_boost(c.source, wanted_subjects)
        exact_hits   = sum(1 for t in q_set if t in text_l)
        phrase_hits  = sum(
            3 for p in key_phrases
            if p in expanded.lower() and p in text_l
        )

        if exact_hits == 0 and phrase_hits == 0 and source_boost == 0:
            continue

        overlap         = keyword_overlap(expanded, c.text)
        subject_quality = 0.20 if subject in wanted_subjects else 0.0
        if is_subnetting_query(query):
            subject_quality += 0.35 * _cn_keyword_score(c.text)

        score = exact_hits + phrase_hits + (10 * overlap) + (10 * source_boost) + (10 * subject_quality)
        rows.append((score, idx, c, subject, overlap))

    rows.sort(reverse=True, key=lambda x: x[0])
    results = []
    for rank, (score, idx, c, subject, overlap) in enumerate(rows[:top_k], 1):
        results.append({
            "rank":           rank,
            "doc_id":         c.doc_id,
            "source":         c.source,
            "page":           c.page,
            "subject":        subject,
            "score":          float(score),
            "dense_norm":     0.0,
            "lexical":        round(float(score), 4),
            "hybrid_score":   round(float(score / 10.0), 4),
            "overlap":        round(float(overlap), 4),
            "chunk_index":    idx,
            "evidence":       quote(c.text, 420),
            "text":           c.text,
            "retrieval_mode": "keyword_fallback",
        })
    return results


def lexical_subject_scan(
    query: str,
    chunks: List[Chunk],
    wanted_subjects: List[str],
    limit: int = 80,
) -> List[Dict]:
    """
    Fallback: TF-IDF scan restricted to subject-matching chunks.
    """
    pool = [
        (idx, c) for idx, c in enumerate(chunks)
        if (not wanted_subjects or infer_subject(c.text, c.source) in wanted_subjects)
        and not (is_subnetting_query(query)
                 and infer_subject(c.text, c.source) == "CN"
                 and _cn_keyword_score(c.text) <= 0)
    ]
    if not pool:
        return []

    texts  = [c.text for _, c in pool]
    scores = _lexical_scores(expand_query(query), texts)
    order  = np.argsort(scores)[::-1][:limit]

    rows = []
    for rank, oi in enumerate(order, 1):
        idx, c = pool[int(oi)]
        score  = float(scores[int(oi)])
        if score <= 0:
            continue
        rows.append({
            "rank":           rank,
            "doc_id":         c.doc_id,
            "source":         c.source,
            "page":           c.page,
            "subject":        infer_subject(c.text, c.source),
            "score":          score,
            "dense_norm":     0.0,
            "lexical":        round(score, 4),
            "hybrid_score":   round(score, 4),
            "overlap":        round(keyword_overlap(expand_query(query), c.text), 4),
            "chunk_index":    idx,
            "evidence":       quote(c.text, 420),
            "text":           c.text,
            "retrieval_mode": "lexical_subject_fallback",
        })
    return rows