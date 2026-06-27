"""
AcadAI – Hybrid FAISS retrieval pipeline
Dense embedding → hybrid scoring → optional cross-encoder re-rank →
subject filtering → keyword/lexical fallbacks → neighbour context expansion.
"""

import numpy as np
import time 
from typing import List, Dict, Tuple

from models.chunk import Chunk
from utils import clean_text, quote, keyword_overlap
from config import (
    DEFAULT_TOP_K, DEFAULT_CANDIDATE_K,
    DEFAULT_MIN_HYBRID_SCORE, DEFAULT_EMBEDDING_MODEL,
    DEFAULT_CROSS_ENCODER_MODEL,
)
from retrieval.subject import (
    infer_subject, detect_query_subjects, is_subnetting_query,
    expand_query, source_subject_boost,
)
from retrieval.keyword import keyword_fallback_search, lexical_subject_scan, _cn_keyword_score
from retrieval.embeddings import get_embedding_model, get_cross_encoder

try:
    import faiss as _faiss
except Exception:
    _faiss = None

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity as _cos_sim
    _sklearn_ok = True
except Exception:
    _sklearn_ok = False


# ── Helpers ────────────────────────────────────────────────────────────────────

def _normalize_dense(raw: np.ndarray, index) -> np.ndarray:
    scores = raw.astype("float32")
    if len(scores) == 0:
        return scores
    metric_type = getattr(index, "metric_type", None)
    if _faiss and metric_type == _faiss.METRIC_INNER_PRODUCT:
        mn, mx = float(scores.min()), float(scores.max())
        return (scores - mn) / (mx - mn + 1e-9)
    inv = 1.0 / (1.0 + np.maximum(scores, 0))
    mn, mx = float(inv.min()), float(inv.max())
    return (inv - mn) / (mx - mn + 1e-9)


def _tfidf_scores(query: str, texts: List[str]) -> np.ndarray:
    if not texts or not _sklearn_ok:
        return np.zeros(len(texts), dtype="float32")
    try:
        vec    = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=8000)
        matrix = vec.fit_transform([query] + texts)
        return _cos_sim(matrix[0:1], matrix[1:]).ravel().astype("float32")
    except Exception:
        return np.zeros(len(texts), dtype="float32")


def _expand_neighbour_context(
    results: List[Dict], chunks: List[Chunk], max_extra_chars: int = 350
) -> List[Dict]:
    improved = []
    for r in results:
        idx   = int(r.get("chunk_index", -1))
        texts = [r["text"]]
        base  = chunks[idx] if 0 <= idx < len(chunks) else None
        for nidx in (idx - 1, idx + 1):
            if base and 0 <= nidx < len(chunks):
                n = chunks[nidx]
                if n.source == base.source and abs((n.page or 0) - (base.page or 0)) <= 1 and n.text:
                    texts.append(n.text[:max_extra_chars])
        r = dict(r)
        r["text"]     = clean_text(" ".join(texts))
        r["evidence"] = quote(r["text"], 420)
        improved.append(r)
    return improved


def _cross_encoder_rerank(query: str, rows: List[Dict], model_name: str) -> List[Dict]:
    reranker = get_cross_encoder(model_name)
    if reranker is None or not rows:
        return rows
    try:
        pairs     = [[query, r["text"]] for r in rows]
        ce_scores = reranker.predict(pairs)
        for r, s in zip(rows, ce_scores):
            r["cross_score"] = round(float(s), 4)
        rows.sort(key=lambda x: x.get("cross_score", -999), reverse=True)
        for i, r in enumerate(rows, 1):
            r["rank"] = i
    except Exception:
        pass
    return rows


def _filter_by_subject(
    candidate_rows, query: str, mode: str = "auto", manual_subject: str = "Any"
) -> Tuple[list, str]:
    if mode == "off":
        return candidate_rows, "Subject filter off"
    wanted = []
    if manual_subject and manual_subject != "Any":
        wanted = [manual_subject]
    elif mode == "auto":
        wanted = detect_query_subjects(query)
    if not wanted:
        return candidate_rows, "No subject detected"

    filtered = [
        row for row in candidate_rows
        if infer_subject(row[2].text, row[2].source) in wanted
    ]

    is_strong_cn = "CN" in wanted and is_subnetting_query(query)
    if len(filtered) >= 1 and is_strong_cn:
        return filtered, f"Strong CN filter: {', '.join(wanted)}"
    if len(filtered) >= 3:
        return filtered, f"Filtered to subject(s): {', '.join(wanted)}"
    return candidate_rows, f"Filter too strict; kept all. Detected: {', '.join(wanted)}"


# ── TF-IDF baseline retriever (no FAISS) ──────────────────────────────────────

def retrieve_tfidf(
    query: str, chunks: List[Chunk], top_k: int = DEFAULT_TOP_K
) -> Tuple[List[Dict], Dict]:
    if not chunks or not _sklearn_ok:
        return [], {"match": False, "reason": "No chunks or sklearn unavailable", "overlap": 0.0}
    corpus = [c.text for c in chunks]
    scores = _tfidf_scores(query, corpus)
    ranked = np.argsort(scores)[::-1][:top_k]
    results = []
    for rank, idx in enumerate(ranked, 1):
        c = chunks[int(idx)]
        results.append({
            "rank":    rank,
            "doc_id":  c.doc_id,
            "source":  c.source,
            "page":    c.page,
            "score":   float(scores[int(idx)]),
            "overlap": keyword_overlap(query, c.text),
            "evidence": quote(c.text),
            "text":    c.text,
            "chunk_index": int(idx),
        })
    best    = float(scores[int(ranked[0])]) if ranked.size else 0.0
    combined = " ".join(r["text"] for r in results[:3])
    overlap  = keyword_overlap(query, combined)
    match    = best >= 0.18 or overlap >= 0.34
    return results, {
        "match": match,
        "reason": f"TF-IDF: best={best:.2f}, overlap={overlap:.0%}",
        "overlap": overlap, "best_score": best,
    }


# ── Main hybrid FAISS retriever ────────────────────────────────────────────────

def retrieve_faiss(
    query: str,
    index,
    chunks: List[Chunk],
    embedding_model_name: str  = DEFAULT_EMBEDDING_MODEL,
    top_k: int                 = DEFAULT_TOP_K,
    candidate_k: int           = DEFAULT_CANDIDATE_K,
    min_hybrid_score: float    = DEFAULT_MIN_HYBRID_SCORE,
    use_hybrid_rerank: bool    = True,
    use_cross_encoder: bool    = False,
    cross_encoder_model: str   = DEFAULT_CROSS_ENCODER_MODEL,
    subject_filter_mode: str   = "auto",
    manual_subject: str        = "Any",
    use_llm_expansion: bool    = False,
    parent_context_chars: int  = 900,
) -> Tuple[List[Dict], Dict]:
    """
    Full hybrid retrieval pipeline:
    1. Query expansion (academic synonyms + optional LLM)
    2. Dense FAISS ANN search
    3. Subject-based soft filtering
    4. Hybrid score = 0.55 * dense + 0.45 * TF-IDF + boosts
    5. Keyword / lexical fallbacks when dense misses
    6. Optional cross-encoder re-rank
    7. Neighbour context expansion
    """
    if _faiss is None or index is None or not chunks:
        return retrieve_tfidf(query, chunks, top_k)

    try:
        # 1. Expand query
        expanded = expand_query(query)
        if use_llm_expansion:
            from llm.mistral import llm_query_expansion
            expanded = llm_query_expansion(expanded)

        # E5 models want a 'query:' prefix
        model_query = (
            "query: " + expanded
            if "e5" in embedding_model_name.lower() and not expanded.lower().startswith("query:")
            else expanded
        )

        # 2. Dense ANN
                # ---------------- Embedding model lookup ----------------
        t0 = time.perf_counter()

        embed_model = get_embedding_model(embedding_model_name)

        if embed_model is None:
            return retrieve_tfidf(query, chunks, top_k)

        # ---------------- Query embedding ----------------
        t0 = time.perf_counter()

        q_vec = embed_model.encode(
            [model_query],
            normalize_embeddings=True,
        ).astype("float32")

        k_search = min(candidate_k, index.ntotal)

        # ---------------- FAISS search ----------------
        t0 = time.perf_counter()

        raw_scores, raw_indices = index.search(q_vec, k_search)

        
        raw_scores = raw_scores[0]
        raw_indices = raw_indices[0]

        # 3. Build candidate rows
        valid = [(pos, int(idx), chunks[int(idx)])
                 for pos, idx in enumerate(raw_indices)
                 if 0 <= int(idx) < len(chunks)]
        if not valid:
            return retrieve_tfidf(query, chunks, top_k)

        valid, subject_note = _filter_by_subject(valid, query, subject_filter_mode, manual_subject)

        valid_scores   = _normalize_dense(raw_scores[:len(valid)], index)
        candidate_texts = [c.text for _, _, c in valid]

        # 4. Hybrid score
        # Skip expensive TF-IDF computation
        lex = np.zeros(len(candidate_texts), dtype="float32")

        overlaps = np.array(
            [keyword_overlap(expanded, t) for t in candidate_texts],
            dtype="float32",
        )

        required_subjects = detect_query_subjects(query)
        hybrid_scores = []
        for i, (pos, idx, c) in enumerate(valid):
            dense_w   = 0.55
            lexical_w = 0.45
            hybrid    = dense_w * float(valid_scores[i]) + lexical_w * float(lex[i])
            hybrid   += float(overlaps[i]) * 0.15
            hybrid   += source_subject_boost(c.source, required_subjects)
            if is_subnetting_query(query):
                hybrid += 0.25 * _cn_keyword_score(c.text)
            hybrid_scores.append(hybrid)

        order = np.argsort(np.array(hybrid_scores))[::-1]

        # 5. Select, deduplicate, apply subject guards
        pre_selected: List[Dict] = []
        seen_keys: set = set()

        for cand_i in order:
            pos, idx, c = valid[int(cand_i)]
            subject     = infer_subject(c.text, c.source)
            key         = (c.source, c.page, c.text[:90])
            if key in seen_keys:
                continue

            ov = float(overlaps[int(cand_i)])
            lx = float(lex[int(cand_i)])

            if required_subjects and subject not in required_subjects and ov < 0.15 and lx < 0.05:
                continue
            if "CN" in required_subjects and any(
                x in query.lower() for x in ["subnet", "subnetting", "cidr", "vlsm", "ip address"]
            ) and subject != "CN" and ov < 0.18:
                continue

            seen_keys.add(key)
            pre_selected.append({
                "rank":           len(pre_selected) + 1,
                "doc_id":         c.doc_id,
                "source":         c.source,
                "page":           c.page,
                "subject":        subject,
                "score":          float(valid_scores[int(cand_i)]),
                "dense_norm":     round(float(valid_scores[int(cand_i)]), 4),
                "lexical":        round(lx, 4),
                "hybrid_score":   round(float(hybrid_scores[int(cand_i)]), 4),
                "overlap":        round(ov, 4),
                "chunk_index":    idx,
                "evidence":       quote(c.text, 420),
                "text":           c.text,
            })
            if len(pre_selected) >= top_k * 2:
                break

        # Keyword fallbacks when dense misses
        if not pre_selected:
            fb  = lexical_subject_scan(query, chunks, required_subjects, limit=max(candidate_k, 80))
            kw  = keyword_fallback_search(query, chunks, required_subjects, top_k=max(candidate_k, 80))
            merged = fb + kw
            if not merged:
                return [], {"match": False, "reason": f"No chunks after filtering. {subject_note}", "overlap": 0.0}
            seen_fb: set = set()
            deduped: List[Dict] = []
            for row in sorted(merged, key=lambda r: float(r.get("hybrid_score", 0)), reverse=True):
                k = (row.get("source"), row.get("page"), row.get("text", "")[:90])
                if k not in seen_fb:
                    seen_fb.add(k)
                    deduped.append(row)
            pre_selected = deduped[:top_k * 2]
            subject_note += " | keyword fallback used"

        # Mix in keyword fallback when best result is weak
        if pre_selected:
            if float(pre_selected[0].get("overlap", 0)) < 0.08 or float(pre_selected[0].get("hybrid_score", 0)) < min_hybrid_score:
                kw = keyword_fallback_search(query, chunks, required_subjects, top_k=40)
                if kw:
                    merged2 = pre_selected + kw
                    seen2: set = set()
                    mixed: List[Dict] = []
                    for row in sorted(merged2, key=lambda r: float(r.get("hybrid_score", 0)), reverse=True):
                        k = (row.get("source"), row.get("page"), row.get("text", "")[:90])
                        if k not in seen2:
                            seen2.add(k)
                            mixed.append(row)
                    pre_selected = mixed[:top_k * 3]
                    subject_note += " | weak-result keyword mix"

        # 6. Optional cross-encoder re-rank
        if use_cross_encoder:
            pre_selected = _cross_encoder_rerank(expanded, pre_selected, cross_encoder_model)

        # CN subnetting: float CN chunks to the top
        if is_subnetting_query(query):
            cn_rows  = [r for r in pre_selected if r.get("subject") == "CN" or _cn_keyword_score(r.get("text", "")) > 0]
            rest     = [r for r in pre_selected if r not in cn_rows]
            pre_selected = cn_rows + rest

        selected = pre_selected[:top_k]

        # 7. Neighbour context expansion
        selected = _expand_neighbour_context(selected, chunks, parent_context_chars)

        combined    = " ".join(r["text"] for r in selected[:5])
        overlap     = keyword_overlap(expanded, combined)
        best_hybrid = float(selected[0].get("hybrid_score", 0.0)) if selected else 0.0
        best_raw    = float(selected[0].get("score", 0.0)) if selected else 0.0
        best_cross  = selected[0].get("cross_score", "off") if selected else "off"
        match       = bool(selected) and (best_hybrid >= min_hybrid_score or overlap >= 0.08)

        return selected, {
            "match":          match,
            "reason":         f"hybrid={best_hybrid:.3f}, raw={best_raw:.3f}, cross={best_cross}, overlap={overlap:.0%}. {subject_note}",
            "overlap":        overlap,
            "best_score":     best_raw,
            "best_hybrid":    best_hybrid,
            "expanded_query": expanded,
        }

    except Exception as exc:
        return [], {"match": False, "reason": f"FAISS retrieval failed: {type(exc).__name__}: {exc}", "overlap": 0.0}