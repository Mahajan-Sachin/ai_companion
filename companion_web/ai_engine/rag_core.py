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
# 1. Setup Persistent ChromaDB
# --------------------------------

client = chromadb.PersistentClient(path="chroma_storage")

collection = client.get_or_create_collection(
    name="memory_collection"
)


# --------------------------------
# 2. Embedding Model
# --------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------
# 3. Memory Store Function
# --------------------------------

def store_memory(text: str):

    embedding = model.encode([text]).tolist()

    collection.add(
        documents=[text],
        embeddings=embedding,
        ids=[f"id{collection.count()+1}"]
    )


# --------------------------------
# 4. Retrieval Function
# --------------------------------

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


# --------------------------------
# 5. Load Groq LLM
# --------------------------------

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)


# --------------------------------
# 6. Prompt Template
# --------------------------------

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
-If the user speaks in Hindi or Hinglish or any other language, respond in the same language style.

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

# --------------------------------
# 7. LCEL RAG Pipeline
# --------------------------------

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
# 8. Public Function
# --------------------------------

def ask_ai(question: str):

    # detect emotion
    emotion = detect_emotion(question)

    # get short-term chat history
    history = get_history()

    # run chain
    response = chain.invoke({
        "question": question,
        "emotion": emotion,
        "history": history
    })

    answer = response.content

    # update short-term history
    add_message("User", question)
    add_message("AI", answer)

    # store long-term memory
    store_memory(f"User said: {question}")
    store_memory(f"AI replied: {answer}")

    return answer


# --------------------------------
# 9. Clear Memory
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