from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def vector_search(repository, query: str, top_k: int = 5) -> list[dict]:
    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    response = repository.qdrant.query_points(
        collection_name="code_chunks",
        query=query_embedding,
        limit=top_k,
    )

    results = []

    for point in response.points:
        chunk = point.payload.copy()
        chunk["score"] = point.score
        results.append(chunk)

    return results


if __name__ == "__main__":
    print("Run vector_search through the repository loader.")