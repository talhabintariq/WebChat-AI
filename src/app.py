# Import necessary libraries and setup environment
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from chatbot.bot import get_vectorstore_from_url, get_response

load_dotenv()

# Configure Streamlit app
st.set_page_config(
    page_title="Web Chat Assistant",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/chat-with-web',
        'Report a bug': "https://github.com/yourusername/chat-with-web/issues",
        'About': """
        # Web Chat Assistant
        An AI-powered chat interface for website content.
        Built with Streamlit and LangChain.
        """
    }
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        max-width: 1200px;
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 WebChat AI")

# Create sidebar for website URL input
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")
    depth_of_child_pages = st.number_input("Depth of Child Pages", min_value=1, value=1)
    
if website_url is None or website_url == "":
    st.info("Please enter a website URL")
else:
    try:
        with st.status("Processing website...", expanded=True) as status:
            st.write(f"🌐 Target URL: {website_url}")
            st.write(f"📊 Crawling depth: {depth_of_child_pages}")
            status.update(label="⏳ Extracting content from website...")
            
            with st.spinner('Please wait while we process the website...'):
                if "vector_store" not in st.session_state:
                    st.session_state.vector_store = get_vectorstore_from_url(website_url, depth_of_child_pages)
                st.progress(1.0, "Completed!")
                
            st.success(f"✅ Successfully processed {website_url}")
    except Exception as e:
        st.error(f"❌ Error processing URL: {str(e)}")

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="""
            👋 Welcome! I'm your WebChat Assistant.
            """)
        ]
    
    # Process user input and generate response
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        response = get_response(user_query)
        
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))
        
    # Display chat history with appropriate avatars
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)
