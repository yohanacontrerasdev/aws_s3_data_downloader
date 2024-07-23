import os
from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from src import config  # Importar el archivo de configuración

# Cargar las variables de entorno
load_dotenv()

# Obtener la API key de OpenAI desde las variables de entorno
openai_api_key = os.getenv('OPENAI_API_KEY')

# Utilizar la ruta VECTORSTORE_PATH desde config.py
VECTORSTORE_PATH = config.VECTORSTORE_PATH


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=10000,
        chunk_overlap=2000,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def save_vectorstore(vectorstore, path):
    if not os.path.exists(path):
        os.makedirs(path)
    vectorstore.save_local(path)

def load_vectorstore(path):
    return FAISS.load_local(path, embeddings=OpenAIEmbeddings(openai_api_key=openai_api_key), allow_dangerous_deserialization=True)

def create_and_save_vectorstore(contenido):
    # Generar los fragmentos de texto
    text_chunks = get_text_chunks(contenido)

    # Crear los embeddings y el vectorstore
    vectorstore = get_vectorstore(text_chunks)

    # Guardar el vectorstore en el disco
    save_vectorstore(vectorstore, VECTORSTORE_PATH)
