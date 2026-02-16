import subprocess

OLLAMA_PATH = r"C:\Users\prathamesh.p\AppData\Local\Programs\Ollama\ollama.exe"
MODEL_NAME = "llama3"


SYSTEM_PROMPT = """You are Jarvis, a helpful AI assistant.

Rules:
- Reply ONLY in English.
- Be concise and natural.
- Answer directly.
- No roleplay.
- No example conversations.
- No motivational lines.
- No unnecessary explanations.
"""


def query_llm(user_prompt: str) -> str:
    final_prompt = f"{SYSTEM_PROMPT}\nUser: {user_prompt}\nJarvis:"

    result = subprocess.run(
        [OLLAMA_PATH, "run", MODEL_NAME],
        input=final_prompt,
        text=True,
        encoding="utf-8",
        capture_output=True
    )

    return result.stdout.strip()


# Quick test
if __name__ == "__main__":
    print(query_llm("Hello Jarvis, are you online?"))