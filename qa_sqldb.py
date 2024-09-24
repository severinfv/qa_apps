from dotenv import load_dotenv
load_dotenv()  

import streamlit as st
import os
import sqlite3
import google.generativeai as genai  

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and generate SQL queries from the question
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')  # Load the Gemini Pro model
        response = model.generate_content([prompt[0], question])  # Generate response using the prompt and question
        return response.text  # Return the generated SQL query text
    except Exception as e:
        st.error(f"Error generating response from Gemini: {e}")
        return None

# Function to execute an SQL query and retrieve data from the SQLite database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)  # Connect to the SQLite database
        cur = conn.cursor()
        cur.execute(sql)  # Execute the SQL query
        rows = cur.fetchall()  # Fetch all rows from the query result
        conn.commit()  # Commit any changes (if applicable)
        conn.close()  # Close the connection
        return rows  # Return the result rows
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return None
    except Exception as e:
        st.error(f"Error reading SQL query: {e}")
        return None

# Define the initial prompt for guiding the Gemini model to generate SQL queries
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION. \n\nFor example,\nExample 1 - How many records are present?, 
    the SQL command will be something like this: SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this: SELECT * FROM STUDENT 
    WHERE CLASS="Data Science"; 
    Also, the SQL code should not have backticks or 'sql' keyword in the output.
    """
]

# Initializing a Streamlit app
st.set_page_config(page_title="I can Retrieve Any SQL Query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(question, prompt)
    
    if response:
        st.subheader("Generated SQL Query:")
        st.write(response)  
        
        query_results = read_sql_query(response, "sql.db")
        
        if query_results:
            st.subheader("The Response is:")
            for row in query_results:
                st.write(row)  
        else:
            st.error("No results found or error in query execution.")
    else:
        st.error("Failed to generate SQL query.")

