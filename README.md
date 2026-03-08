# AI Companion – Retrieval Augmented Conversational AI

AI Companion is a context-aware conversational AI system that simulates emotionally intelligent dialogue. The system uses a Retrieval-Augmented Generation (RAG) architecture to remember past conversations and generate more personalized responses over time.

The application combines a Django backend, a vector database for memory storage, and an LLM-powered response system to create a companion-style chatbot capable of multi-turn conversations.

<img width="1912" height="940" alt="image" src="https://github.com/user-attachments/assets/0cc1ae59-d557-4e22-b979-78df0cc0dbb1" />


-------

## Features

Context-aware conversational AI using Retrieval-Augmented Generation (RAG)

Long-term memory using ChromaDB vector database

Semantic search using Sentence Transformer embeddings

Emotion-aware responses using a transformer-based classifier

Short-term conversation history + long-term semantic memory

Dynamic chat interface with message bubbles, avatars, and typing simulation

Multi-language conversational support (English, Hindi, Hinglish)

------

## System Architecture

User Message

↓

Emotion Detection (Transformer Model)

↓

Semantic Retrieval from Vector Database (ChromaDB)

↓

Conversation History + Retrieved Context

↓

LLM Response Generation (Groq – Llama 3.1)

↓

Memory Storage (Vector + Chat History)


------------

## Tech Stack

### Backend

Python

Django

### AI / LLM

LangChain (LCEL)

Groq API (Llama 3.1)

Vector Database

ChromaDB

### NLP / ML

Sentence Transformers

HuggingFace Transformers

PyTorch

Scikit-learn

### Frontend

HTML

CSS

JavaScript

### Other Tools

python-dotenv

SQLite

------

## Key Concepts Implemented

Retrieval-Augmented Generation (RAG)

Semantic search using vector embeddings

Conversational memory systems

Emotion-aware dialogue generation

Context retention across multi-turn conversations

Project Structure
<img width="469" height="515" alt="image" src="https://github.com/user-attachments/assets/4bbe53b1-f495-48c9-ab91-4f4a21be8d0e" />

----------------------

## How It Works

User sends a message through the chat interface.

The system detects the user's emotional tone.

The message is converted into embeddings using Sentence Transformers.

Relevant past memories are retrieved from ChromaDB using semantic similarity.

Retrieved context + conversation history are passed to the LLM.

The LLM generates a contextual and emotionally aware response.

The interaction is stored in both short-term and long-term memory.

------------------------------------------
## Future Improvements

Streaming responses (token-by-token generation)

User profiles and persistent conversation sessions

Voice interaction support

Mobile-responsive UI

Advanced memory summarization

----------------------------------
## Author

Sachin Mahajan
