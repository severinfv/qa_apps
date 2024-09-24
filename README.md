# AI-Powered Q&A Applications

This repository contains a collection of AI-driven Q&A applications built with Streamlit and Google Generative AI models, focusing on various use cases such as text, image, PDF, and database querying. Each app demonstrates features, including real-time interaction with large language models, chat history management using session state, and more. Apps use Google GenAI models and Streamlit for web interface. Below is an overview of each app:

---
### [`qa_chathistory.py`](qa_chathistory.py)
**Description**: This app demonstrates how to build a Q&A chatbot with session-based chat history, allowing users to see past conversations in real-time.
- **Main Tools**: 
  - Google Generative AI (`gemini-pro`)
  - Streamlit for user interaction
  - Session State for managing chat history
- **Features**: Uses Streamlit session state to maintain chat history across multiple interactions, providing a conversational experience.

### [`qa_text.py`](qa_text.py)
**Description**: This application allows users to ask questions based on a provided text input, leveraging Google's Generative AI to generate detailed responses. 
- **Main Tools**: 
  - Google Generative AI (`gemini-pro` model)
  - Streamlit for the web interface
- **Features**: User input is processed in real-time with the model providing detailed responses based on natural language queries.

### [`qa_image.py`](qa_image.py)
**Description**: This app lets users upload an image (such as a document or visual content), and Google's Generative AI analyzes the image to answer related questions.
- **Main Tools**: 
  - Google Generative AI (`gemini-1.5-flash`)
  - Streamlit for image uploading and display
  - PIL for image processing
- **Features**: Handles image uploads and integrates with AI to provide context-based responses.

### [`qa_pdf.py`](qa_pdf.py)
**Description**: Users can upload PDF files, and the app extracts text from the document to answer questions related to the content.
- **Main Tools**: 
  - PyPDF2 for extracting text from PDFs
  - Google Generative AI for content analysis
  - Streamlit for user interaction
- **Features**: Efficient handling of multi-page PDF documents, including real-time extraction and summarization.

### [`qa_sqldb.py`](qa_sqldb.py)
**Description**: This application connects to an SQLite database, allowing users to submit natural language questions, which are converted into SQL queries by the AI model.
- **Main Tools**: 
  - Google Generative AI (`gemini-pro`)
  - SQLite for database querying
  - Streamlit for query submission
- **Features**: Automatic SQL query generation based on natural language inputs, allowing dynamic querying of a SQL database.

### [`qa_documents.py`](qa_documents.py)
**Description**: This app allows users to upload multiple document types (PDF, text, etc.) and perform Q&A based on their contents. It uses FAISS for document vectorization and similarity search.
- **Main Tools**: 
  - FAISS for vector-based document retrieval
  - Google Generative AI
  - Streamlit for document uploading
- **Features**: Uses FAISS for vector-based search, enabling users to query specific document chunks based on context.

### [`qa_ytvid.py`](qa_ytvid.py)
**Description**: Users can input a YouTube video link, and the app extracts the transcript, which is then analyzed to provide a summary or answer specific questions.
- **Main Tools**: 
  - YouTube Transcript API for transcript extraction
  - Google Generative AI for video content summarization
  - Streamlit for user interaction
- **Features**: Integration with YouTube Transcript API to automatically extract and summarize video content.

### [`qa_invoice_img.py`](qa_invoice_img.py)
**Description**: This app is designed for extracting and analyzing data from invoice images, answering questions about the extracted information.
- **Main Tools**: 
  - PIL for image processing
  - Google Generative AI (`gemini-pro`) for invoice data extraction and Q&A
  - Streamlit for image uploads
- **Features**: Image analysis for structured data extraction from invoices, with natural language interaction.

### [`qa_cv.py`](qa_cv.py)
**Description**: This application evaluates a user's CV against a provided job description, offering both HR-style reviews and ATS-style keyword matching.
- **Main Tools**: 
  - PyPDF2 for CV (PDF) extraction
  - Streamlit for user interaction
- **Features**: Uses natural language prompts to simulate HR and ATS evaluations, providing insights into CV-job description alignment and keyword analysis.

---

## How to Run
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run each application by navigating to the file directory and executing `streamlit run <filename>.py`.

---