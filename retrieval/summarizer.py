from brain.llm_loader import query_llm

def summarize(text):
    prompt = f"Summarize the following content:\n{text[:3000]}"
    return query_llm(prompt)