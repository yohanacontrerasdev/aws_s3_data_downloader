import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Establecer la clave de API como variable de entorno
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

PROYECTO_PATH = os.path.dirname(os.path.dirname(__file__))
VECTORSTORE_PATH = os.path.join(PROYECTO_PATH, "vectorstore/")

conversation_chain = None
chat_history = []

def load_vectorstore(path):
    return FAISS.load_local(path, embeddings=OpenAIEmbeddings(), allow_dangerous_deserialization=True)

def get_conversation_chain(vectorstore, getContext=False):
    template = """
    Your template here
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    retriever = vectorstore.as_retriever()
    if getContext:
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            condense_question_prompt=prompt,
            return_source_documents=True,
            output_key='source_documents'
        )
    else:    
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            condense_question_prompt=prompt,
        )
    return conversation_chain

# Función para obtener las respuestas para una pregunta dada
def get_answer(question, conversation_chain):
    response = conversation_chain.invoke({'question': question})
    return response['answer']

# Función para obtener los contextos para una pregunta dada
def get_contexts(question, conversation_chain):
    response = conversation_chain.invoke({'question': question})
    contexts = display_retrieved_documents(response['source_documents'])
    return contexts

def display_retrieved_documents(retrieved_docs):
    page_contents = []
    for doc in retrieved_docs:
        page_contents.append(doc.page_content)
    return page_contents

def execute(df):
    
    # Inicializar el contador para manejar el índice manualmente
    index = 0
    
    if df is not None:

        # Bucle while para iterar sobre el DataFrame
        while index < len(df):
            
            # Cargar el vectorstore desde el disco
            if os.path.exists(VECTORSTORE_PATH):
                vectorstore = load_vectorstore(VECTORSTORE_PATH)
                conversation_chain = get_conversation_chain(vectorstore)
                conversation_chain_context = get_conversation_chain(vectorstore, True)
            else:
                print(f"Vector store not found in {VECTORSTORE_PATH}. Please generate it first.")

            question = df.at[index, 'question']
            
            # Obtener la respuesta utilizando tu modelo
            answer = get_answer(question, conversation_chain)
            #print(f"Question: {question}\nAnswer: {answer}")
            
            # Actualizar la columna 'answer' en el DataFrame
            df.at[index, 'answer'] = answer
            
            # Obtener los contextos
            contexts = get_contexts(question, conversation_chain_context)
            
            # Actualizar la columna 'contexts' en el DataFrame
            df.at[index, 'contexts'] = contexts

            # Incrementar el contador manualmente
            index += 1

    return df