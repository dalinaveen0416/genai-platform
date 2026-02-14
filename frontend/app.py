import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000"

def safe_api_call(endpoint, data_or_files, is_json=True):
    """Safely call API and handle errors"""
    try:
        if is_json:
            response = requests.post(f"{API_URL}{endpoint}", json=data_or_files)
        else:
            response = requests.post(f"{API_URL}{endpoint}", files=data_or_files)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from server"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

st.title("Groq GenAI Platform")

menu = st.sidebar.selectbox(
    "Choose Module",
    ["RAG Chat", "Summarize", "SQL Chat", "Agent"]
)

if menu == "RAG Chat":

    file = st.file_uploader("Upload PDF")

    if file:
        result = safe_api_call("/ingest", {"file": file}, is_json=False)
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.success(result.get("message", "Document indexed"))

    question = st.text_input("Ask question")

    if st.button("Submit"):
        result = safe_api_call("/chat", {"question": question})
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.write(result.get("answer", "No answer returned"))


elif menu == "Summarize":
    st.write("Enter large text to summarize:")

    text = st.text_area("Enter text")

    if st.button("Summarize"):
        result = safe_api_call("/summarize", {"text": text})
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.write(result.get("summary", "No summary returned"))


elif menu == "SQL Chat":
    st.write("Ask a question about the sample database (e.g. 'List all users'):")

    question = st.text_input("Ask SQL question")

    if st.button("Run"):
        result = safe_api_call("/sql-chat", {"question": question})
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.write(result.get("result", "No result returned"))


elif menu == "Agent":
    st.write("Ask a question or math problem to the agent:")

    query = st.text_input("Ask agent")

    if st.button("Run Agent"):
        result = safe_api_call("/agent", {"question": query})
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.write(result.get("result", "No result returned"))
