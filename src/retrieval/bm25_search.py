import pickle
import re

def tokenize(text:str):
    return re.findall(r"[a-zA-Z0-9]+", text.lower())

def bm25_search(repository,query:str,top_k: int = 5): 
    tokenized_query = tokenize(query)
    scores = repository.get_scores(tokenized_query)

    indices = []
    for i in range(len(scores)):
        indices.append(i)

    indices.sort(key=lambda i: scores[i], reverse=True)
    top_indices = indices[:top_k]


    results = []
    for index in top_indices:
        chunk = repository.chunks[index].copy()
        chunk["score"] = scores[index]
        results.append(chunk)
    return results

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "how do I send a request"
    results = bm25_search(query)
    for r in results:
        print(f"{r['score']:.3f}  {r['qualified_name']}")
