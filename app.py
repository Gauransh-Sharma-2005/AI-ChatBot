import streamlit as st
from general_chat import ChatBot
from history_aware_generation import ask_question

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatBot()

# ==================================================
# ROUTER
# ==================================================

def route_query(query):

    query = query.lower()

    rag_keywords = [
        "document",
        "pdf",
        "policy",
        "handbook",
        "report",
        "proposal",
        "leave",
        "onboarding",
        "employee",
        "company",
        "department",
        "probation",
        "holiday"
    ]

    if any(word in query for word in rag_keywords):
        return "RAG"

    return "CHAT"

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🤖 AI Assistant")

    st.markdown("---")

    st.subheader("Features")

    st.success("🧠 General Chat")
    st.warning("📄 RAG Search")

    st.markdown("---")

    st.info(
        """
        Documents have already been
        ingested into ChromaDB.
        """
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        if "chatbot" in st.session_state:
            st.session_state.chatbot.reset()

        st.rerun()

# ==================================================
# HEADER
# ==================================================

st.title("🚀 Intelligent AI Assistant")

st.caption(
    "Automatic routing between General Chat and RAG"
)

# ==================================================
# DISPLAY OLD CHAT
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==================================================
# USER INPUT
# ==================================================

prompt = st.chat_input(
    "Ask me anything..."
)

if prompt:

    # Save user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Route query

    selected_tool = route_query(prompt)

    # Assistant response

    with st.chat_message("assistant"):

        st.caption(
            f"Selected Tool: {selected_tool}"
        )

        with st.spinner("Thinking..."):

            try:

                if selected_tool == "RAG":

                    response = ask_question(prompt)

                else:

                    response = (
                        st.session_state.chatbot
                        .chat(prompt)
                    )

            except Exception as e:

                response = (
                    f"❌ Error: {str(e)}"
                )

        st.markdown(response)

    # Save assistant response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )