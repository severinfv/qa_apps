import streamlit as st
import os
import google.generativeai as genai 
from youtube_transcript_api import YouTubeTranscriptApi  
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt to instruct the Gemini model to summarize the transcript
prompt = """
You are a YouTube video summarizer. You will take the transcript text
and summarize the entire video, providing the important summary in points
within 250 words. Please provide the summary of the text given here: 
"""

# Function to extract transcript details from a YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]  # Extract the video ID from the URL
        
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine transcript into a single string
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript  # Return the full transcript

    except Exception as e:
        st.error(f"Error fetching transcript: {e}")  
        return None

# Function to generate summary from the Gemini Pro model based on the transcript
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")  
        
        # Generate content by passing the prompt and transcript text to the model
        response = model.generate_content(prompt + transcript_text)
        
        return response.text  
    except Exception as e:
        st.error(f"Error generating summary: {e}")  
        return None

#Initializing a Streamlit app 
st.title("YouTube Transcript to Detailed Notes Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")

# If a YouTube link is provided, display the video's thumbnail image
if youtube_link:
    try:
        video_id = youtube_link.split("=")[1]  # Extract video ID from the link
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True) 
    except IndexError:
        st.error("Invalid YouTube link. Please provide a valid link.")  

# Button to generate detailed notes from the transcript
if st.button("Get Detailed Notes"):
    # Fetch the transcript from the provided YouTube link
    transcript_text = extract_transcript_details(youtube_link)

    # If transcript is successfully fetched, generate the summary
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        
        if summary:
            st.markdown("## Detailed Notes:") 
            st.write(summary)
        else:
            st.error("Failed to generate summary. Please try again.")
