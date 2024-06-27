from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

llm = ChatOllama(model="gemma:2b",temperature=0.5)
prompt = ChatPromptTemplate.from_messages([
    ("system","You are a proficient {Language} Programmer, and will now assist me with by solving my doubts."),
    ("user","{query}")
])

chain =  prompt | llm

st.title("ChatBot")
lang = st.text_input("Enter Programming language.")
query = st.text_input("Enter your query.")
if query:
    st.write_stream(chain.stream({"Language":lang , "query":query}))
        

