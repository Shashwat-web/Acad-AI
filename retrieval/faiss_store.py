"""
AcadAI – FAISS store loader
Loads index.faiss + index.pkl from disk and converts the pickle's varied
formats (LangChain docstore, plain list, dict) into our Chunk dataclass.
"""

import os
import streamlit as st

from models.chunk import Chunk
from utils import clean_text

try:
    import faiss
except Exception:
    faiss = None


def _doc_to_chunk(doc, fallback_id: str, source: str = "faiss_store") -> Chunk:
    """Convert a LangChain Document-like object into a Chunk."""
    text = getattr(doc, "page_content", None) or getattr(doc, "text", None) or str(doc)
    meta = getattr(doc, "metadata", {}) or {}
    return Chunk(
        str(meta.get("doc_id", fallback_id)),
        str(meta.get("source", source)),
        int(meta.get("page", 0) or 0),
        clean_text(text),
    )


def _extract_chunks_from_pickle(obj) -> list:
    """
    Supports common FAISS pickle formats:
      - LangChain tuple: (docstore, index_to_docstore_id)
      - Plain list of Chunk / Document / dict
      - Dict with 'chunks', 'documents', 'docs', or 'texts' key
    """
    chunks = []

    # LangChain FAISS: (docstore, index_to_docstore_id)
    if isinstance(obj, tuple) and len(obj) >= 2:
        docstore, index_to_docstore_id = obj[0], obj[1]
        docs = getattr(docstore, "_dict", None)
        if isinstance(docs, dict) and isinstance(index_to_docstore_id, dict):
            for i in sorted(index_to_docstore_id):
                doc_id = index_to_docstore_id[i]
                doc = docs.get(doc_id)
                if doc is not None:
                    chunks.append(_doc_to_chunk(doc, str(doc_id)))
            return chunks

    # Plain list
    if isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, Chunk):
                chunks.append(item)
            elif isinstance(item, dict):
                text = (
                    item.get("page_content")
                    or item.get("text")
                    or item.get("content")
                    or ""
                )
                chunks.append(Chunk(
                    str(item.get("doc_id", f"faiss::{i}")),
                    str(item.get("source", "faiss_store")),
                    int(item.get("page", 0) or 0),
                    clean_text(text),
                ))
            else:
                chunks.append(_doc_to_chunk(item, f"faiss::{i}"))
        return [c for c in chunks if c.text]

    # Dict wrapper
    if isinstance(obj, dict):
        items = (
            obj.get("chunks")
            or obj.get("documents")
            or obj.get("docs")
            or obj.get("texts")
        )
        if isinstance(items, list):
            return _extract_chunks_from_pickle(items)

    return chunks


@st.cache_resource(show_spinner=False)
def load_faiss_store(store_dir: str):
    """
    Load a FAISS index from *store_dir*.

    Returns
    -------
    (index, chunks, error_message)
      index   – faiss.Index or None
      chunks  – list of Chunk objects (may be empty)
      error   – human-readable error string (empty on success)
    """
    if faiss is None:
        return None, [], "FAISS package missing. Install: pip install faiss-cpu"

    index_path = os.path.join(store_dir, "index.faiss")
    pkl_path = os.path.join(store_dir, "chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(pkl_path):
        return None, [], f"index.faiss / index.pkl not found in: {store_dir}"

    try:
        import pickle
        index = faiss.read_index(index_path)
        with open(pkl_path, "rb") as f:
            obj = pickle.load(f)
        chunks = _extract_chunks_from_pickle(obj)
        if not chunks:
            return index, [], "FAISS index loaded but index.pkl format was not recognised."
        return index, chunks, ""
    except Exception as exc:
        return None, [], f"FAISS load failed: {type(exc).__name__}: {exc}"