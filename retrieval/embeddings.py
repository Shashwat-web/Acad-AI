"""
AcadAI – Embedding models
"""

import streamlit as st

try:
    from sentence_transformers import SentenceTransformer, CrossEncoder
except Exception:
    SentenceTransformer = None
    CrossEncoder = None


@st.cache_resource(show_spinner=False)
def get_embedding_model(model_name: str): 
    if SentenceTransformer is None:
        return None

    try:
        return SentenceTransformer(
            model_name,
            local_files_only=False
        )
    except Exception as e:
        print("Embedding load error:", e)
        return None


@st.cache_resource(show_spinner=False)
def get_cross_encoder(model_name: str):
    if CrossEncoder is None:
        return None

    try:
        return CrossEncoder(model_name)
    except Exception:
        return None