import query_chain
import module_contents
import re
import streamlit as st


def invoke_module(url):
    chain_response=""
    with st.status("Invoking model...", expanded=True) as status:
        st.write("Cloning the module...")
        module_data, routing_file_data = module_contents.clone_and_convert_to_json(url)
        st.write("Cloned the module.")
        st.write("Invoking the AI model...")
        print(routing_file_data)
        chain_response = query_chain.invoke(routing_file_data)
        status.update(label="Invocation complete!", state="complete", expanded=False)
        print(chain_response)
    return chain_response

def extract_answer(ai_response):
    query_text = ""
    #pattern = r'\bAnswer:\s*(.+)'
    pattern = r'^```(?:\w+)?\s*\n(.*?)(?=^```)```'
    match = re.search(pattern, ai_response, re.DOTALL | re.MULTILINE)
    if match:
        query_text = match.group(1).strip()
    return query_text

st.title('AI Assistant writing tests for Drupal Modules')

hello_message = f"Hello 👋. I am AI Assistant which can write test cases for Drupal modules."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": hello_message, "type": "text"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("type") != "text":
            st.code(message["content"], language=message.get("type"))
        else:
            st.markdown(message["content"])

prompt = st.chat_input("Drupal module repository link(HTTPS)")

if prompt:
     # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.write(prompt)
    ## Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response_list = []
        response = extract_answer(invoke_module(prompt))
        #response = invoke_module(prompt)
        response_list.append(response)

        for response in response_list:
            full_response += response
        message_placeholder.code(full_response, language="php")

    st.session_state.messages.append({"role": "assistant", "content": full_response, "type": "php"})
