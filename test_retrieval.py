from retrieval.faiss_store import load_faiss_store
from retrieval.embeddings import get_embedding_model
from config import DEFAULT_FAISS_DIR, DEFAULT_EMBEDDING_MODEL

index, chunks, err = load_faiss_store(DEFAULT_FAISS_DIR)

if index is None:
    print(err)
    exit()

model = get_embedding_model(DEFAULT_EMBEDDING_MODEL)

query = "database normalization 1NF 2NF 3NF DBMS"

query_embedding = model.encode(
    [query],
    convert_to_numpy=True,
    normalize_embeddings=True,
)

scores, indices = index.search(query_embedding, 5)

print("\nTop Results\n")

for score, idx in zip(scores[0], indices[0]):

    chunk = chunks[idx]

    print("=" * 70)
    print("Score :", score)
    print("Source:", chunk.source)
    print(chunk.text[:350])