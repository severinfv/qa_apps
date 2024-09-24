# Importing necessary libraries for the application
import streamlit as st
import os
from langchain_groq import ChatGroq  
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from langchain.chains.combine_documents import create_stuff_documents_chain  
from langchain_core.prompts import ChatPromptTemplate  
from langchain.chains import create_retrieval_chain 
from langchain_community.vectorstores import FAISS  
from langchain_community.document_loaders import PyPDFDirectoryLoader  
from langchain_google_genai import GoogleGenerativeAIEmbeddings  
from dotenv import load_dotenv  
import time  
import logging 

# Load environment variables (API keys) from .env file
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# Initialize the ChatGroq model with a specific Llama3 model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Define the prompt template for answering questions based on the context from documents
prompt = ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question.
<context>
{context}
<context>
Questions: {input}
"""
)

# Initializing a Streamlit app
st.set_page_config(page_title="Document Q&A")
st.header("Gemini LLM Application") 

# Function to generate vector embeddings for the documents
def vector_embedding():
    try:
        if "vectors" not in st.session_state:
            # Initialize embeddings using Google Generative AI
            st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            
            # Load PDF documents from the 'docs' folder
            st.session_state.loader = PyPDFDirectoryLoader("./docs")
            st.session_state.docs = st.session_state.loader.load()  # Load the documents
            
            # Split documents into chunks
            st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:20])
            
            # Create vector embeddings using FAISS
            st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
    except Exception as e:
        logging.error(f"Error during vector embedding: {e}")
        st.write("Error while creating vector embeddings. Please check the document format or try again.")


prompt1 = st.text_input("Enter Your Question From Documents")

if st.button("Documents Embedding"):
    vector_embedding()
    st.write("Vector Store DB Is Ready")

# Handle the document retrieval and response generation
if prompt1:
    try:
        # Create the document chain with the provided LLM and prompt
        document_chain = create_stuff_documents_chain(llm, prompt)
        
        # Retrieve the vectors stored in session state
        retriever = st.session_state.vectors.as_retriever()
        
        # Create a retrieval chain to retrieve relevant document chunks
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        
        # Invoke the chain to get the response
        response = retrieval_chain.invoke({'input': prompt1})

        # Display the response in Streamlit
        st.write(response['answer'])

        # Expand section to display document similarity search results
        with st.expander("Document Similarity Search"):
            # Display the relevant chunks from the document context
            for i, doc in enumerate(response["context"]):
                st.write(doc.page_content)
                st.write("--------------------------------")
    except KeyError:
        st.write("Error: It seems the vector store is not initialized. Please click on 'Documents Embedding' first.")
    except Exception as e:
        logging.error(f"Error during document retrieval or response generation: {e}")
        st.write("An error occurred while processing the request. Please try again.")
