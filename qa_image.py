# Importing load_dotenv to load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Importing necessary libraries
import streamlit as st  
import os  
import google.generativeai as genai 
from PIL import Image  
import logging 

# Configuring the Generative AI API 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Loading the Gemini PRO model 
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_reponse(input, image):
    try:
        if input != "":  
            response = model.generate_content([input, image])  
        else:
            response = model.generate_content(image)  
        return response.text  
    except Exception as e:
        logging.error(f"Error generating response: {e}")  # Log the error for debugging
        return "Sorry, I couldn't process that request. Please try again later."  # User-friendly error message

# Initializing a Streamlit app
st.set_page_config(page_title="Gemini Image QA")
st.header("Gemini LLM Application") 

input = st.text_input("Input prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = None 
if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)  
        st.image(image, caption="Uploaded Image", use_column_width=True)  
    except Exception as e:
        logging.error(f"Error loading image: {e}") 
        st.write("Error loading image. Please try again.") 

submit = st.button("Tell me about the image")

if submit:
    if image is not None:  
        response = get_gemini_reponse(input, image)  
        st.subheader("The response is")  
        st.write(response)  
    else:
        st.write("Please upload an image before submitting.")  
