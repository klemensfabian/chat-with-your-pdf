import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client
from gen_ai_hub.proxy.langchain.init_models import init_embedding_model, init_llm
from langchain_community.vectorstores import HanaDB, FAISS
from hdbcli import dbapi
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from PyPDF2 import PdfReader
from io import BytesIO
from langchain.docstore.document import Document

from config import (
    PDF_CHUNK_SIZE, 
    PDF_CHUNK_OVERLAP, 
    EMBEDDING_MODEL, 
    DB_DEFAULT,
    DB_TABLE,
    LLM_MODEL, 
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS
)

load_dotenv()

def get_pdf_text(uploaded_file):
    """
    Extracts text from a PDF file.

    Args:
        uploaded_file (file): The uploaded PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    text_parts = []
    try:
        with BytesIO(uploaded_file.read()) as pdf_stream:
            pdf_reader = PdfReader(pdf_stream)
            for page in pdf_reader.pages:
                text_parts.append(page.extract_text())
    except Exception as e:
        # Handle specific exceptions as needed and log or return an error message
        return f"An error occurred: {str(e)}"
    return ''.join(text_parts)


def get_text_chunks(text):
    """
    Splits the text into chunks.

    Args:
        text (str): The text to be split.

    Returns:
        list: List of Document objects, each representing a text chunk.
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=PDF_CHUNK_SIZE, chunk_overlap=PDF_CHUNK_OVERLAP)
        chunks = text_splitter.split_text(text)
        return [Document(page_content=chunk) for chunk in chunks]
    except Exception as e:
        raise

def get_vectorstore(pdf_pages, db_choice=DB_DEFAULT):
    """
    Creates a vector store from the PDF pages.

    Args:
        pdf_pages (list): List of Document objects representing the PDF pages.
        db_choice (str, optional): The choice of database. Defaults to DB_DEFAULT.

    Returns:
        object: The created vector store.
    """
    try:
        proxy_client = get_proxy_client("gen-ai-hub")
        embeddings = init_embedding_model(EMBEDDING_MODEL, proxy_client=proxy_client)
        
        if db_choice == "HANA":
            hana_conn = get_hana_connection()
            vectorstore = HanaDB(embedding=embeddings, connection=hana_conn, table_name=DB_TABLE)
            vectorstore.delete(filter={})
        else:  # FAISS
            vectorstore = FAISS.from_documents(pdf_pages, embeddings)
        
        vectorstore.add_documents(pdf_pages)
        return vectorstore
    except Exception as e:
        raise

def get_hana_connection():
    """
    Establishes a connection to the SAP HANA database.

    Returns:
        object: The HANA database connection object.
    """
    try:
        return dbapi.connect(
            address=os.getenv('SAP_HANA_ADDRESS'),
            port=443,
            user=os.getenv('SAP_HANA_USER'),
            password=os.getenv('SAP_HANA_PASSWORD'),
            encrypt='true'
        )
    except Exception as e:
        raise

def get_conversation_chain(vectorstore):
    """
    Creates a conversation chain for conversational retrieval.

    Args:
        vectorstore (object): The vector store.

    Returns:
        object: The conversation chain.
    """
    try:
        proxy_client = get_proxy_client("gen-ai-hub")
        llm = init_llm(LLM_MODEL, proxy_client=proxy_client, temperature=LLM_TEMPERATURE, max_tokens=LLM_MAX_TOKENS)
        
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        Keep the answer as concise as possible but with all needed information.
        {context}
        Question: {question}
        Helpful Answer:"""

        prompt = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question", "chat_history"]
        )
        
        memory = ConversationBufferMemory(
            memory_key="chat_history", 
            output_key="answer", 
            return_messages=True)
        
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 6}),
            chain_type="stuff",
            return_source_documents=True,
            memory=memory,
            verbose=False,
            combine_docs_chain_kwargs={"prompt": prompt}
        )
        return conversation_chain
    except Exception as e:
        raise

def process_pdf(uploaded_file, db_choice):
    """
    Processes the uploaded PDF file.

    Args:
        uploaded_file (file): The uploaded PDF file.
        db_choice (str): The choice of database.

    Returns:
        object: The vector store.
    """
    pdf_text = get_pdf_text(uploaded_file)
    text_chunks = get_text_chunks(pdf_text)
    return get_vectorstore(text_chunks, db_choice)