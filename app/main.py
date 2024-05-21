import ai
import re
import json
import os
import streamlit as st
import logging
from io import StringIO

logger = logging.getLogger(__name__)
logging.basicConfig(filename='ai-hackathon.log')
logger.setLevel(os.environ.get('LOG_LEVEL', logging.INFO))

def ask_question(question):
    with st.spinner('Wait for it...'):
        return ai.invoke(question)

def extract_answer(ai_response):
    logger.debug("AI response " + json.dumps(ai_response))
    query_text = ""
    pattern = r"<\?php[\s\S]*?(?=```|$)"
    match = re.search(pattern, ai_response, re.IGNORECASE | re.DOTALL)
    if match:
        query_text = match.group().strip()
    return query_text

hello_message = f"Hello 👋. I am AI Assistant which can write test cases for Drupal modules."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": hello_message, "type": "text"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.code(message["content"], language=message.get("type"))

prompt = st.chat_input("Drupal module routing file contents")

if prompt:
     # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "yaml"})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.code(prompt, language="yaml")

    ## Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        logger.debug("User prompt " + json.dumps(prompt))
        response = extract_answer(ask_question(prompt))
        message_placeholder.code(response, language='php')

    st.session_state.messages.append({"role": "assistant", "content": response, "type": "php"})
