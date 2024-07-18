import streamlit as st

def sidebar():
    with st.sidebar:
        st.title("📚 Chat with your PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                st.success("PDF successfully uploaded!")
            else:
                st.error("Invalid PDF file. Please upload a valid PDF.")
                uploaded_file = None

        
        db_choice = st.radio(
            "Choose Vector Store:",
            ("Local (FAISS)", "HANA DB")
        )
        db_choice = "HANA" if db_choice == "HANA DB" else "FAISS"

        submitted = st.button('Process PDF')

        if st.session_state.pdf_processed:
            st.success(f"PDF processed successfully using {db_choice}!")
        
    return uploaded_file, db_choice, submitted

def chat_interface():
    # set initial message
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to 📚 Chat with your PDF, please ask a question about your document"}
        ]

    # display messages
    if "messages" in st.session_state.keys():
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "🧑‍💼"):
                st.write(message["content"])


    # get user input
    user_prompt = st.chat_input()


    if user_prompt is not None:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user", avatar="🧑‍💼"):
            st.write(user_prompt)


    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Loading..."):
                ai_response = st.session_state.conversation.invoke({"question": user_prompt}).get("answer")
                st.write(ai_response)
                
        new_ai_message = {"role": "assistant", "content": ai_response}
        st.session_state.messages.append(new_ai_message)