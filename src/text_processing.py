import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

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
  return FAISS.load_local(path, embeddings=OpenAIEmbeddings(), allow_dangerous_deserialization=True)

def create_and_save_vectorstore(contenido, path):
  # Generate the text chunks
  text_chunks = get_text_chunks(contenido)

  # Creaeate the embeddings and the vectorstore
  vectorstore = get_vectorstore(text_chunks)

  # save the vectorstore in the disk
  save_vectorstore(vectorstore, path)
