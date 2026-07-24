import pickle
from pathlib import Path

from qdrant_client import QdrantClient

from repository import Repository


def load_repository(repo_dir: Path):

    with open(repo_dir / "bm25.pkl", "rb") as f:
        data = pickle.load(f)

    return Repository(
        repo_dir=repo_dir,
        bm25=data["bm25"],
        chunks=data["chunks"],
        qdrant=QdrantClient(path=repo_dir / "qdrant"),
    )