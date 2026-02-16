import subprocess

OLLAMA_PATH = r"C:\Users\prathamesh.p\AppData\Local\Programs\Ollama\ollama.exe"
MODEL_NAME = "phi3"

def query_llm(user_prompt: str) -> str:

    system_prompt = """
You are Jarvis, a smart, calm, minimal AI assistant.

Rules:
- Reply in the SAME language the user used.
- Keep responses short and natural.
- Do NOT be dramatic.
- Do NOT add motivational lines.
- Do NOT explain unnecessary details.
- If Hindi/Marathi/Urdu is spoken, reply fluently in that language.
- If English is spoken, reply in clear simple English.
"""

    final_prompt = system_prompt + "\nUser: " + user_prompt + "\nJarvis:"

    result = subprocess.run(
        [OLLAMA_PATH, "run", MODEL_NAME],
        input=final_prompt,
        text=True,
        encoding="utf-8",
        capture_output=True
    )

    return result.stdout.strip()