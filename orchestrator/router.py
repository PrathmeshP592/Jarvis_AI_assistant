from memory.vector_store import retrieve_memory, store_memory
from retrieval.search_engine import search_web
from retrieval.web_parser import extract_text
from retrieval.summarizer import summarize
from brain.prompt_engine import build_prompt
from brain.llm_loader import query_llm
from orchestrator.decision_logic import needs_web_search

def handle_query(query: str):

    memory_context = "\n".join(retrieve_memory(query))

    web_context = ""
    if needs_web_search(query):
        urls = search_web(query)
        content = [extract_text(u) for u in urls]
        web_context = summarize("\n".join(content))

    prompt = build_prompt(query, memory_context, web_context)

    response = query_llm(prompt)

    if len(query) > 20:
        store_memory(query + " -> " + response)

    return response