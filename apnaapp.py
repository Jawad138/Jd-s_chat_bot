import streamlit as st
import requests
import json
import os

from dotenv import load_dotenv

API_URL = "https://api.openai.com/v1/chat/completions"

# Load environment variables from .env file
load_dotenv()

st.set_page_config(
    page_title="Jd's Chatbot",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="auto"
)

# Function to interact with the ChatGPT API
def query_chatbot(message, api_key):
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    data = response.json()
    return data["choices"][0]["message"]["content"]

# Streamlit interface
def main():
    # Custom CSS style...
    
    # Add sidebar
    with st.sidebar:
        st.markdown("## Options")
        st.write("Enter your API Key:")
        api_key = st.text_input("API Key", value="", type="password")
        submit_button = st.button("Submit")

        # When the "Submit" button is clicked, move focus to the user input field
        if submit_button:
            st.experimental_set_query_params(input_field="user_input")

    # Set custom background
    st.markdown(
        """
        <style>
        body {
            background: url("background.png") no-repeat fixed;
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Jd's Chatbot")

    # Increase width of the main content area
    st.markdown(
        """
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Move focus to the user input field when the page loads or "Submit" button is clicked
    if st.experimental_get_query_params().get("input_field") == ["user_input"]:
        st.markdown(
            """
            <script>
            document.getElementById('user_input').focus();
            </script>
            """,
            unsafe_allow_html=True
        )

    user_input = st.text_area("You:", value="", height=150, max_chars=None, key="user_input", help=None, placeholder="Send message")

    if st.button("Send", key="send_button"):
        if user_input and api_key:
            response = query_chatbot(user_input, api_key)
            st.subheader("Chatbot")
            st.markdown(f'<div class="custom-output">{response}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
