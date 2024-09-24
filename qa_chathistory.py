from dotenv import load_dotenv
load_dotenv()  

import streamlit as st
import os
import google.generativeai as genai  

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")  
chat = model.start_chat(history=[])  

# Function to send a question and get a streamed response from the Gemini model
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)  # Streamed response from the model
        return response
    except Exception as e:
        st.error(f"Error getting response from Gemini: {e}")  # Handle any errors
        return None

# Initialize a Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state if it doesn't already exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []  # Initialize empty chat history in session state

input = st.text_input("Input:", key="input")
submit = st.button("Ask your question")

if submit and input:
    response = get_gemini_response(input)  
    if response:  
        st.session_state['chat_history'].append(("User", input))  # Add user's input to chat history
        st.subheader("The response is:")
        
        for chunk in response:
            st.write(chunk.text)  # Display the response in chunks as it streams
            st.session_state['chat_history'].append(("Bot", chunk.text))  # Append bot response to chat history

# Display the chat history
st.subheader("Chat history:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")  # Display each entry (role and text) from the chat history
