"""
AcadAI – PDF ingestion pipeline
Handles uploading PDFs via Streamlit file-uploader and splitting extracted
text into overlapping chunks ready for indexing or TF-IDF retrieval.
"""

import tempfile
from typing import List, Tuple

from models.chunk import Chunk
from retrieval.embeddings import get_embedding_model
from utils import clean_text


def split_text(
    text: str,
    source: str,
    page: int,
    chunk_size: int = 512,
    overlap: int = 64,
) -> List[Chunk]:
    """
    Split a page's text into overlapping fixed-size Chunk objects.

    Parameters
    ----------
    text       : Raw page text (will be cleaned before splitting).
    source     : Source document name / filename.
    page       : 1-based page number this text came from.
    chunk_size : Maximum character length of each chunk.
    overlap    : Character overlap between consecutive chunks to preserve context.

    Returns
    -------
    List of Chunk objects. Chunks shorter than 60 characters are discarded.
    """
    text = clean_text(text)
    if not text:
        return []

    chunks: List[Chunk] = []
    start = 0
    idx = 1

    while start < len(text):
        part = text[start : start + chunk_size]
        if len(part) > 60:
            chunks.append(
                Chunk(f"{source}::{page}.{idx}", source, page, part)
            )
        start += max(1, chunk_size - overlap)
        idx += 1

    return chunks


def read_pdf_uploads(files) -> Tuple[List[Chunk], List[str]]:
    """
    Extract text from Streamlit-uploaded PDF files and split into chunks.

    Parameters
    ----------
    files : List of Streamlit UploadedFile objects (from st.file_uploader).

    Returns
    -------
    (chunks, skipped)
      chunks  – flat list of Chunk objects from all successfully read files.
      skipped – list of error strings for files that could not be read.

    Notes
    -----
    Requires ``pypdf``. If the package is absent the function returns an
    empty list with a single error message explaining the missing dependency.
    """
    chunks: List[Chunk] = []
    skipped: List[str] = []

    if not files:
        return chunks, skipped

    try:
        from pypdf import PdfReader
    except Exception:
        return [], ["PDF upload needs pypdf. Run: pip install pypdf"]

    for file in files:
        try:
            # Write to a named temp file so pypdf can seek over it.
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                path = tmp.name

            reader = PdfReader(path)
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                chunks.extend(split_text(text, file.name, page_num))

        except Exception as exc:
            skipped.append(f"{file.name}: {type(exc).__name__}: {exc}")

    return chunks, skipped

import os
import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


def build_faiss_store(
    chunks,
    store_dir="./knowledge_base/vector_store",
    embedding_model="all-MiniLM-L6-v2",
):
    """
    Build and save FAISS index from uploaded PDF chunks.
    """

    if not chunks:
        return False, "No chunks found"

    os.makedirs(store_dir, exist_ok=True)

    print("Embedding model:", embedding_model)

    from retrieval.embeddings import get_embedding_model

    model = get_embedding_model(embedding_model)

    if model is None:
        return False, "Failed to load embedding model"

    texts = [c.text for c in chunks]

    for c in chunks:
        print("=" * 50)
        print(c.text[:500])

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
    ).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    faiss.write_index(
        index,
        os.path.join(store_dir, "index.faiss"),
    )

    with open(
    os.path.join(store_dir, "chunks.pkl"),
    "wb",
    ) as f:
        pickle.dump(chunks, f)

    return True, f"Indexed {len(chunks)} chunks"