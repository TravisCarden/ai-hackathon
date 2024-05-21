import ai
import re
import json
import os
import streamlit as st
import logging

def setup_logging():
    """Configure logging for the application."""
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='ai-hackathon.log', level=os.environ.get('LOG_LEVEL', 'INFO').upper())
    return logger

def ask_question(question):
    """Invoke the AI model with a question and return the response."""
    with st.spinner('Wait for it...'):
        return ai.invoke(question)

def extract_answer(ai_response, logger):
    """Extract the relevant answer from the AI response using a regex pattern."""
    logger.debug("AI response: %s", json.dumps(ai_response))
    pattern = r"<\?php[\s\S]*?(?=```|$)"
    match = re.search(pattern, ai_response, re.IGNORECASE | re.DOTALL)
    return match.group().strip() if match else ""

def initialize_session_state():
    """Initialize session state for messages if not already set."""
    hello_message = "Hello 👋. I am AI Assistant which can write test cases for Drupal modules."
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": hello_message, "type": "text"}]

def display_chat_history():
    """Display chat messages from history on app rerun."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.code(message["content"], language=message.get("type"))

def process_prompt(prompt, logger):
    """Process user prompt and display the assistant's response."""
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "yaml"})
    with st.chat_message("user"):
        st.code(prompt, language="yaml")

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        logger.debug("User prompt: %s", json.dumps(prompt))
        ai_response = ask_question(prompt)
        response = extract_answer(ai_response, logger)
        message_placeholder.code(response, language='php')

    st.session_state.messages.append({"role": "assistant", "content": response, "type": "php"})

def main():
    """Main function to execute the Streamlit app logic."""
    logger = setup_logging()
    initialize_session_state()
    display_chat_history()

    prompt = st.chat_input("Drupal module routing file contents")
    if prompt:
        process_prompt(prompt, logger)

if __name__ == "__main__":
    main()
