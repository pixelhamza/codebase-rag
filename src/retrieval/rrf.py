from bm25_search import bm25_search
from vector_search import vector_search

RRF_K = 60
def rrf(query :str ,top_k : int = 5): 
    bm25_results = bm25_search(query,top_k = 10) #rrf needs a reasonale candidate pool i.e why 10
    vector_results = vector_search(query, top_k=10)

    rrf_scores = {}
    chunk_lookup = { }

    #BM25 contribution
    rank =1
    for chunk in bm25_results:
        chunk_id = chunk["id"]

        if chunk_id not in rrf_scores:
            rrf_scores[chunk_id] = 0

        rrf_scores[chunk_id] += 1 / (RRF_K + rank) #text RRF formula
        chunk_lookup[chunk_id] = chunk
        rank += 1

    #Vector search contribution
    rank = 1
    for chunk in vector_results:
        chunk_id = chunk["id"]

        if chunk_id not in rrf_scores:
            rrf_scores[chunk_id] = 0

        rrf_scores[chunk_id] += 1 /(RRF_K + rank)
        chunk_lookup[chunk_id] = chunk
        rank += 1
    
    ranked_chunks = []
    for chunk_id, score in rrf_scores.items():
        chunk = chunk_lookup[chunk_id].copy()
        chunk["rrf_score"] = score
        ranked_chunks.append(chunk)

    ranked_chunks.sort(
        key=lambda chunk: chunk["rrf_score"],
        reverse=True,
    )

    return ranked_chunks[:top_k]

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "how do I send a request"
    results = rrf(query)

    for result in results:
        print(f"{result['rrf_score']:.5f}  {result['id']}")