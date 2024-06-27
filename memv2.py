import os


import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage , AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory  # it is responsible for reading and updating the chat message history.

## importing claude 3 haiku model
model = ChatOllama(model="gemma:2b",temperature=0.8)

st.title("Simple ChatBot")

st.write("This is a simple chat bot which stores chat histories Based Session ID")
st.divider()


store = {} # dictionary to store {session_id:Past_chats}
# update: scraped due to non-persistant nature of variable in streamlit 
# instead using st.session_state

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state:
        st.session_state[session_id] = ChatMessageHistory()
    return st.session_state[session_id]

with_message_history = RunnableWithMessageHistory(model, get_session_history)

## input sessionID 
SessID = "abc"
configure = {"configurable": {"session_id":SessID}}

if SessID not in st.session_state:
    st.session_state[SessID] = ChatMessageHistory()


for message in st.session_state[SessID]:
    if isinstance(message,AIMessage):
        with st.chat_input("assistant"):
            st.markdown(message)
    else:
        with st.chat_message("user"):
            st.markdown(message)


## input prompt
input_prompt = st.chat_input("Enter a prompt",key="prompt")
with st.chat_message("user"):
    st.markdown(input_prompt)

try:
    with st.chat_message("assistant"):
        st.write_stream(with_message_history.invoke([
        HumanMessage(content=input_prompt)
        ],config=configure).content)
except Exception as e:
    st.write(f"{type(e)=}")