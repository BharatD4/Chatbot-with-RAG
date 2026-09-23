# 🤖 Chatbot with RAG

An AI-powered document question-answering chatbot built using **Retrieval-Augmented Generation (RAG)**.

This project allows users to interact with a PDF knowledge base through a conversational chat interface. The application extracts content from the document, splits it into meaningful chunks, generates vector embeddings, retrieves relevant information using semantic similarity, and uses a Large Language Model to generate the final response.

## 🚀 Live Demo

🔗 **Live Application:**  
https://chatbot-with-rag-frdahwrz767ug5gacblycj.streamlit.app/

🔗 **GitHub Repository:**  
https://github.com/BharatD4/Chatbot-with-RAG

---

## 📌 Project Overview

Traditional chatbots generally depend only on the knowledge already available inside an LLM.

This project demonstrates how **Retrieval-Augmented Generation (RAG)** can be used to connect an LLM with an external knowledge source.

The application uses a PDF document as its knowledge base.

When a user asks a question:

1. The question is processed.
2. Relevant document chunks are retrieved from the vector database.
3. The retrieved context is provided to the LLM.
4. The LLM generates a natural-language response.

This approach helps build applications where responses can be based on domain-specific documents rather than relying only on the model's pre-trained knowledge.

---

## ✨ Features

- 📄 **PDF Knowledge Base**
  - Load and process PDF documents using PyPDF.

- 🔎 **Semantic Search**
  - Retrieve relevant document content using vector embeddings.

- 🧠 **Retrieval-Augmented Generation**
  - Combines document retrieval with LLM-based response generation.

- 🤖 **Groq LLM Integration**
  - Uses Groq's API for fast LLM inference.

- 💬 **Interactive Chat Interface**
  - Built with Streamlit's conversational UI.

- 🗂️ **Vector Database**
  - ChromaDB is used to store and retrieve document embeddings.

- 🔤 **Hugging Face Embeddings**
  - Uses Sentence Transformers for semantic document representation.

- ⚡ **Cached Vector Store**
  - Streamlit resource caching reduces unnecessary document processing.

- 🔐 **Secure API Configuration**
  - API credentials are managed through environment variables and Streamlit Secrets.

- ☁️ **Cloud Deployment**
  - Deployed using Streamlit Community Cloud.

---

## 🏗️ System Architecture

```text
                    ┌───────────────────┐
                    │    PDF Document   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   PyPDFLoader     │
                    │  Document Loader  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  Text Splitter    │
                    │ RecursiveCharacter│
                    │    TextSplitter   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Hugging Face      │
                    │ Embeddings        │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     ChromaDB      │
                    │  Vector Store     │
                    └─────────┬─────────┘
                              │
                    User Question
                              │
                              ▼
                    ┌───────────────────┐
                    │ Similarity Search │
                    │    Top-K Chunks   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     Groq LLM      │
                    │ Response Generator│
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  Final Response   │
                    │  Streamlit Chat   │
                    └───────────────────┘
