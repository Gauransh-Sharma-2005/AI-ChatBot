import streamlit as st
import time

# Page Config
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# initialization first
if "messages" not in st.session_state:
        st.session_state.messages = []

if "current_mode" not in st.session_state:
    st.session_state.current_mode = "LLM"

st.title("🤖 AI Assistant")

# Now it's safe to access
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# SideBar
with st.sidebar:
    st.title("🤖 AI Assistant")
    st.markdown("---")
    st.subheader("Features")

    st.success("🧠 General Chat")
    st.info("🌐 Web Search")
    st.warning("📄 RAG Search")

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload Documents",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main Header
st.title("Intelligent Multi-Mode AI Agent")

st.caption(
    "LLM • Web Search • RAG • Memory"
)

# Mode Display
st.info(
    f"Current Mode: {st.session_state.current_mode}"
)

# Chat History
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask something...")

# Message Processing
if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mode Routing
    lower_prompt = prompt.lower()

    if any(word in lower_prompt for word in [
        "latest",
        "today",
        "news",
        "current",
        "recent"
    ]):
        mode = "Web Search"

    elif any(word in lower_prompt for word in [
        "document",
        "pdf",
        "policy",
        "file"
    ]):
        mode = "RAG"

    else:
        mode = "LLM"

    st.session_state.current_mode = mode

    # Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(1)

            response = (
                f"This is a sample response generated "
                f"using {mode} mode.\n\n"
                f"Your question was:\n\n"
                f"**{prompt}**"
            )

            st.markdown(response)

            # SOURCE DISPLAY
            with st.expander("Sources"):

                if mode == "Web Search":
                    st.write("🌐 Example Web Source")
                    st.write("https://example.com")

                elif mode == "RAG":
                    st.write("📄 Uploaded Document")
                    st.write("employee_handbook.pdf")

                else:
                    st.write("🧠 LLM Internal Knowledge")

    # Sotring assistant message
    response = f"You asked: {prompt}"
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )