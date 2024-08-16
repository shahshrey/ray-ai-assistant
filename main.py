import asyncio
import streamlit as st
from src.config.config import INPUT_DIR, PROMPTS_DIR, BASE_DIR
from src.engines import setup_engines, setup_search_engines
from src.ui.ui import setup_page_config, setup_sidebar, display_result
from src.indexing.indexing import check_indexing_status, perform_indexing
from src.utils.utils import initialize_directories, save_results_to_csv
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='ray.log')
logger = logging.getLogger(__name__)

async def process_query(query, search_engine, mode):
    logger.info(f"Processing query: {query} in {mode} mode")
    st.info(f"RAY is processing your query: {query}")
    
    search_query = f"{query} Please format your answer in markdown."
    response = await search_engine.asearch(search_query)
    
    logger.info(f"Query processed. Tokens: {response.prompt_tokens}, LLM Calls: {response.llm_calls}")
    return {
        "Response": response.response,
        "Tokens": response.prompt_tokens,
        "LLM Calls": response.llm_calls
    }

def process_and_display_results(query, search_engine, mode):
    with st.spinner("Processing..."):
        results = asyncio.run(process_query(query, search_engine, mode))

    display_result(mode.capitalize(), results)
    save_results_to_csv(results, query, mode)

def main():
    logger.info("Starting RAY application")
    setup_page_config()
    
    initialize_directories(INPUT_DIR, PROMPTS_DIR, BASE_DIR)
    
    files_exist = bool(os.listdir(INPUT_DIR))
    
    if not files_exist:
        logger.warning("No files in the input folder")
        st.warning("No files in the input folder. Please add files.")
        uploaded_file = st.file_uploader("Upload New File", type=["txt"])
        if uploaded_file is not None:
            logger.info(f"File uploaded: {uploaded_file.name}")
            with open(os.path.join(INPUT_DIR, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} has been uploaded. You can now perform indexing.")
            files_exist = True
            st.experimental_rerun()
    
    indexing_status = check_indexing_status()
    logger.info(f"Indexing status: {indexing_status}")

    if files_exist and not indexing_status:
        st.warning("Indexing is required. Please perform indexing before proceeding.")
        if st.button("Perform Indexing"):
            logger.info("Performing indexing")
            perform_indexing()
        return

    user_input, mode, config = setup_sidebar()
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

    if st.sidebar.button("Submit"):
        questions = [q.strip() for q in user_input.split('\n') if q.strip()]
        logger.info(f"Processing {len(questions)} questions")
        
        for query in questions:
            st.subheader(f"Query: {query}")
            if mode == "global":
                logger.info(f"Processing global query: {query}")
                process_and_display_results(query, global_search_engine, mode)
            else:
                logger.info(f"Processing local query: {query}")
                process_and_display_results(query, local_search_engine, mode)

    logger.info("RAY application finished processing")

if __name__ == "__main__":
    main()