# --------------------------------
# Memory Utilities
# --------------------------------

import chromadb


# --------------------------------
# Connect to existing Chroma DB
# --------------------------------

client = chromadb.PersistentClient(path="chroma_storage")

collection = client.get_or_create_collection(
    name="memory_collection"
)


# --------------------------------
# List all memories
# --------------------------------

def list_memories():

    data = collection.get()

    docs = data["documents"]

    if not docs:
        return []

    return docs


# --------------------------------
# Delete memory by index
# --------------------------------

def forget_memory(index: int):

    data = collection.get()

    ids = data["ids"]
    docs = data["documents"]

    if index < 0 or index >= len(ids):
        return "Invalid memory index"

    deleted = docs[index]

    collection.delete(ids=[ids[index]])

    return f"Deleted memory: {deleted}"


# --------------------------------
# Clear entire memory
# --------------------------------

def clear_all_memory():

    global collection

    try:
        client.delete_collection("memory_collection")
    except:
        pass

    collection = client.get_or_create_collection(
        name="memory_collection"
    )

    return "All memories cleared"