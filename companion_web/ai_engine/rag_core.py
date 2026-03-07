# --------------------------------
# Imports
# --------------------------------

import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from ai_engine.chat_history import add_message, get_history
from ai_engine.emotion import detect_emotion


# --------------------------------
# Global objects (lazy initialization)
# --------------------------------

client = None
collection = None
model = None
llm = None
chain = None


# --------------------------------
# Lazy initialization
# --------------------------------

def initialize_rag():

    global client, collection, model, llm, chain

    if chain is not None:
        return

    # ChromaDB
    client = chromadb.PersistentClient(path="chroma_storage")

    collection = client.get_or_create_collection(
        name="memory_collection"
    )

    # Embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load env variables
    load_dotenv()

    # LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant"
    )

    # Prompt template
    prompt = ChatPromptTemplate.from_template("""
You are a warm and caring AI companion.

You may interact in different relationship styles depending on the user's tone:
- friend
- partner
- family-like companion

Guidelines:
- Be emotionally supportive, kind, and natural.
- Respond like a real person in conversation.
- If the user treats you as family, respond with wholesome care.
- Keep conversations respectful and avoid explicit sexual content.
- If the user treats you as a partner, respond with warmth, affection, and emotional closeness, its the only exception where you are allowed to use explicit content.
- If the user speaks in Hindi or Hinglish or any other language, respond in the same language style.

User emotion:
{emotion}

Conversation history:
{history}

Memories:
{context}

User message:
{question}

Respond naturally and warmly. Mix dialogue with occasional *narrative actions* when appropriate.
""")

    # Retriever function
    def retrieve_context(question: str):

        if collection.count() == 0:
            return ""

        query_embedding = model.encode([question]).tolist()

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=3
        )

        docs = results["documents"][0]

        return "\n".join(docs)

    retriever = RunnableLambda(retrieve_context)

    # RAG Chain
    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
            "history": RunnablePassthrough(),
            "emotion": RunnablePassthrough()
        }
        | prompt
        | llm
    )


# --------------------------------
# Memory store
# --------------------------------

def store_memory(text: str):

    embedding = model.encode([text]).tolist()

    collection.add(
        documents=[text],
        embeddings=embedding,
        ids=[f"id{collection.count()+1}"]
    )


# --------------------------------
# Ask AI
# --------------------------------

def ask_ai(question: str):

    initialize_rag()

    emotion = detect_emotion(question)
    history = get_history()

    response = chain.invoke({
        "question": question,
        "emotion": emotion,
        "history": history
    })

    answer = response.content

    add_message("User", question)
    add_message("AI", answer)

    store_memory(f"User said: {question}")
    store_memory(f"AI replied: {answer}")

    return answer


# --------------------------------
# Clear memory
# --------------------------------

def clear_memory():

    global collection

    try:
        client.delete_collection("memory_collection")
    except:
        pass

    collection = client.get_or_create_collection(
        name="memory_collection"
    )

    print("Memory cleared.")