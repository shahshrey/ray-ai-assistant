import os
import subprocess
import streamlit as st
import logging

from ..utils.utils import get_latest_artifacts_dir
from ..config.config import BASE_DIR, INPUT_DIR, OUTPUT_DIR

logger = logging.getLogger(__name__)

def check_indexing_status():
    if not os.path.exists(OUTPUT_DIR):
        return False
    if not get_latest_artifacts_dir(OUTPUT_DIR):
        return False
    return True

def perform_indexing():
    logger.info("Starting indexing process")
    st.info("Updating RAY's knowledge base...")
    subprocess.run(["python", "-m", "graphrag.index", "--root", BASE_DIR], check=True)
    logger.info("Indexing completed successfully")
    st.success("RAY's knowledge base has been successfully updated!")
    st.experimental_rerun()

def manage_input_files():
    col1, col2 = st.columns(2)
    with col1:
        input_files = os.listdir(INPUT_DIR)
        if input_files:
            selected_file = st.selectbox("Select File from RAY's Knowledge Base", [""] + input_files, key="input_file_select")
            if st.button("Remove File from RAY's Knowledge", key="delete_file_button"):
                os.remove(os.path.join(INPUT_DIR, selected_file))
                st.success(f"Removed {selected_file} from RAY's knowledge base")
                st.warning("File removed. Please update RAY's knowledge base.")
                if st.button("Update RAY's Knowledge Base", key="reindex_button"):
                    perform_indexing()
        else:
            st.info("RAY's knowledge base is empty. Please add files.")
    
    with col2:
        uploaded_file = st.file_uploader("Add New File to RAY's Knowledge Base", type=["txt"], key="file_uploader")
        if uploaded_file is not None:
            with open(os.path.join(INPUT_DIR, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Added {uploaded_file.name} to RAY's knowledge base.")
            st.warning("New information added. Please update RAY's knowledge base.")
            if st.button("Update RAY's Knowledge Base", key="reindex_button_new_file"):
                perform_indexing()