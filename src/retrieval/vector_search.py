from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
client = QdrantClient(path="data/qdrant_db")

def vector_search(query:str,top_k : int = 5) ->list[dict]:
    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    response = client.query_points(
        collection_name='code_chunks',
        query = query_embedding,
        limit = top_k
    )
    results = []
    for point in response.points:
        chunk = point.payload.copy()
        chunk["score"] = point.score
        results.append(chunk)

    return results

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "how do I send a request"
    results = vector_search(query)
    for r in results:
        print(f"{r['score']:.3f}  {r['qualified_name']}")
    client.close()