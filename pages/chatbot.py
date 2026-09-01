import streamlit as st
from rag.chatbot import ask_question
from gui.style import apply_style, page_header

apply_style()

page_header(
    "Production Planning Assistant",
    "Ask questions about the optimized production plans."
)

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Ask about the production plans..."
)

if question:
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing production plans..."):
            try:
                answer = ask_question(question)
                st.markdown(answer)

                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:
                st.error(
                    f"Error while generating the answer: {e}"
                )