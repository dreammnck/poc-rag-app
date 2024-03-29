from fastapi import UploadFile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..utils import predictor
from ..config import config
from langchain_community.vectorstores import Chroma


def upload(file: UploadFile):
    try:
        with open(f'{file.filename}', 'wb') as f:
            f.write(file.file.read())
        return add_to_vector_db(file.filename)
    except Exception as e:
        return e

def add_to_vector_db(filename: str):
    try:
        loader = PyPDFLoader(f'{os.getcwd()}/{filename}')
        documents = loader.load()
    
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)
        Chroma.from_documents(docs,  predictor.embedding_model, client=predictor.chroma_client, collection_name=config.Settings().vector_db_collection_name)
    except Exception as e:
        return e
    finally:
        os.remove(filename)
        
    return "success"