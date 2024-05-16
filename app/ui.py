import query_chain
import re
import streamlit as st


def ask_question(question):
    chain_response = query_chain.question_chain(question)
    return chain_response

def extract_answer(ai_response):
    query_text = ""
    pattern = r'\bAnswer:\s*(.+)'
    match = re.search(pattern, ai_response, re.IGNORECASE | re.DOTALL)
    if match:
        query_text = match.group(1).strip()
    return query_text

hello_message = r"""Hello 👋. I am AI Assistant which can write test cases for Drupal modules.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": hello_message, "type": "text"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.text(message["content"])

prompt = st.chat_input("Drupal module routing file contents")

if prompt:
     # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    ## Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response_list = []
        response = extract_answer(ask_question(prompt))
        response_list.append(response)

        for response in response_list:
            full_response += response
            message_placeholder.write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response, "type": "text"})
