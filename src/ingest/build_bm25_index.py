import json
import pickle
import re
from pathlib import Path

from rank_bm25 import BM25Okapi


def load_chunks(path: Path) -> list[dict]:
    with open(path, "r") as f:
        return [json.loads(line) for line in f]


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def build_bm25_index(chunks: list[dict]) -> BM25Okapi:
    texts = []

    for chunk in chunks:
        text = ""
        text += chunk["qualified_name"] + "\n\n"
        if chunk.get("docstring"):
            text += chunk["docstring"] + "\n\n"
        text += chunk["source"]

        texts.append(text)

    tokenized_corpus = [tokenize(text) for text in texts]

    return BM25Okapi(tokenized_corpus)

def build_bm25(repo_dir: Path):

    chunks = load_chunks(repo_dir / "chunks.jsonl")

    bm25 = build_bm25_index(chunks)

    with open(repo_dir / "bm25.pkl", "wb") as f:
        pickle.dump(
            {
                "bm25": bm25,
                "chunks": chunks,
            },
            f,
        )

    print(f"Built BM25 index over {len(chunks)} chunks.")