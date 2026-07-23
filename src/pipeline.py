from retrieval.fuse import rrf
from retrieval.rerank import rerank

candidates = rrf("max_redirects", top_k=10)
final = rerank("max_redirects", candidates, top_k=5)

for r in final:
    print(f"{r['rerank_score']:.3f}  {r['id']}")