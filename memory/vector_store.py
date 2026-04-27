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
    import re

    text = user_input.strip()

    match = re.search(r"my name is\s+([a-zA-Z]+)", text, re.IGNORECASE)

    if match:
        name = match.group(1).capitalize()
        set_fact("name", name)
        return f"I will remember your name as {name}."

    return None