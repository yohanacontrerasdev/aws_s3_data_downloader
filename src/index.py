import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Here we initialize our history variable
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.set_page_config(page_title='Financial ChatBot', page_icon='🤑')

st.title('FACha_tBot')

# get response
def get_ai_response(query, hat_history):
    template = """
    Your are a helpful assistant. Answer the following questions considering the history of the conversation:
    
    Chat history: {chat_history}
    User question: {user_question}
    """
    prompt = ChatPromptTemplate.from_template(template)
#     here I have to use my llm
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()
    return chain.stream({
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
if user_query is not None and user_query!= "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message('Human'):
        st.markdown(user_query)
    with st.chat_message('AI'):
        ai_response = st.write_stream(get_ai_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(ai_response))