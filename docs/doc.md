# RAY AI Assistant - Detailed Documentation

## 1. Introduction

RAY (Research Analysis Yielder) is an advanced AI assistant designed to help users interact with complex datasets and perform sophisticated searches using various AI-powered techniques. It leverages OpenAI's language models and provides a user-friendly interface through Streamlit.

## 2. Features

- Global and local search modes for versatile querying
- Integration with OpenAI's language models for advanced natural language processing
- File management and indexing capabilities for efficient data handling
- Streamlit-based user interface for easy interaction
- Customizable search parameters for fine-tuned results
- Community-based analysis and ranking system
- Ability to process and analyze various file types (PDF, PPTX, DOCX, CSV, TXT)

## 3. Setup and Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Step-by-step Installation

1. Clone the Repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a Virtual Environment (optional but recommended):
   ```
   python -m venv ray_env
   source ray_env/bin/activate  # On Windows, use: ray_env\Scripts\activate
   ```

3. Install Dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up Environment Variables:
   Create a `.env` file in the root directory with the following content:
   ```
   OPENAI_API_KEY=<your_openai_api_key>
   GRAPHRAG_API_KEY=<your_graphrag_api_key>
   GRAPHRAG_LLM_MODEL=<preferred_llm_model>
   GRAPHRAG_EMBEDDING_MODEL=<preferred_embedding_model>
   ```

5. Initialize the Knowledge Base:
   ```
   python -m graphrag.index --init --root brain
   ```

6. Run the Application:
   ```
   streamlit run main.py
   ```

## 4. Project Structure

The project is organized as follows:

- `main.py`: Entry point of the application
- `src/`: Contains the core application code
  - `config/`: Configuration files and settings
  - `data/`: Data loading and processing modules
  - `engines/`: Search engine setup and configuration
  - `indexing/`: File indexing and management
  - `ui/`: User interface components
  - `utils/`: Utility functions
- `docs/`: Documentation files
- `tests/`: Test files (if any)
- `requirements.txt`: List of Python dependencies
- `.gitignore`: Specifies intentionally untracked files to ignore

## 5. Configuration

The application can be configured through the `src/config/config.py` file and the Streamlit interface. Key configuration options include:

### Environment Variables (in `.env` file)
- `OPENAI_API_KEY`: Your OpenAI API key
- `GRAPHRAG_API_KEY`: Your GraphRAG API key
- `GRAPHRAG_LLM_MODEL`: Preferred language model (e.g., "gpt-4")
- `GRAPHRAG_EMBEDDING_MODEL`: Preferred embedding model

### Streamlit Interface Configuration

```9:34:src/ui/ui.py
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
```


These options allow users to customize various aspects of RAY's behavior directly from the UI.

## 6. Usage Guide

### 6.1 Adding Documents to RAY's Knowledge Base

1. Navigate to the "Input" tab in the sidebar.
2. Use the file uploader to add new documents (supported formats: TXT, PDF, DOCX, PPTX, CSV).
3. Once uploaded, click on "Update RAY's Knowledge Base" to index the new documents.

### 6.2 Configuring Search Parameters

1. In the "Model" tab:
   - Select the preferred language model
   - Adjust the temperature (creativity) of the model
2. In the "Search" tab:
   - Toggle general knowledge usage
   - Enable/disable community summary and rank
   - Adjust the community analysis depth

### 6.3 Performing Searches

1. In the "Input" tab, enter your question(s) in the text area.
2. Select the search mode (global, local, or vanilla).
3. Click the "Submit" button to process your query.
4. View the results in the main area, which will include:
   - The AI's response
   - Token usage
   - Number of LLM calls

### 6.4 Managing the Knowledge Base

1. In the "Input" tab, you can:
   - View existing files in the knowledge base
   - Remove files from the knowledge base
   - Add new files to the knowledge base
2. After any changes, remember to update the knowledge base by clicking the appropriate button.

## 7. Advanced Features

### 7.1 Global vs. Local Search

- Global Search: Provides broad knowledge across the entire dataset.
- Local Search: Focuses on specific context, useful for detailed queries about particular topics.

### 7.2 Community Analysis

RAY uses a community-based analysis system to rank and weight information. This can be adjusted using the "Community Analysis Depth" slider in the UI.

### 7.3 Custom Indexing

For advanced users, custom indexing can be performed by modifying the indexing process in:


```15:19:src/indexing/indexing.py
def perform_indexing():
    st.info("Updating RAY's knowledge base...")
    subprocess.run(["python", "-m", "graphrag.index", "--root", BASE_DIR], check=True)
    st.success("RAY's knowledge base has been successfully updated!")
    st.experimental_rerun()
```


## 8. Troubleshooting

### Common Issues and Solutions

1. **API Key Errors**: 
   - Ensure that your API keys are correctly set in the `.env` file.
   - Check if the keys are valid and have the necessary permissions.

2. **Indexing Failures**:
   - Verify that the input files are in the correct format and not corrupted.
   - Check the console for specific error messages.
   - Ensure you have sufficient disk space for indexing.

3. **Out of Memory Errors**:
   - Try reducing the `CHUNK_SIZE` and `MAX_TOKENS` values in `src/config/config.py`.
   - Process smaller batches of documents at a time.

4. **Slow Performance**:
   - Adjust the `CONCURRENT_COROUTINES` value in `src/config/config.py`.
   - Consider upgrading your hardware or using a more powerful cloud instance.

### Logging

To enable detailed logging for troubleshooting:

1. Modify `main.py` to include logging configuration:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG, filename='ray_debug.log')
   ```

2. Add logging statements in relevant parts of the code, e.g.:
   ```python
   logging.debug(f"Processing query: {query}")
   ```

3. Check the `ray_debug.log` file for detailed information when issues occur.

## 9. Contributing

Contributions to RAY AI Assistant are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write your code and tests.
4. Ensure all tests pass and the code adheres to the project's style guide.
5. Submit a pull request with a clear description of your changes.

## 10. License

RAY AI Assistant is licensed under the MIT License. This means you are free to use, modify, and distribute the software, provided that you include the original copyright notice and this permission notice in any copies or substantial portions of the software.

The full text of the MIT License is as follows.

## 11. Contact and Support

For questions, issues, or support, please [provide appropriate contact information or links to support resources].

This detailed documentation should provide a comprehensive guide to setting up, configuring, and using the RAY AI Assistant. It covers the main features, installation process, usage instructions, and troubleshooting tips, making it easier for users to get started and make the most of the application.