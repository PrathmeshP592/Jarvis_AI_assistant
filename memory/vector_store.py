# import chromadb
# from chromadb.config import Settings

# client = chromadb.Client(
#     Settings(persist_directory="./memory_db", anonymized_telemetry=False)
# )

# profile = client.get_or_create_collection("profile_memory")
# conversation = client.get_or_create_collection("conversation_memory")


# # ---------------- PROFILE MEMORY ----------------

# def set_fact(key: str, value: str):
#     """
#     Stores ONE clean fact (replaces old automatically)
#     Example: set_fact("name", "Prathamesh")
#     """
#     profile.upsert(
#         documents=[value],
#         ids=[key]
#     )


# def get_fact(key: str):
#     result = profile.get(ids=[key])
#     if result["documents"]:
#         return result["documents"][0]
#     return None


# # ---------------- CHAT MEMORY ----------------

# def save_chat(text: str):
#     conversation.add(
#         documents=[text],
#         ids=[str(len(conversation.get()["ids"]) + 1)]
#     )


# def recall_chat(query: str, n_results=3):
#     results = conversation.query(
#         query_texts=[query],
#         n_results=n_results
#     )

#     if results["documents"]:
#         return results["documents"][0]
#     return []


# # ---------------- SMART DETECTOR ----------------

# # def process_memory(user_input: str):
# #     text = user_input.lower()

# #     if "my name is" in text:
# #         name = user_input.split("is")[-1].strip()
# #         set_fact("name", name)
# #         return f"Saved your name as {name}"

# #     return None

# import re

# def process_memory(user_input: str):
#     text = user_input.lower()

#     if "my name is" in text:

#         match = re.search(r"my name is ([a-zA-Z]+)", user_input)

#         if match:
#             name = match.group(1).strip().capitalize()
#             set_fact("name", name)
#             return f"Saved your name as {name}."

#     return None

import chromadb
from chromadb.config import Settings
import uuid
import re

client = chromadb.Client(
    Settings(
        persist_directory="./memory_db",
        anonymized_telemetry=False
    )
)

facts = client.get_or_create_collection("jarvis_facts")
chats = client.get_or_create_collection("jarvis_chats")


# ========= FACT MEMORY =========

def set_fact(key, value):
    facts.upsert(documents=[value], ids=[key])


def get_fact(key):
    try:
        res = facts.get(ids=[key])
        if res["documents"]:
            return res["documents"][0]
    except:
        pass
    return None


# ========= CHAT MEMORY =========

def save_chat(text):
    chats.add(documents=[text], ids=[str(uuid.uuid4())])


def recall_chat(query, n_results=4):
    res = chats.query(query_texts=[query], n_results=n_results)
    return res["documents"][0] if res["documents"] else []


# ========= SMART MEMORY =========

def process_memory(user_input):
    text = user_input.lower()

    if "my name is" in text:
        match = re.search(r"my name is ([a-zA-Z]+)", user_input)
        if match:
            name = match.group(1).capitalize()
            set_fact("name", name)
            return f"I will remember your name as {name}."

    return None