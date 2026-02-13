def build_prompt(user_query, memory_context, web_context):
    return f"""
You are Jarvis, an intelligent multilingual assistant.

Memory Context:
{memory_context}

Live Web Context:
{web_context}

User Query:
{user_query}

Respond clearly and in the same language as the user.
"""