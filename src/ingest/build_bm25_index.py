import json
import pickle
import re
from rank_bm25 import BM25Okapi


def load_chunks(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f]


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())

def build_bm25_index(chunks: list[dict]):
    texts = []

    for chunk in chunks:
        text = ""

        text += chunk["qualified_name"] + "\n\n"

        if chunk.get("docstring"):
            text += chunk["docstring"] + "\n\n"

        text += chunk["source"]

        texts.append(text)

    tokenized_corpus = []

    for text in texts:
        tokens = tokenize(text)
        tokenized_corpus.append(tokens)

    bm25 = BM25Okapi(tokenized_corpus)

    return bm25

if __name__ == "__main__":
    chunks = load_chunks("data/chunks.jsonl")
    bm25 = build_bm25_index(chunks)
    with open("data/bm25_index.pkl", "wb") as f:
        pickle.dump({"bm25": bm25, "chunks": chunks}, f)
    print(f"Built BM25 index over {len(chunks)} chunks.")