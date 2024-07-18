import streamlit as st
from dotenv import load_dotenv
from ui import sidebar, chat_interface
from ChatWithYourData import process_pdf, get_conversation_chain


st. set_page_config(layout="wide")

def initialize_session_state():
    """
    Initializes necessary keys in Streamlit's session state if they are not already present
    """
    if 'conversation' not in st.session_state:
        st.session_state.conversation = None
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False

def main():
    """
    Main function for the Streamlit app
    """
    load_dotenv()
    
    initialize_session_state()
    
    # Sidebar components
    uploaded_file, db_choice, submitted = sidebar()
    
    # Main content area
    st.title("📚 Chat with your PDF")
    
    if uploaded_file is not None and not st.session_state.pdf_processed and submitted:
        try:
            with st.spinner(f"Processing PDF using {db_choice}..."):
                vectorstore = process_pdf(uploaded_file, db_choice)
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.session_state.pdf_processed = True
            with st.sidebar:
                st.success(f"PDF processed successfully using {db_choice}!")
        except Exception as e:
            st.error(f"An error occurred while processing the PDF with {db_choice}. Please try again.")
    
    # Chat interface
    if st.session_state.pdf_processed:
        chat_interface()

if __name__ == '__main__':
    main()