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
    logger.info("Invoking the AI")
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

#prompt = st.chat_input("Drupal module routing file contents")


uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # To convert to a string based IO:
    string_input = StringIO(uploaded_file.getvalue().decode("utf-8")).read()


     # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": string_input, "type": "yaml"})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.code(string_input, language="yaml")
    ## Display assistant response in chat message container
    full_response = ""
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response_list = []
        response = extract_answer(ask_question(string_input))
        response_list.append(response)

        for response in response_list:
            full_response += response
            message_placeholder.code(full_response, language='php')

    st.session_state.messages.append({"role": "assistant", "content": full_response, "type": "php"})

logging.basicConfig(filename='myapp.log', level=logging.INFO)
