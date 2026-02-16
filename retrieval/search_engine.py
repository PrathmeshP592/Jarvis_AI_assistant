# from duckduckgo_search import DDGS

# def search_web(query, max_results=3):
#     with DDGS() as ddgs:
#         results = list(ddgs.text(query, max_results=max_results))
#     return [r["href"] for r in results]

from ddgs import DDGS

def search_web(query, max_results=3):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    return [r["href"] for r in results]