import streamlit as st
from turtles import rag_chain

responses = []

def main():
    st.title("All About Turtles  🐢")
    with st.sidebar:
        st.markdown("## About Turtles 🐢")
        st.markdown("- Turtles are reptiles.")
        st.markdown("- They have a hard shell.")
        st.markdown("- There are many different species of turtles.")
        st.markdown("- They live in the ocean.")
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.markdown("Hello! I'm a turtle expert. Ask me anything about turtles.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # Accept user input
    if prompt := st.chat_input("Ask me anything about turtles"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        response = rag_chain.invoke(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        responses.append(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": responses[-1]})

if __name__ == "__main__":
    main()