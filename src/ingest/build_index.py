import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def load_chunks(path: Path) -> list[dict]:
    with open(path, "r") as f:
        return [json.loads(line) for line in f]


def vector_indexing(repo_dir: Path):
    """
    Builds the vector index for a repository.

    Expected structure:
        repo_dir/
            chunks.jsonl
            qdrant/
    """

    chunks = load_chunks(repo_dir / "chunks.jsonl")

    client = QdrantClient(path=repo_dir / "qdrant")

    client.recreate_collection(
        collection_name="code_chunks",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        ),
    )

    texts = []

    for chunk in chunks:
        text = f"""
Qualified Name: {chunk['qualified_name']}

Docstring:
{chunk.get('docstring') or ""}

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

    print(f"Indexed {len(chunks)} chunks into Qdrant.")