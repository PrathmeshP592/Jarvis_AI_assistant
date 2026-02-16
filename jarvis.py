# from brain.llm_loader import query_llm

# def jarvis():
#     print("\n🤖 Jarvis is online. Type 'exit' to quit.\n")

#     while True:
#         user_input = input("You: ")

#         if user_input.lower() in ["exit", "quit"]:
#             print("Jarvis: Shutting down. Goodbye!")
#             break

#         response = query_llm(user_input)
#         print(f"\nJarvis: {response}\n")


# if __name__ == "__main__":
#     jarvis()

# from brain.llm_loader import query_llm
# from brain.memory import save_memory, recall_memory


# def jarvis():
#     print("\n🤖 Jarvis is online with memory enabled. Type 'exit' to quit.\n")

#     while True:
#         user_input = input("You: ")

#         if user_input.lower() in ["exit", "quit"]:
#             print("Jarvis: Shutting down. Goodbye!")
#             break

#         # Retrieve relevant past memories
#         past_memories = recall_memory(user_input)

#         context = ""
#         if past_memories:
#             context = "Previous related information:\n"
#             context += "\n".join(past_memories) + "\n\n"

#         # Combine memory + current input
#         full_prompt = context + user_input

#         response = query_llm(full_prompt)

#         # Save conversation
#         save_memory(f"User: {user_input}")
#         save_memory(f"Jarvis: {response}")

#         print(f"\nJarvis: {response}\n")


# if __name__ == "__main__":
#     jarvis()



SYSTEM_CONTEXT = """
You are Jarvis, a local AI assistant running on the user's computer.

You have:
- A long-term memory stored in a vector database (Chromadb)
- Internet access via web search
- A local LLM (Mistral) running through Ollama

When user asks about memory:
Explain that you store information in a local vector database.

When user asks about learning:
Explain you don't retrain but recall stored memories.

When user asks about code:
Explain you run locally in Python using Ollama.
"""

from brain.llm_loader import query_llm
from brain.memory import save_memory, recall_memory
from retrieval.search_engine import search_web
from retrieval.web_parser import fetch_article


def jarvis():
    print("\n🤖 Jarvis online with memory + internet. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Jarvis: Shutting down.")
            break

        # ===== 1. MEMORY FIRST (always) =====
        memories = recall_memory(user_input)
        context = ""

        if memories:
            context = "Past memory:\n" + "\n".join(memories) + "\n\n"

        # ===== 2. DECIDE IF WEB IS NEEDED =====
        use_web = False
        if not memories:
            use_web = any(word in user_input.lower() for word in [
                "who", "what", "latest", "news", "explain", "how"
            ])

        # ===== 3. FETCH INTERNET INFO IF NEEDED =====
        if use_web:
            links = search_web(user_input)

            web_text = ""
            for link in links[:2]:
                article = fetch_article(link)
                if article:
                    web_text += article[:1500] + "\n\n"

            prompt = (
                context +
                "Use this real-world information to answer:\n" +
                web_text +
                "Question: " + user_input
            )
        else:
            prompt = context + user_input

        # ===== 4. ASK LLM =====
        response = query_llm(prompt)

        # ===== 5. SAVE MEMORY =====
        save_memory(f"User: {user_input}")
        save_memory(f"Jarvis: {response}")

        print(f"\nJarvis: {response}\n")


if __name__ == "__main__":
    jarvis()