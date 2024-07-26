import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Establecer la clave de API como variable de entorno
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

VECTORSTORE_PATH = "vectorstore/"

def load_vectorstore(path):
    return FAISS.load_local(path, embeddings=OpenAIEmbeddings(), allow_dangerous_deserialization=True)

def get_conversation_chain(vectorstore):
    template = """
    Your template here
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        condense_question_prompt=prompt,
        return_source_documents=True,
        output_key='source_documents'  # Explicitly set the output key for the source documents
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    st.session_state.retrieved_docs = response['source_documents']
    display_retrieved_documents()

def display_retrieved_documents():
    st.subheader("Documentos relevantes:")
    for doc in st.session_state.retrieved_docs:
        st.write(doc.page_content)  # Mostrar el texto del documento
        # También podrías mostrar otros metadatos del documento si están disponibles

def main():
    st.set_page_config(page_title="FinancialChatbot", page_icon="🤖")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state or st.session_state.conversation is None:
        st.session_state.conversation = None
        st.session_state.chat_history = []
        st.session_state.retrieved_docs = []

    st.header("Chat with NASDAQ PDFs :books:")
    user_question = st.chat_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    # Cargar el vectorstore desde el disco
    if os.path.exists(VECTORSTORE_PATH):
        vectorstore = load_vectorstore(VECTORSTORE_PATH)
        st.session_state.conversation = get_conversation_chain(vectorstore)
    else:
        st.error("Vector store not found. Please generate it first.")

if __name__ == '__main__':
    main()