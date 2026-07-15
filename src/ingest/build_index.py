import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from qdrant_client.models import PointStruct

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
client = QdrantClient(path="data/qdrant_db")       

def load_chunks(path: str)-> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f]


def vector_indexing(chunks: list[dict]): 
    client.recreate_collection(
        collection_name="code_chunks",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    texts = []

    for chunk in chunks:
        text = f"""
    Qualified Name: {chunk['qualified_name']}

    Docstring:
    {chunk['docstring'] or ""} 

    Source:
    {chunk['source']}
    """
        texts.append(text.strip())

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    points = []

    for i, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
        points.append(
            PointStruct(
                id=i,
                vector=embedding.tolist(),
                payload=chunk,
            )
        )

    client.upsert(
        collection_name="code_chunks",
        points=points,
    )
    client.close()

if __name__ == "__main__":
    chunks = load_chunks("data/chunks.jsonl")
    vector_indexing(chunks)
    print(f"Indexed {len(chunks)} chunks into Qdrant.")


