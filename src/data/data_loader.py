import pandas as pd
import streamlit as st
from graphrag.query.indexer_adapters import (
    read_indexer_entities, read_indexer_reports, read_indexer_relationships,
    read_indexer_covariates, read_indexer_text_units
)
import os
@st.cache_data
def load_data(artifacts_dir):
    table_names = {
        "community_report": "create_final_community_reports",
        "entity": "create_final_nodes",
        "entity_embedding": "create_final_entities",
        "relationship": "create_final_relationships",
        "covariate": "create_final_covariates",
        "text_unit": "create_final_text_units"
    }
    
    return {name: pd.read_parquet(f"{artifacts_dir}/{filename}.parquet") for name, filename in table_names.items()}

@st.cache_data
def prepare_context(data_frames, community_level):
    reports = read_indexer_reports(data_frames['community_report'], data_frames['entity'], community_level)
    entities = read_indexer_entities(data_frames['entity'], data_frames['entity_embedding'], community_level)
    relationships = read_indexer_relationships(data_frames['relationship'])
    claims = read_indexer_covariates(data_frames['covariate'])
    covariates = {"claims": claims}
    text_units = read_indexer_text_units(data_frames['text_unit'])
    return reports, entities, relationships, covariates, text_units
