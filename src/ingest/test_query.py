from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
client = QdrantClient(path="data/qdrant_db")

results = client.query_points(
    collection_name="code_chunks",
    query=model.encode("how do I send a request").tolist(),
    limit=3,
)
for r in results.points:
    print(r.payload["qualified_name"], r.score)