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
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
  )
  chunks = text_splitter.split_text(text)
  return chunks

def chunk_and_save(df):

  if 'Normalized Text' not in df.columns:
    raise ValueError("DataFrame must contain a 'Normalized Text' column")

  df['Text Chunks'] = df['Normalized Text'].apply(lambda text: get_text_chunks(text))

  return df

def get_vectorstore(text_chunks):
  embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
  vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
  return vectorstore

def process_and_create_vectorstore(df):
  df_with_chunks = chunk_and_save(df)
  all_text_chunks = [chunk for sublist in df_with_chunks['Text Chunks'] for chunk in sublist]
  
  vectorstore = get_vectorstore(all_text_chunks)
  
  return vectorstore

