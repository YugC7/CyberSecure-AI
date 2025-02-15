#adding necessary imports
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory # type: ignore
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import chromadb
import fitz
from openai import OpenAI
from sentence_transformers import SentenceTransformer

#This Class delas with working of Chatbot

class CyberSecure: 
  """This is the class which deals mainly with a conversational RAG
    It takes llm, embeddings and vector store as input to initialise.
    It has a function conversational which takes a query as input and returns the answer.

    Run it with:
    law = CyberSecure(llm,embeddings,vectorstore)
    query1 = "What is rule of Law?"
    law.conversational(query1)
    query2 = "Is it applicable in India?"
    law.conversational(query2)
  """
  store = {}

  def __init__(self,llm,embeddings,vector_store):
    self.llm = llm
    self.embeddings = embeddings
    self.vector_store = vector_store

  def __retriever(self):
    """The function to define the properties of retriever"""
    retriever = self.vector_store.as_retriever(search_type="similarity_score_threshold",search_kwargs={"k": 10, "score_threshold":0.3})
    return retriever
  
  def llm_answer_generator(self,query):
    llm = self.llm
    retriever = self.__retriever()
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    system_prompt = (
      "You are a helpful legal assistant who is tasked with answering to the question, which is: {input}")
    qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", """.
                You are provided a law specific question bellow, your work is to retrive relevant information from google and display it to the user. It can be what to do and what not to do, which laws are required to be complied and how would someone approach the particular legal issue in india\n\nRelevant Context: \n"
                {context}

                You should return only the answer as output."""),
            ]
        )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

  def get_session_history(self,session_id: str) -> BaseChatMessageHistory:
    if session_id not in CyberSecure.store:
        CyberSecure.store[session_id] = ChatMessageHistory()
    return CyberSecure.store[session_id]
  
  def conversational(self,query):
    rag_chain = self.llm_answer_generator(query)
    get_session_history = self.get_session_history
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer")
    response = conversational_rag_chain.invoke(
        {"input": query},
        config={
            "configurable": {"session_id": "abc123"}
        },
    )
    return(response['answer'])
  
class doc_process():
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    #   """This function is used to process the uploaded document"""

    # def __init__(self):
    #     self.client = chromadb.PersistentClient(path="./chroma_db")  # Persistent storage
    #     self.collection = self.client.get_or_create_collection("documents")
    # self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # Efficient embedding model
    #     self.openai_client = OpenAI()  # Replace with your API key

    # def extract_text(self, document_path):
    #     """Extract text from a PDF document."""
    #     text = ""
    #     with pdfplumber.open(document_path) as pdf:
    #         for page in pdf.pages:
    #             text += page.extract_text() + "\n"
    #     return text

    def get_pages(uploaded_file):
      file = fitz.open(stream=uploaded_file.read(), filetype="pdf")  # Read file from stream
      num_pages = file.page_count
      return [str(i) for i in range(1, num_pages + 1)]  # Return list of page numbers

    # def get_pages(uploaded_file):
    #   file = fitz.open(uploaded_file)
    #   num_pages = file.page_count
    #   id = []
    #   i = 1
    #   while i <= num_pages:
    #     id.append(f'{i}')
    #     i += 1
    #   ids = (list(id))
    #   return ids

    def uploaded_document(self, uploaded_file):
      file = fitz.open(stream=uploaded_file.read(), filetype="pdf")
      text = chr(12).join([page.get_text() for page in file])
      vectors = SentenceTransformer("all-MiniLM-L6-v2").encode(text.split(chr(12)))
      ids = self.get_pages(uploaded_file)
      client = chromadb.PersistentClient(path="./chroma_db")  
      collection = client.get_or_create_collection("new_vector_collection") 
      collection.add(documents=vectors, ids=ids)
      return "Document uploaded and stored successfully!"
  
    def retrieve_context(self, query):
        """Retrieves relevant context using ChromaDB for RAG."""
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(query_embeddings=[query_embedding], n_results=3)  # Retrieve top 3 relevant docs
        return [result["content"] for result in results["metadatas"][0]]
  
    def conduct_rag(self, query):   
        """Conducts Retrieval-Augmented Generation using GPT-4."""
        context = self.retrieve_context(query)
        prompt = f"Use the following context to answer: {context}\n\nQuestion: {query}"
        
        response = self.openai_client.Completion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]

        conduct_rag(self,query)

# # Usage
# processor = DocumentProcessor()
# processor.uploaded_document("sample.pdf")
# response = processor.conduct_rag("Summarize the document")
# print(response)