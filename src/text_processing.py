import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
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
    return FAISS.load_local(path, embeddings=OpenAIEmbeddings(openai_api_key=openai_api_key), allow_dangerous_deserialization=True)

def create_and_save_vectorstore(contenido, path):
    # Generate the text chunks
    text_chunks = get_text_chunks(contenido)

    # Create the embeddings and the vectorstore
    vectorstore = get_vectorstore(text_chunks)

    # Save the vectorstore to disk
    save_vectorstore(vectorstore, path)

# Define the path where you want to save the vectorstore
VECTORSTORE_PATH = "vectorstore/"

# Create and save the vectorstore
cleaned_text = "Aquí va tu texto limpio"  # Asegúrate de definir cleaned_text con el contenido apropiado
create_and_save_vectorstore(cleaned_text, VECTORSTORE_PATH)
