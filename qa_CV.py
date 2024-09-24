import streamlit as st
import google.generativeai as genai  
import os
import PyPDF2 as pdf  
from dotenv import load_dotenv  
import json 

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(jd_content, cv_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')  
        response = model.generate_content([jd_content, cv_content, prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating response from Gemini: {e}")
        return None

# Function to extract text from an uploaded PDF file (CV)
def input_pdf_text(uploaded_file):
    try:
        if uploaded_file is not None:
            reader = pdf.PdfReader(uploaded_file)
            cv_content = ""
            for page in range(len(reader.pages)):
                page = reader.pages[page]
                cv_content += str(page.extract_text())  
            return cv_content
        else:
            raise FileNotFoundError("No file uploaded")  
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

# Prompts for the Gemini model to evaluate the resume
input_prompt1 = """
 You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements. Consider transferrable skills that could be relevant from previous positions.
"""

input_prompt2 = """
You are a skilled or very experienced Application Tracking System with a deep understanding of tech fields, data science, data analyst roles. 
Your task is to evaluate the resume based on the given job description.
Analyze if the CV matches the requirements listed in the job description, both technical and in terms of years of work experience. Consider if the applicant has transferrable skills from previous positions that match the current job description. 
The job market is very competitive. Assign the percentage Matching based on JD and
the missing keywords with high accuracy.
resume:{cv_content}
description:{jd_content}

I want the response in one single string with the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# Streamlit App setup
st.set_page_config(page_title="Application Tracking System Resume Support")
st.header("HR/ATS Evaluation")

jd_content = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your CV in PDF format.", type=["pdf"], help="Please upload your CV in PDF format.")

# Display a success message if a PDF is uploaded
if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell Me About this applicant")
submit2 = st.button("Applicant-Job match")

# Logic for the first button (HR-style evaluation)
if submit1:
    if uploaded_file is not None and jd_content:
        cv_content = input_pdf_text(uploaded_file)
        if cv_content:
            response = get_gemini_response(jd_content, cv_content, input_prompt1)
            if response:
                st.subheader("Result:")
                st.write(response)  # Display the HR-style evaluation result
    else:
        st.write("Please upload your resume and fill in the job description")

# Logic for the second button (ATS-style evaluation)
if submit2:
    if uploaded_file is not None and jd_content:
        cv_content = input_pdf_text(uploaded_file)
        if cv_content:
            response = get_gemini_response(jd_content, cv_content, input_prompt2)
            if response:
                st.subheader("Result:")
                st.write(response)  
    else:
        st.write("Please upload your resume and fill in the job description")
