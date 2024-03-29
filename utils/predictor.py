from functools import lru_cache
from ..config import config
import chromadb
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

@lru_cache
def get_settings():
    return config.Settings()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def init_chroma(settings: config.Settings):
    return chromadb.HttpClient(host = settings.vector_db_url, port = settings.vector_db_port)

def init_embedding_model(settings: config.Settings):
    return GoogleGenerativeAIEmbeddings(model=settings.embedded_model_name)

def init_rag_retriever(settings: config.Settings):
    
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"]  = settings.google_api_key
        
    http_client = chromadb.HttpClient(host = settings.vector_db_url, port = settings.vector_db_port)
    embedding_function = GoogleGenerativeAIEmbeddings(model=settings.embedded_model_name)
    db = Chroma(
    client=http_client,
    collection_name=settings.vector_db_collection_name,
    embedding_function=embedding_function,
    )

    prompt = """You are an assistant. You need to answer the question related to the question. 
                Given below is the context and question of the user.
                context = {context}
                question = {question}
            """

    prompt = ChatPromptTemplate.from_template(prompt)

    llm = ChatGoogleGenerativeAI(model=settings.chat_model_name, google_api_key=settings.google_api_key)
    retriever = db.as_retriever()

    rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
    )
    
    return rag_chain

rag_predictor = init_rag_retriever(get_settings())
chroma_client = init_chroma(get_settings())
embedding_model = init_embedding_model(get_settings())