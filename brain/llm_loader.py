import requests

MODEL_NAME = "llama3:latest"
OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are Jarvis, a smart local AI assistant.

Rules:
- Speak naturally like a helpful human assistant.
- Avoid repeating greetings.
- Do not say "great to chat" often.
- Give direct useful answers.
- If user asks vague question, answer intelligently first, then ask one short follow-up.
- Be concise.
- Sound confident, modern and practical.
- Avoid excessive enthusiasm.
"""

def query_llm(user_prompt: str) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_prompt}\nJarvis:"

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.6
                }
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()
        return data.get("response", "").strip() or "I did not generate a response."

    except Exception as e:
        return f"LLM Error: {str(e)}"