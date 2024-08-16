<div align="center">
  <a href="https://github.com/shahshrey/ray-ai-assistant">
    <img src="docs/images/logo.png" style="max-width: 500px" width="50%" alt="Logo">
  </a>
</div>

<div align="center">
  <em>An advanced AI assistant designed to help users interact with complex datasets and perform sophisticated searches using various AI-powered techniques, including Graph RAG and traditional RAG approaches.</em>
</div>

<br />

<div align="center">
  <a href="https://github.com/shahshrey/ray-ai-assistant/commits">
    <img src="https://img.shields.io/github/commit-activity/m/shahshrey/ray-ai-assistant" alt="git commit activity">

    <img src="https://img.shields.io/badge/License-MIT-yellow.svg?&color=3670A0" alt="License: MIT">
  </a>
</div>
<p align="center">
<a href="https://github.com/shahshrey/ray-ai-assistant">🖇️ Repository</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="#">📙 Documentation</a>
</p>

<br/>

# 🧠 RAY AI Assistant

RAY (Research Analysis Yielder) is a cutting-edge tool that integrates AI capabilities into your data analysis process. It leverages both Graph RAG and traditional RAG techniques to offer enhanced retrieval and generation capabilities. RAY provides global and local search modes, file management, and indexing capabilities, all through a Streamlit-based user interface.

## 🌟 Features

|                                       |                                                               |
| ------------------------------------- | ------------------------------------------------------------- |
| 🔍 **Advanced retrieval**             | Using Graph RAG and traditional RAG                           |
| 🌐 **Global and local search modes**  | For comprehensive data exploration                            |
| 🤖 **Integration with OpenAI**        | Leverages OpenAI's language models                            |
| 📂 **File management**                | Efficient file management and indexing capabilities           |
| 🖥️ **Streamlit-based UI**             | User-friendly interface for seamless interaction              |
| ⚙️ **Customizable search parameters** | Tailor search parameters to fit specific needs                |

### Graph RAG Advantages

RAY incorporates Graph RAG, a superior technique for retrieval that offers several benefits over traditional RAG:

- **Enhanced context understanding**: Graph RAG leverages knowledge graphs to capture complex relationships between entities, providing more accurate and contextually rich answers.
- **Improved handling of structured and unstructured data**: It excels at representing and retrieving heterogeneous and interconnected information.
- **Better performance in domain-specific queries**: Graph RAG addresses limitations of generic embedding models in company-specific knowledge retrieval.

## 🚀 Quick Start ⌨️

1. Clone the repository:
   ```bash
   git clone https://github.com/shahshrey/ray-ai-assistant.git
   cd ray_ai_assistant
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Copy the `.env.example` file to `.env`
   - Fill in your API keys and other configuration values

5. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

6. Open your web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501)

7. Use the sidebar to configure RAY and upload your documents

8. Ask questions and interact with RAY through the main interface, leveraging both Graph RAG and traditional RAG capabilities for comprehensive information retrieval

## 🗂️ Project Structure

- `src/`: Contains the main application code
- `tests/`: Contains test files (to be implemented)
- `docs/`: Contains additional documentation
- `main.py`: The entry point of the application
- `requirements.txt`: Lists all Python dependencies
- `.env.example`: Template for environment variables

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.