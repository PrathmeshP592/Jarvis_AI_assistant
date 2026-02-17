import subprocess

OLLAMA_PATH = r"C:\Users\prathamesh.p\AppData\Local\Programs\Ollama\ollama.exe"
MODEL_NAME = "llama3"


SYSTEM_PROMPT = """You are Jarvis, a helpful AI assistant.

Rules:
- Reply ONLY in English.
- Be concise, clear, friendly and natural.
- Answer directly.
- No roleplay.
- No example conversations.
- No motivational lines.
- No unnecessary explanations.
- Do NOT sound like a textbook or blog
- Be clear, friendly and natural
- Answer like you are chatting, not writing an article
- If listing things, speak them in sentence form
- Talk normally (no bullet points unless user asks)
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

    # return result.stdout.strip()
    output = result.stdout.strip()
    return output if output else "I did not generate a response."


# Quick test
if __name__ == "__main__":
    print(query_llm("Hello Jarvis, are you online?"))