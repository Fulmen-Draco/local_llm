from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage , AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import streamlit as st

st.title("Programming Chat bot")
st.divider()
 
llm = ChatOllama(model="gemma:2b", temperature=0.2)

prompt = ChatPromptTemplate.from_messages([
    ("system","You are a proficient {Language} Programmer, and will now assist me with by solving my doubts.",),
    MessagesPlaceholder(variable_name="messages"),
])

chain = prompt | llm 

# defining inputs

store = {} # dictionary to store {session_id:Past_chats}
# update: scraped due to non-persistant nature of variable in streamlit 
# instead using st.session_state
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)

## input sessionID 
# SessID = "default"
configure = {"configurable": {"session_id":"default"}}

## streamlit
#initialise a store space
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    p_lang = st.text_input("Enter name of programming language",key="lang")

# take input; store it with role:user and display it
if doubt := st.chat_input("Enter your doubt",key="doubt"):
    st.session_state.messages.append({"role": "user", "content": doubt})
    with st.chat_message("user"):
        st.markdown(doubt)

# generate output; store it with role:assistant and display it
    with st.chat_message("assistant"):
        result = with_message_history.invoke(
            {"messages": [HumanMessage(content=doubt)], "Language": p_lang},
            config=configure
        )
        st.write(result.content)
        st.session_state.messages.append({"role": "assistant", "content": result.content})
        



