import streamlit as st

st.title("ChatBot")

# Chat Input
prompt = st.chat_input("Ask a question")

if prompt:
    st.write(f"You asked: {prompt}")

# SideBar
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

with st.sidebar:
    st.title("🤖 AI Assistant")
    st.markdown("---")
    st.write("Modes")
    st.success("LLM")
    st.info("Web Search")
    st.warning("RAG")