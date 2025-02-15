import os
import streamlit as st
import random
import time
import base64
from cybersecure import CyberSecure, doc_process
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from langchain.schema import HumanMessage
#This page implements the streamlit UI
# Set page configuration
st.set_page_config(page_title="CyberLaw AI", page_icon="public/logo.png", layout="wide")

# Custom CSS for better UI
def add_custom_css():
    custom_css = """
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .st-chat-input {
            border-radius: 15px;
            padding: 10px;
            border: 1px solid #ddd;
            margin-bottom: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .stButton > button {
            background-color: #0066cc;
            color: white;
            font-size: 16px;
            border-radius: 20px;
            padding: 10px 20px;
            margin-top: 5px;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #0052a3;
        }
        .st-chat-message-assistant {
            background-color: #f7f7f7;
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .st-chat-message-user {
            background-color: #d9f0ff;
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .chat-input-container {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f0f0f0;
            padding: 20px;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
            display: flex;
            gap: 10px;
        }
        .chat-input {
            flex-grow: 1;
        }
        .st-title {
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            color: #333;
            display: flex;
            align-items: center;
            gap: 15px;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .logo {
            width: 40px;
            height: 30px;
        }
        .st-sidebar {
            background-color: #f9f9f9;
            padding: 20px;
        }
        .st-sidebar header {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .st-sidebar p {
            font-size: 14px;
            color: #666;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

add_custom_css()
##Below Code implementation is tha main functioanlity in building the streamlit application
# Title with Logo
logo_path = "Public/logo.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
    <div class="st-title">
        <img src="data:image/png;base64,{encoded_image}" alt="CyberLaw AI Logo" class="logo">
        <span>CyberLaw - An AI based Legal Assistant </span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="st-title">
        <span>CyberLaw` AI - Your Legal Assistant 📖</span>
    </div>
    """, unsafe_allow_html=True)

# Sidebar improvements
st.sidebar.header("About CyberLaw AI")
st.sidebar.markdown("""
**CyberLaw AI** is a free, open-source AI legal assistant that helps answer legal questions.

Visit our website: [CyberLaw AI](http://127.0.0.1:5500/CyberSecure-AI/Public/index.html)

_Disclaimer_: This tool is in its pilot phase, and responses may not be 100% accurate.
""")

load_dotenv()

# Load API key
openai_api_key = os.getenv('OPENAI_API_KEY')
#Defining the Language Model
llm = ChatOpenAI(model  = 'gpt-4o' ,temperature = 0.9, openai_api_key = openai_api_key)

#Defining the Embeddings
embeddings = OpenAIEmbeddings()

#Defining the vector store
vector_store = Chroma(persist_directory="chroma_db_legal_bot_part1", embedding_function=embeddings)

#Creating the instance of the class Lawglance
law = CyberSecure(llm, embeddings, vector_store)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# Chat input prompt fixed at the bottom
st.markdown("<div class='chat-input-container'>", unsafe_allow_html=True)
# User Input
prompt = st.chat_input("Have a legal question? Let’s work through it.")
# uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, TXT) for analysis:", type=["pdf", "docx", "txt"])

st.markdown("</div>", unsafe_allow_html=True)

# Process uploaded file
# if uploaded_file is not None:
#     # Process the file here if needed
#     page_num = doc_process.get_pages( uploaded_file)
#     # processor.uploaded_document("upload_file")
#     st.success("File uploaded successfully!")
# else:
#     pass

    
if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate answer from LLM
    query = prompt
    result = law.conversational(query)

    # Assistant's response
    def response_generator(result):
        response = random.choice([result])
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

    final_response = f"AI Legal Assistant: {result}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = "".join(list(response_generator(final_response)))
        response = response.replace(". ", ".\n")
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
