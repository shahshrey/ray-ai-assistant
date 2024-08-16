import os
import csv
import subprocess
from datetime import datetime
import streamlit as st
import json
import pandas as pd  # Added missing import for pandas
from langchain.schema import Document, HumanMessage

def initialize_directories(INPUT_DIR, PROMPTS_DIR, BASE_DIR):
    os.makedirs(INPUT_DIR, exist_ok=True)
    if not os.path.exists(PROMPTS_DIR) or len(os.listdir(PROMPTS_DIR)) != 4:
        st.info("Initializing RAY's knowledge base...")
        subprocess.run(["python", "-m", "graphrag.index", "--init", "--root", BASE_DIR], check=True)
        st.success("RAY's knowledge base initialized successfully.")

def get_latest_artifacts_dir(OUTPUT_DIR):
    if not os.path.exists(OUTPUT_DIR):
        return None
    subdirs = [d for d in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, d))]
    if not subdirs:
        return None
    latest_dir = max(subdirs, key=lambda x: os.path.getctime(os.path.join(OUTPUT_DIR, x)))
    artifacts_dir = os.path.join(OUTPUT_DIR, latest_dir, "artifacts")
    return artifacts_dir if os.path.exists(artifacts_dir) else None

def doc_to_message(doc: Document) -> HumanMessage:
    return HumanMessage(json.dumps(doc.page_content))

def save_results_to_csv(results, query, mode):
    st.info("Saving results to CSV...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results_df = pd.DataFrame({
        "Timestamp": [timestamp],
        "Query": [query],
        f"{mode.capitalize()} Search Response": [results.get("Response", "")],
        f"{mode.capitalize()} Search Tokens": [results.get("Tokens", 0)],
        f"{mode.capitalize()} Search LLM Calls": [results.get("LLM Calls", 0)]
    })

    file_path = "search_results.csv"
    if os.path.exists(file_path):
        results_df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        results_df.to_csv(file_path, mode='w', header=True, index=False)
    
    st.success("Results have been successfully saved to search_results.csv")
