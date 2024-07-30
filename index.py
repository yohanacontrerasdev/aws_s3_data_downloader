import os
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain

load_dotenv()
VECTORSTORE_PATH = "vectorstore/"

# Here we initialize our history variable
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.set_page_config(page_title='Financial ChatBot', page_icon='🤑')

st.title('FACha_tBot')


# get response
def load_vectorstore(path):
    return FAISS.load_local(path, embeddings=OpenAIEmbeddings(), allow_dangerous_deserialization=True)


def get_retriever():
    if os.path.exists(VECTORSTORE_PATH):
        vectorstore = load_vectorstore(VECTORSTORE_PATH)
        retriever = vectorstore.as_retriever()

        # Print details about the retriever
        print(f'Retriever loaded from {VECTORSTORE_PATH}')
        # replace `size` and `info` with actual methods or properties of the retriever object
        # print(f'Number of documents in retriever: {retriever.size()}')
        # print(f'Other information: {retriever.}')

        return retriever


def get_ai_response(query, hat_history):
    template = """Your are a helpful chat bot. Answer the following questions using the provided context, 
    where is the data to response all the questions, and the history of the conversation: 
    context: {context} 
    chat_history: {chat_history} 
    user_question: {user_question}"""
    prompt = ChatPromptTemplate.from_template(template)
    # here I have to use my llm
    llm = ChatOpenAI()

    retriever = get_retriever()
    # return stream
    chain = prompt | llm | StrOutputParser()
    return chain.stream({
        "context": retriever,
        "chat_history": hat_history,
        "user_question": query,
    })


# conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

user_query = st.chat_input('Ask for financial assistant')

# user input
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message('Human'):
        st.markdown(user_query)
    with st.chat_message('AI'):
        ai_response = st.write_stream(get_ai_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(ai_response))
