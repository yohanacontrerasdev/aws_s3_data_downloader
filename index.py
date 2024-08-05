import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

# Set the API key as an environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

VECTORSTORE_PATH = "vectorstore/"

# Initialize chat_history at the global level to persist across reruns
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def load_vectorstore(path):
    return FAISS.load_local(path, embeddings=OpenAIEmbeddings(), allow_dangerous_deserialization=True)


def get_conversation_chain(vectorstore2):
    template = """
    You are a financial chat bot, you will respond questions in base the information extracted from a bunch of pdf 
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore2.as_retriever(),
        memory=memory,
        condense_question_prompt=prompt
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history.extend(response['chat_history'])


if os.path.exists(VECTORSTORE_PATH):
    print('hola aquí')
    vectorstore = load_vectorstore(VECTORSTORE_PATH)
    st.session_state.conversation = get_conversation_chain(vectorstore)
else:
    st.error("Vector store not found. Please generate it first.")


def main():
    st.set_page_config(page_title="FinancialChatbot", page_icon="🤖")

    print('session state', st.session_state)

    if "conversation" not in st.session_state or st.session_state.conversation is None:
        st.session_state.conversation = None

    st.header("Chat with NASDAQ PDFs :books:")

    # Move user input handling above chat history display
    user_question = st.chat_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    # Now update the chat history after the user question has been handled
    for message in st.session_state.chat_history:
        # Use isinstance to check the type of message object
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)


if __name__ == '__main__':
    main()