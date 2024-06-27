import streamlit as st
import anthropic
import constant as constant

st.title("Programming chatbot")
with st.sidebar:
    def reset_conversation():
        st.session_state.messages = None
    st.button('Reset Chat', on_click=reset_conversation)


# Set OpenAI API key from Streamlit secrets
client = anthropic.Client(api_key=constant.anthropic_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "You are an programming expert.Ask user which programming language they need assistance in."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input
if prompt := st.chat_input("Ask your Question"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)




with st.chat_message("assistant"):
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=False,
)
        #response = st.write(message)
    response_text = ''.join([block.text for block in message.content])
    st.write(response_text)

st.session_state.messages.append({"role": "assistant", "content": response_text})