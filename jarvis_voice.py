from brain.llm_loader import query_llm
from voice.stt import listen
from voice.tts import speak
from memory.vector_store import (
    get_fact,
    process_memory
)

EXIT_PHRASES = [
    "shut down", "turn off", "exit", "stop jarvis", "bye", "goodbye"
]


# =========================
# CORE INTELLIGENCE
# =========================

def jarvis_think(user_input):

    text = user_input.lower()

    # ---- SAVE FACTS (like name) ----
    memory_reply = process_memory(user_input)
    if memory_reply:
        return memory_reply

    # ---- DIRECT MEMORY QUESTIONS ----
    if "my name" in text or "what is my name" in text:
        name = get_fact("name")
        if name:
            return f"Your name is {name}."
        else:
            return "I do not have your name saved yet."

    # ---- INCLUDE NAME PASSIVELY ----
    name = get_fact("name")
    if name:
        user_input = f"My name is {name}. {user_input}"

    # ---- CLEAN LLM CALL ----
    response = query_llm(user_input)

    return response


# =========================
# VOICE LOOP
# =========================

def jarvis_voice():

    speak("Jarvis online.")

    while True:

        user_input = listen()

        if not user_input:
            continue

        print("You:", user_input)

        if any(p in user_input.lower() for p in EXIT_PHRASES):
            speak("Shutting down.")
            print("🛑 Jarvis stopped.")
            break

        response = jarvis_think(user_input)

        print("Jarvis:", response)
        speak(response)


if __name__ == "__main__":
    jarvis_voice()