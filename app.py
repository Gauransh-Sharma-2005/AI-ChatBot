import streamlit as st
import time

# Page Config
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Session State
if "messages" not in st.session_state:
        st.session_state.messages = []

# if "current_mode" not in st.session_state:
#     st.session_state.current_mode = "LLM"
# st.title("🤖 AI Assistant")

# Router
def route_query(query):

    query = query.lower()

    # Real-time information
    web_keywords = [
        "latest",
        "today",
        "current",
        "news",
        "recent",
        "stock",
        "weather",
        "trend"
    ]

    # Document-related queries
    rag_keywords = [
        "document",
        "pdf",
        "uploaded",
        "policy",
        "handbook",
        "report",
        "file",
        "proposal"
    ]

    if any(word in query for word in web_keywords):
        return "🌐 Web Search"

    if any(word in query for word in rag_keywords):
        return "📄 RAG"

    return "🧠 LLM"



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

# Chat History
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask something...")

# Message Processing
if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route Query
    selected_tool = route_query(prompt)

    # Assistant Response
    with st.chat_message("assistant"):

        st.caption(f"Selected Tool: {selected_tool}")

        with st.spinner("Thinking..."):

            time.sleep(1)

            # Placeholder responses
            if selected_tool == "🌐 Web Search":

                response = f"""
I determined that this question requires **real-time information**.

Your query:

**{prompt}**

(Here you will later call DuckDuckGo Search.)
"""

            elif selected_tool == "📄 RAG":

                response = f"""
I determined that this question is related to **uploaded documents**.

Your query:

**{prompt}**

(Here you will later perform vector search using FAISS.)
"""

            else:

                response = f"""
I determined that this is a **general knowledge question**.

Your query:

**{prompt}**

(Here you will later call your LLM.)
"""

            st.markdown(response)

        # --------------------------------------------------
        # SOURCE PANEL
        # --------------------------------------------------

        with st.expander("📚 Sources"):

            if selected_tool == "🌐 Web Search":
                st.write("Web Search Results")
                st.write("DuckDuckGo Search (to be integrated)")

            elif selected_tool == "📄 RAG":
                st.write("Document Sources")
                st.write("Uploaded documents will appear here")

            else:
                st.write("LLM Internal Knowledge")

    # Sotring assistant message
    response = f"You asked: {prompt}"
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )