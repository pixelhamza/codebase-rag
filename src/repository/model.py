from dataclasses import dataclass
from qdrant_client import QdrantClient
from rank_bm25 import BM25Okapi
from pathlib import Path
@dataclass
class Repository:
    repo_dir: Path
    bm25: BM25Okapi
    chunks: list[dict]
    qdrant: QdrantClient