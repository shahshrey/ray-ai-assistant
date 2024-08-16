import streamlit as st
from ..indexing.indexing import manage_input_files
from ..config.config import ARTIFACTS_DIR, API_KEY
def setup_page_config():
    st.set_page_config(page_title="RAY - Your Virtual AI Assistant", layout="wide", initial_sidebar_state="expanded")
    st.title("RAY - Your Virtual AI Assistant")
    st.markdown("<style>body { background-color: #f0f2f6; }</style>", unsafe_allow_html=True)

def setup_sidebar():
    st.sidebar.title("RAY Configuration")
    tabs = st.sidebar.tabs(["Input", "Model", "Search", "Advanced"])
    with tabs[0]:  # Input tab
        user_input = st.text_area("Ask RAY a question (or multiple questions, one per line):")
        mode = st.selectbox("Select Search Mode", ["global", "local", "vanilla"], help="Global: Broad knowledge. Local: Specific context. Vanilla: Basic RAG.")
        st.subheader("Manage RAY's Knowledge")
        
        manage_input_files()
    
    with tabs[1]:  # Model tab
        config = {}
        config["openai_model"] = st.selectbox("Select RAY's Language Model", ["gpt-4o", "gpt-4o-mini"], index=1)
        config["api_key"] = st.text_input("OpenAI API Key for RAY", value=API_KEY, type="password")
        config["temperature"] = st.slider("RAY's Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    
    with tabs[2]:  # Search tab
        config["allow_general_knowledge"] = st.checkbox("Allow RAY to Use General Knowledge", value=False)
        config["use_community_summary"] = st.checkbox("Use Community Summary in RAY's Responses", value=False)
        config["include_community_rank"] = st.checkbox("Include Community Rank in RAY's Analysis", value=True)
        config["community_level"] = st.slider("RAY's Community Analysis Depth", min_value=0, max_value=5, value=2, step=1)
    
    with tabs[3]:  # Advanced tab
        config["artifacts_dir"] = st.text_input("RAY's Knowledge Base Directory", value=ARTIFACTS_DIR)
    
    return user_input, mode, config

def display_result(title, result):
    with st.expander(f"{title} Search - Click to expand"):
        st.markdown(f"### {title} Search", unsafe_allow_html=True)
        st.markdown(f"{result['Response']}")
        st.write(f"**Tokens:** {result['Tokens']}")
        st.write(f"**LLM Calls:** {result['LLM Calls']}")
