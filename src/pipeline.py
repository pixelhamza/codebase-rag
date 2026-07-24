from src.retrieval.fuse import rrf
from src.retrieval.rerank import rerank

from src.generation.prompt import build_prompt
from src.generation.llm import generate


def answer(repository,query):
    candidates = rrf(repository,query, top_k=10)
    ranked = rerank(query, candidates, top_k=5)

    prompt = build_prompt(query, ranked)
    response = generate(prompt)

    return {
        "answer": response,
        "sources": ranked
    }