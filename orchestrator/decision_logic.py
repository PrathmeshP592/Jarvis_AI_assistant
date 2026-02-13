def needs_web_search(query: str) -> bool:
    keywords = ["latest", "today", "news", "recent", "update"]
    return any(k in query.lower() for k in keywords)