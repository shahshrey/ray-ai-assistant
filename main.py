import asyncio
import streamlit as st
from src.config.config import INPUT_DIR, PROMPTS_DIR, BASE_DIR
from src.engines import setup_engines, setup_search_engines
from src.ui.ui import setup_page_config, apply_custom_css, setup_sidebar, display_result, display_chat_interface
from src.indexing.indexing import check_indexing_status, perform_indexing
from src.utils.utils import initialize_directories, save_results_to_csv
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='ray.log')
logger = logging.getLogger(__name__)

async def process_query(query, search_engine, mode):
    logger.info(f"Processing query: {query} in {mode} mode")
    with st.spinner("RAY is processing your query..."):
        search_query = f"{query} Please format your answer in markdown."
        response = await search_engine.asearch(search_query)
    
    logger.info(f"Query processed. Tokens: {response.prompt_tokens}, LLM Calls: {response.llm_calls}")
    return {
        "Response": response.response,
        "Tokens": response.prompt_tokens,
        "LLM Calls": response.llm_calls
    }

def main():
    logger.info("Starting RAY application")
    setup_page_config()
    apply_custom_css()
    
    initialize_directories(INPUT_DIR, PROMPTS_DIR, BASE_DIR)
    
    st.sidebar.title("RAY Configuration")
    user_input, mode, config = setup_sidebar()
    
    files_exist = bool(os.listdir(INPUT_DIR))
    indexing_status = check_indexing_status()
    
    if not files_exist:
        st.warning("No files in RAY's knowledge base. Please add files.")
        uploaded_file = st.file_uploader("Upload New File", type=["txt"])
        if uploaded_file is not None:
            logger.info(f"File uploaded: {uploaded_file.name}")
            with open(os.path.join(INPUT_DIR, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} has been uploaded. You can now perform indexing.")
            files_exist = True
            st.experimental_rerun()
    
    if files_exist and not indexing_status:
        st.warning("Indexing is required. Please perform indexing before proceeding.")
        if st.button("Perform Indexing"):
            logger.info("Performing indexing")
            perform_indexing()
        return

    logger.info(f"User selected mode: {mode}")

    try:
        logger.info("Setting up engines")
        llm, token_encoder, env_vars, reports, entities, relationships, covariates, text_units = setup_engines(config)
        global_search_engine, local_search_engine = setup_search_engines(llm, token_encoder, reports, entities, relationships, covariates, text_units, env_vars, config)
    except Exception as e:
        logger.error(f"Error setting up search engines: {str(e)}", exc_info=True)
        st.error(f"Error setting up search engines: {str(e)}")
        st.error("This might be due to missing or corrupted index files. Please try to integrate the knowledge into RAY's brain.")
        if st.button("Integrate the knowledge into RAY's Brain"):
            logger.info("Performing indexing after setup error")
            perform_indexing()
        return

    st.title("Chat with RAY")
    
    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat interface
    user_message = display_chat_interface(st.session_state.chat_history)

    if user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        
        if mode == "global":
            logger.info(f"Processing global query: {user_message}")
            result = asyncio.run(process_query(user_message, global_search_engine, mode))
        else:
            logger.info(f"Processing local query: {user_message}")
            result = asyncio.run(process_query(user_message, local_search_engine, mode))
        
        st.session_state.chat_history.append({"role": "assistant", "content": result['Response']})
        
        # Display the latest result
        display_result(mode.capitalize(), result)
        
        # Save results to CSV
        save_results_to_csv(result, user_message, mode)

    logger.info("RAY application finished processing")

if __name__ == "__main__":
    main()