import streamlit as st
from datetime import datetime
from utils import upload_document, ask_question, check_api_connection, format_sources
from config import PAGE_TITLE, PAGE_ICON, LAYOUT, ALLOWED_FILE_TYPES, DEFAULT_TOP_K, MAX_TOP_K

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #667eea;
    }
    .assistant-message {
        background-color: #e8f4fd;
        border-left-color: #764ba2;
    }
    .upload-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_doc_id" not in st.session_state:
    st.session_state.current_doc_id = None
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

def main():
    # Header
    st.markdown('<h1 class="main-header">📚 StudyBuddy.ai</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI-powered study assistant for document-based Q&A")
    
    # Document Upload Section
    st.header("📁 Upload Document")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a document to upload",
            type=ALLOWED_FILE_TYPES,
            help="Supported formats: PDF, DOCX, TXT"
        )
    
    with col2:
        if uploaded_file is not None:
            if st.button("📤 Upload Document", type="primary", use_container_width=True):
                with st.spinner("Uploading and processing document..."):
                    result = upload_document(uploaded_file)
                    
                    if result:
                        st.session_state.current_doc_id = result["doc_id"]
                        st.session_state.uploaded_files.append({
                            "filename": result["filename"],
                            "doc_id": result["doc_id"],
                            "chunk_count": result["chunk_count"],
                            "upload_time": datetime.now()
                        })
                        st.success(f"✅ Document uploaded successfully!")
                        st.info(f"📄 {result['filename']} processed into {result['chunk_count']} chunks")
                        st.rerun()
    
    # Current Document and Settings Section
    if st.session_state.uploaded_files:
        st.header("📋 Document Management")
        
        # Create tabs for different sections
        tab1, tab2, tab3 = st.tabs(["📄 Current Document", "📚 All Documents", "⚙️ Settings"])
        
        with tab1:
            if st.session_state.current_doc_id:
                current_file = next((f for f in st.session_state.uploaded_files 
                                   if f['doc_id'] == st.session_state.current_doc_id), None)
                if current_file:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**📄 {current_file['filename']}**")
                    with col2:
                        st.write(f"**Chunks:** {current_file['chunk_count']}")
                    with col3:
                        st.write(f"**Uploaded:** {current_file['upload_time'].strftime('%Y-%m-%d %H:%M')}")
                else:
                    st.write(f"Document ID: `{st.session_state.current_doc_id}`")
            else:
                st.info("No document selected. Upload a document above to get started.")
        
        with tab2:
            st.subheader("📚 All Uploaded Documents")
            for i, file_info in enumerate(st.session_state.uploaded_files):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"📄 {file_info['filename']}")
                with col2:
                    st.write(f"{file_info['chunk_count']} chunks")
                with col3:
                    st.write(file_info['upload_time'].strftime('%Y-%m-%d %H:%M'))
                with col4:
                    if st.button(f"Select", key=f"select_{i}", use_container_width=True):
                        st.session_state.current_doc_id = file_info['doc_id']
                        st.success(f"Selected: {file_info['filename']}")
                        st.rerun()
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💬 Chat Settings")
                top_k = st.slider("Number of relevant chunks to use", 1, MAX_TOP_K, DEFAULT_TOP_K)
                
                if st.button("🗑️ Clear Chat History", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()
            
            with col2:
                st.subheader("🔗 API Status")
                if check_api_connection():
                    st.success("✅ Backend API is running")
                else:
                    st.error("❌ Backend API is not accessible")
                    st.info("Make sure to run: `uvicorn app.main:app --reload` in the backend directory")
                
                st.subheader("🤖 AI Configuration")
                st.info("Configure your AI provider in the backend `.env` file")
    
    # Chat Interface
    st.header("💬 Chat with Your Document")
    
    # Check if document is selected
    if not st.session_state.current_doc_id:
        st.info("👆 Please upload a document above to start asking questions.")
        return
    
    # Chat interface
    chat_container = st.container()
    
    # Display chat messages
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
                # Show sources for assistant messages
                if message["role"] == "assistant" and "sources" in message:
                    with st.expander("📚 Sources"):
                        for source in message["sources"]:
                            st.write(f"**Chunk {source.get('chunk', 'N/A')}** (Score: {source.get('score', 0):.3f})")
                            st.write(f"*{source.get('filename', 'Unknown file')}*")
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your document..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = ask_question(prompt, st.session_state.current_doc_id)
                
                if response:
                    answer = response["answer"]
                    sources = response["sources"]
                    used_chunks = response["used_chunks"]
                    
                    st.write(answer)
                    
                    # Show sources
                    with st.expander(f"📚 Sources ({used_chunks} chunks used)"):
                        for source in sources:
                            st.write(f"**Chunk {source.get('chunk', 'N/A')}** (Score: {source.get('score', 0):.3f})")
                            st.write(f"*{source.get('filename', 'Unknown file')}*")
                    
                    # Add assistant message to chat
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources
                    })
                else:
                    st.error("Failed to get response from AI. Please try again.")

if __name__ == "__main__":
    main()
