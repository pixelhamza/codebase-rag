from src.retrieval.fuse import rrf
from src.retrieval.rerank import rerank

from src.generation.prompt import build_prompt
from src.generation.llm import generate


def answer(query):
    candidates = rrf(query)
    ranked = rerank(query, candidates)

    top_chunks = ranked[:5]

    prompt = build_prompt(query, top_chunks)

    response = generate(prompt)

    return {
        "answer": response,
        "sources": top_chunks
    }