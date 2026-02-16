import chromadb
from chromadb.config import Settings

client = chromadb.Client(
    Settings(persist_directory="./memory_db", anonymized_telemetry=False)
)

collection = client.get_or_create_collection(name="jarvis_memory")


def save_memory(text: str):
    collection.add(
        documents=[text],
        ids=[str(len(collection.get()["ids"]) + 1)]
    )


def recall_memory(query: str, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    if results["documents"]:
        return results["documents"][0]
    return []