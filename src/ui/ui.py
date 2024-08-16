import streamlit as st
from ..indexing.indexing import manage_input_files
from ..config.config import ARTIFACTS_DIR, API_KEY

def setup_page_config():
    st.set_page_config(
        page_title="RAY - Your Virtual AI Assistant",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/shahshrey/ray-ai-assistant',
            'Report a bug': "https://github.com/shahshrey/ray-ai-assistant/issues",
            'About': "RAY is an advanced AI assistant designed to help users interact with complex datasets."
        }
    )

def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        background-color: #121212;
        color: #E0E0E0;
    }

    .stApp {
        max-width: 100%;
        padding: 1rem;
    }

    .main .block-container {
        max-width: 100%;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .stSidebar .sidebar-content {
        background-color: #1E1E1E;
    }

    .stButton > button {
        background-color: #BB86FC;
        color: #000000;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: background-color 0.3s;
    }

    .stButton > button:hover {
        background-color: #3700B3;
        color: #FFFFFF;
    }

    .stTextInput > div > div > input {
        background-color: #2C2C2C;
        color: #E0E0E0;
        border: 1px solid #BB86FC;
        border-radius: 4px;
    }

    .stSelectbox > div > div > select {
        background-color: #2C2C2C;
        color: #E0E0E0;
        border: 1px solid #BB86FC;
        border-radius: 4px;
    }

    .stTab {
        background-color: #1E1E1E;
        color: #BB86FC;
    }

    .stTab[data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #2C2C2C;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .stTab[aria-selected="true"] {
        background-color: #BB86FC;
        color: #000000;
    }

    .stMarkdown a {
        color: #BB86FC;
    }

    .stMarkdown a:hover {
        color: #3700B3;
    }
    </style>
    """, unsafe_allow_html=True)

def setup_sidebar():
    st.sidebar.title("RAY Configuration")
    
    tabs = st.sidebar.tabs(["Input", "Model", "Search", "Advanced"])
    
    with tabs[0]:  # Input tab
        user_input = st.text_area("Ask RAY a question:", height=150)
        mode = st.selectbox(
            "Select Search Mode",
            ["global", "local", "vanilla"],
            help="Global: Broad knowledge. Local: Specific context. Vanilla: Basic RAG."
        )
        st.subheader("Manage RAY's Knowledge")
        manage_input_files()
    
    with tabs[1]:  # Model tab
        config = {}
        config["openai_model"] = st.selectbox("Select RAY's Language Model", ["gpt-4o", "gpt-4o-mini"], index=1)
        config["api_key"] = st.text_input("OpenAI API Key for RAY", value=API_KEY, type="password")
        config["temperature"] = st.slider("RAY's Creativity", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    
    with tabs[2]:  # Search tab
        config["allow_general_knowledge"] = st.checkbox("Allow General Knowledge", value=False)
        config["use_community_summary"] = st.checkbox("Use Community Summary", value=False)
        config["include_community_rank"] = st.checkbox("Include Community Rank", value=True)
        config["community_level"] = st.slider("Community Analysis Depth", min_value=0, max_value=5, value=2, step=1)
    
    with tabs[3]:  # Advanced tab
        config["artifacts_dir"] = st.text_input("Knowledge Base Directory", value=ARTIFACTS_DIR)
    
    return user_input, mode, config

def display_result(title, result):
    with st.expander(f"{title} Search Results", expanded=True):
        st.markdown(result['Response'])
        st.write(f"**Tokens:** {result['Tokens']}")
        st.write(f"**LLM Calls:** {result['LLM Calls']}")

def display_chat_interface(chat_history):
    st.markdown("### Chat History")
    
    formatted_history = format_chat_history(chat_history)
    st.markdown(formatted_history)
    
    user_message = st.text_input("Your message:", key="user_input")
    return user_message

def format_chat_history(chat_history):
    formatted_history = ""
    for entry in chat_history:
        role = entry['role']
        content = entry['content']
        if role == 'user':
            formatted_history += f"**You:**\n\n{content}\n\n"
        elif role == 'assistant':
            formatted_history += f"**RAY:**\n\n{content}\n\n"
    return formatted_history