from dotenv import load_dotenv
load_dotenv() 

import streamlit as st
import os
from PIL import Image  
import google.generativeai as genai  

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-1.5-flash")
# Function to load Gemini Pro Vision and get the model's response
def get_gemini_reponse(input_prompt, image_data, input):
    try:
        # Send the input prompt, image, and user query to the Gemini model
        response = model.generate_content([input_prompt, image_data[0], input])
        return response.text
    except Exception as e:
        st.error(f"Error generating response from Gemini: {e}")
        return None

# Function to process the uploaded image and extract its details
def input_image_details(uploaded_file):
    try:
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()  # Get the raw byte data of the image

            image_parts = [
                {
                    "mime_type": uploaded_file.type,  # Get the file type (e.g., image/jpeg)
                    "data": bytes_data  # Image byte data
                }
            ]
            return image_parts
        else:
            raise FileNotFoundError("No file uploaded")  # Handle missing file scenario
    except Exception as e:
        st.error(f"Error processing the image: {e}")
        return None

# Streamlit Setup
st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("MultiLanguage Invoice Extractor")

input = st.text_input("Input prompt: ", key="input")

uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image = None  

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)  
        st.image(image, caption="Uploaded Image.", use_column_width=True)  
    except Exception as e:
        st.error(f"Error loading the image: {e}")  # Handle errors in image loading


submit = st.button("Tell me about the image")

# Predefined input prompt for the Gemini model, guiding it to interpret invoices
input_prompt = """
You are an expert in understanding invoices. An invoice will be uploaded. 
You have to answer any questions based on the uploaded invoice image.
"""

if submit:
    if uploaded_file is not None:
        image_data = input_image_details(uploaded_file)  
        if image_data:
            response = get_gemini_reponse(input_prompt, image_data, input)
            st.subheader("The response is")  
            st.write(response)
    else:
        st.error("Please upload an invoice image to proceed.")  
