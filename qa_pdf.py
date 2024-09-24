# Importing necessary libraries for the application
import os
import io
from dotenv import load_dotenv

import streamlit as st
from PyPDF2 import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Load API keys and set up environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to extract text from uploaded PDF files
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_bytes = pdf.read()
        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Split the extracted text into manageable chunks for processing
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Generate vector embeddings from the text chunks and store them locally using FAISS
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Create a conversational chain with a prompt that ensures detailed and accurate responses
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. 
    If the answer is not in the provided context, say "answer is not available in the context." 
    Do not provide incorrect answers.
    Context: \n {context}\n 
    Question: \n {question}\n 

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Process the user's input question, search for similar documents, and provide an answer
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Load precomputed vectors from FAISS and perform a similarity search
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    # Get the conversational chain to process the query
    chain = get_conversational_chain()

    # Generate a response based on the found documents and user question
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    print(response)
    st.write("Reply: ", response["output_text"])

# Main function to handle the Streamlit interface and user interactions
def main():
    st.set_page_config("Chat with multiple PDF documents")
    st.header("Chat with multiple PDF documents using Gemini")

    # Input for user's question
    user_question = st.text_input("Ask a Question from the PDF files")

    if user_question:
        user_input(user_question)

    # Sidebar for uploading PDF documents
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF files", type="pdf", accept_multiple_files=True)
        if st.button("Submit"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)  # Extract raw text from PDFs
                text_chunks = get_text_chunks(raw_text)  # Split the text into chunks
                get_vector_store(text_chunks)  # Generate vector embeddings and store them
                st.success("Done")

# Run the main function
if __name__ == "__main__":
    main()
