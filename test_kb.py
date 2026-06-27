import pickle

with open("knowledge_base/vector_store/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

print(type(chunks))
print(type(chunks[0]))
print(chunks[0])