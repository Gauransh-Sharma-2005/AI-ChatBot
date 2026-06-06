import streamlit as st

st.title("ChatBot")

prompt = st.chat_input("Ask a question")

if prompt:
    st.write(f"You asked: {prompt}")