import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chroma_db")

# Delete old collection if exists
try:
    client.delete_collection("company_docs")
except:
    pass

collection = client.get_or_create_collection("company_docs")

chunks = [
    "Employees receive 20 paid leave days annually.",
    "Work from home is allowed 3 days per week.",
    "Medical insurance is provided to all employees.",
    "Employees are expected to work 8 hours per day.",
    "Annual performance reviews are conducted in December."
]

for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk).tolist()

    collection.add(
        ids=[f"doc_{i}"],
        documents=[chunk],
        embeddings=[embedding]
    )

print("Vector DB recreated with chunks!")