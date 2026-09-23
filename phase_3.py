import os
import warnings
import logging

import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma

# LangChain 1.x
import langchain_classic.chains


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

st.set_page_config(
    page_title="Ask Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Ask Chatbot!")


# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------
# Vector Store
# ---------------------------------------------------------

@st.cache_resource
def get_vectorstore():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    pdf_name = os.path.join(BASE_DIR, "reflexion.pdf")

    if not os.path.exists(pdf_name):
        raise FileNotFoundError(
            f"PDF file not found: {pdf_name}"
        )

    loader = PyPDFLoader(pdf_name)
    documents = loader.load()

    if not documents:
        raise ValueError("No content could be extracted from the PDF.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No text chunks were created from the PDF.")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vectorstore
# ---------------------------------------------------------
# User Input
# ---------------------------------------------------------

prompt = st.chat_input("Pass your prompt here")


if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # -----------------------------------------------------
    # Groq LLM
    # -----------------------------------------------------

    groq_api_key = os.environ.get("GROQ_API_KEY")

    if not groq_api_key:
        st.error(
            "GROQ_API_KEY is not configured. "
            "Please set your Groq API key in the environment."
        )
        st.stop()


    model = "openai/gpt-oss-20b"

    groq_chat = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model,
        temperature=0
    )


    # -----------------------------------------------------
    # RAG
    # -----------------------------------------------------

    try:

        vectorstore = get_vectorstore()

        if vectorstore is None:
            st.error("Failed to create vector store.")
            st.stop()


        # Create retriever
        retriever = vectorstore.as_retriever(
            search_kwargs={
                "k": 3
            }
        )


        # Create Retrieval QA chain
        chain = langchain_classic.chains.RetrievalQA.from_chain_type(
            llm=groq_chat,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )


        # Ask question
        result = chain.invoke(
            {
                "query": prompt
            }
        )


        # Extract answer
        response = result["result"]


        # -------------------------------------------------
        # Display response
        # -------------------------------------------------

        with st.chat_message("assistant"):
            st.markdown(response)


        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )


    except Exception as e:

        st.error(
            f"Error while processing your question:\n\n{str(e)}"
        )