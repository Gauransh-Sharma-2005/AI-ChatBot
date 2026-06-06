import streamlit as st

st.title("ChatBot")

# initialization first
if "messages" not in st.session_state:
        st.session_state.messages = []

st.title("🤖 AI Assistant")

# Now it's safe to access
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask something...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    response = f"You asked: {prompt}"

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

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