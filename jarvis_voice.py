# from brain.llm_loader import query_llm
# from voice.stt import listen
# from voice.tts import speak
# from memory.vector_store import (
#     set_fact,
#     get_fact,
#     save_chat,
#     recall_chat,
#     process_memory
# )

# try:
#     from retrieval.search_engine import search_web
#     from retrieval.web_parser import fetch_article
#     INTERNET_ENABLED = True
# except:
#     INTERNET_ENABLED = False


# EXIT_PHRASES = [
#     "shut down", "turn off", "exit", "stop jarvis", "bye", "goodbye",
#     "बंद हो जाओ", "बंद करो", "ختم کرو"
# ]


# # =========================
# # SMART LANGUAGE DETECTOR
# # =========================

# def detect_language(text):
#     if any("\u0900" <= c <= "\u097F" for c in text):
#         return "hindi"   # works for Hindi + Marathi
#     return "english"


# # =========================
# # NATURAL LANGUAGE PROMPT
# # =========================

# def language_personality(lang):
#     if lang == "hindi":
#         return """
# You are a native Hindi speaker.
# Think in Hindi.
# Use natural Indian expressions.
# Speak like a real person from India.
# Do NOT translate from English.
# """
#     if lang == "urdu":
#         return """
# You are a native Urdu speaker.
# Think in Urdu.
# Use natural conversational Urdu.
# Sound polite and fluent.
# Do NOT translate from English.
# """
#     return """
# You are a native English speaker.
# Think naturally in English.
# Speak friendly and clear.
# """


# # =========================
# # MAIN INTELLIGENCE
# # =========================

# def jarvis_think(user_input):

#     memory_update = process_memory(user_input)
#     if memory_update:
#         return memory_update

#     name = get_fact("name")
#     memories = recall_chat(user_input)

#     context = ""

#     if name:
#         context += f"\nUser name: {name}\n"

#     if memories:
#         context += "\nRelevant memory:\n" + "\n".join(memories)

#     if INTERNET_ENABLED and any(x in user_input.lower() for x in ["who", "what", "latest", "news", "ceo"]):
#         try:
#             links = search_web(user_input)
#             if links:
#                 article = fetch_article(links[0])
#                 context += f"\nWeb info:\n{article[:800]}"
#         except:
#             pass

#     lang = detect_language(user_input)
#     personality = language_personality(lang)

#     final_prompt = f"""
# {personality}

# You are Jarvis — a smart personal assistant.

# User said:
# {user_input}

# Context:
# {context}

# Respond naturally like a native speaker.
# """

#     response = query_llm(final_prompt)

#     save_chat(f"User: {user_input}")
#     save_chat(f"Jarvis: {response}")

#     return response


# # =========================
# # VOICE LOOP
# # =========================

# def jarvis_voice():

#     speak("Jarvis online. How can I help you?")

#     while True:
#         user_input = listen()

#         if not user_input:
#             continue

#         print("You:", user_input)

#         if any(p in user_input.lower() for p in EXIT_PHRASES):
#             speak("Shutting down. Goodbye.")
#             print("🛑 Jarvis stopped.")
#             break

#         response = jarvis_think(user_input)

#         print("Jarvis:", response)
#         speak(response)


# if __name__ == "__main__":
#     jarvis_voice()

from brain.llm_loader import query_llm
from voice.stt import listen
from voice.tts import speak
from memory.vector_store import (
    get_fact,
    save_chat,
    recall_chat,
    process_memory
)

try:
    from retrieval.search_engine import search_web
    from retrieval.web_parser import fetch_article
    INTERNET_ENABLED = True
except:
    INTERNET_ENABLED = False


EXIT_PHRASES = [
    "shut down", "turn off", "exit", "stop jarvis", "bye", "goodbye",
    "बंद हो जाओ", "بند کرو", "ختم کرو"
]


# =========================
# CORE INTELLIGENCE
# =========================

def jarvis_think(user_input):

    # ---- WRITE MEMORY ----
    memory_reply = process_memory(user_input)
    if memory_reply:
        return memory_reply

    # ---- READ MEMORY ----
    name = get_fact("name")
    memories = recall_chat(user_input)

    context_lines = []

    if name:
        context_lines.append(f"User name is {name}.")

    if memories:
        context_lines.extend(memories)

    # ---- INTERNET ----
    if INTERNET_ENABLED and any(w in user_input.lower() for w in ["who", "what", "latest", "news", "ceo"]):
        try:
            links = search_web(user_input)
            if links:
                article = fetch_article(links[0])
                if article:
                    context_lines.append(article[:600])
        except:
            pass

    # ---- BUILD FINAL INPUT (NO SYSTEM PROMPT HERE) ----
    full_input = ""

    if context_lines:
        full_input += "Context:\n" + "\n".join(context_lines) + "\n\n"

    full_input += user_input

    response = query_llm(full_input)

    save_chat(f"User: {user_input}")
    save_chat(f"Jarvis: {response}")

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