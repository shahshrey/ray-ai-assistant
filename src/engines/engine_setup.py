import streamlit as st
import tiktoken
import logging
from graphrag.query.llm.oai.chat_openai import ChatOpenAI as GraphRAGChatOpenAI
from graphrag.query.llm.oai.typing import OpenaiApiType

from ..config import ARTIFACTS_DIR
from ..data.data_loader import load_data, prepare_context
import os

logger = logging.getLogger(__name__)

@st.cache_resource
def load_environment_variables():
    return {
        "api_key": os.environ["GRAPHRAG_API_KEY"],
        "llm_model": os.environ["GRAPHRAG_LLM_MODEL"],
        "embedding_model": os.environ["GRAPHRAG_EMBEDDING_MODEL"],
        "artifacts_dir": ARTIFACTS_DIR
    }

@st.cache_resource
def initialize_llm_and_encoder(api_key, llm_model):
    llm = GraphRAGChatOpenAI(api_key=api_key, model=llm_model, api_type=OpenaiApiType.OpenAI, max_retries=20)
    token_encoder = tiktoken.get_encoding("cl100k_base")
    return llm, token_encoder

def setup_engines(config):
    logger.info("Setting up engines")
    env_vars = load_environment_variables()
    env_vars["api_key"] = config["api_key"]
    env_vars["artifacts_dir"] = config["artifacts_dir"]
    logger.info(f"Using artifacts directory: {env_vars['artifacts_dir']}")
    llm, token_encoder = initialize_llm_and_encoder(env_vars["api_key"], env_vars["llm_model"])
    data_frames = load_data(env_vars["artifacts_dir"])
    reports, entities, relationships, covariates, text_units = prepare_context(data_frames, config["community_level"])
    logger.info("Engines setup completed")

    return llm, token_encoder, env_vars, reports, entities, relationships, covariates, text_units