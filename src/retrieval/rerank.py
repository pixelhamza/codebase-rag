from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, chunks: list[dict], top_k: int = 5) -> list[dict]:
    pairs = []   
    #pair the chunked code
    for chunk in chunks:
        text = (
            chunk["qualified_name"] + "\n" +
            (chunk["docstring"] or "") + "\n" +
            chunk["source"]
        )

        pairs.append([query, text])

    #rank in batches
    scores = reranker.predict(pairs)

    for i in range(len(chunks)):
        chunks[i]["rerank_score"] = float(scores[i])

    #Sort highest score first
    chunks.sort(key=lambda chunk: chunk["rerank_score"], reverse=True)

    return chunks[:top_k]
