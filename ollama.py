from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint
import streamlit as st

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_new_tokens=512,
    temperature=0.5,
    huggingfacehub_api_token="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",
)
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
        

