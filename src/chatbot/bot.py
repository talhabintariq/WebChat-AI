import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
# from bs4 import BeautifulSoup as Soup
import chromadb

def get_vectorstore_from_url(url):
    # Load and split the webpage content into manageable chunks
    loader = RecursiveUrlLoader(
        url=url,
        max_depth=1,
    )
    document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]  # Optimized splitting
    )
    document_chunks = text_splitter.split_documents(document)
    
    # Initialize persistent Chroma vector database with OpenAI embeddings
    client = chromadb.PersistentClient(path="./db/chroma_db")
    embedding_function = OpenAIEmbeddings()
    vector_store = Chroma(
        client=client,
        embedding_function=embedding_function,
        collection_name="my_collection"
    )

    vector_store.add_documents(document_chunks)
    return vector_store

def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI()
    retriever = vector_store.as_retriever()
    
    # Create a prompt that uses conversation history to generate relevant search queries
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation"),
    ])
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain

def get_conversational_rag_chain(retreiver_chain):
    llm = ChatOpenAI()
    
    # Setup RAG prompt template combining context, chat history, and user input
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    
    # Create and combine document processing chains for RAG
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt) 
    return create_retrieval_chain(retreiver_chain, stuff_documents_chain)

def get_response(user_input):
    # Generate response using RAG pipeline with conversation history
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    
    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_input,
    })
    return response['answer'] 