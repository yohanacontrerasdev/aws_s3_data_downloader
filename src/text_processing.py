import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from src import config

# Load environment variables
load_dotenv()

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Use the VECTORSTORE_PATH path from config.py
VECTORSTORE_PATH = config.VECTORSTORE_PATH

def get_text_chunks(text, chunk_size=1000, chunk_overlap=200):
  text_splitter = CharacterTextSplitter(
    separator=" ",
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
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
  # Generate the text fragments
  text_chunks = get_text_chunks(contenido)

  # Create the embeddings and the vectorstore
  vectorstore = get_vectorstore(text_chunks)

  # Save the vectorstore to disk
  save_vectorstore(vectorstore, VECTORSTORE_PATH)
