from brain.llm_loader import query_llm
from voice.stt import listen
from voice.tts import speak
from memory.vector_store import (
    get_fact,
    process_memory
)

from learning.behavior import (
    analyze_interaction,
    build_behavior_context
)

EXIT_PHRASES = [
    "shut down",
    "turn off",
    "exit",
    "stop jarvis",
    "bye",
    "goodbye"
]


# =========================
# CORE INTELLIGENCE
# =========================

def jarvis_think(user_input):

    text = user_input.lower()

    # ---------- SAVE FACT MEMORY ----------
    memory_reply = process_memory(user_input)
    if memory_reply:
        return memory_reply

    # ---------- DIRECT MEMORY QUESTIONS ----------
    if "my name" in text or "what is my name" in text:
        name = get_fact("name")
        if name:
            return f"Your name is {name}."
        return "I do not have your name saved yet."

    # ---------- LIGHT CONTEXT ----------
    name = get_fact("name")
    if name:
        prompt = f"The user's name is {name}. {user_input}"
    else:
        prompt = user_input

    # ---------- LEARNING CONTEXT ----------
    behavior_context = build_behavior_context()

    final_prompt = behavior_context + "\n" + prompt

    # ---------- LLM ----------
    response = query_llm(final_prompt)

    # ---------- LEARN FROM THIS ----------
    analyze_interaction(user_input, response)

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

        # response = jarvis_think(user_input)

        # print("Jarvis:", response)
        # speak(response)
        
        response = jarvis_think(user_input)
        print("Jarvis:", response)

        # Pause listening while speaking
        speak(response)


if __name__ == "__main__":
    jarvis_voice()