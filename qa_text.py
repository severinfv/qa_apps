# Importing load_dotenv to load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Importing necessary libraries
import streamlit as st  
import os  
import google.generativeai as genai  
import logging  

# Configuring the Generative AI API 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Loading the Gemini PRO model
model = genai.GenerativeModel("gemini-pro")

# Function to send a question to the Gemini model and retrieve the generated response
def get_gemini_reponse(question):
    try:
        response = model.generate_content(question)  
        return response.text 
    except Exception as e:
        logging.error(f"Error generating response: {e}")  
        return "Sorry, I couldn't process that request. Please try again later." 

# Initializing a Streamlit app 
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application") 

user_input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    if user_input:  
        response = get_gemini_reponse(user_input)  
        st.write(response)  
    else:
        st.write("Please enter a question before submitting.")  # Handle empty input case
