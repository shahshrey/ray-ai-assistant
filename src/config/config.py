import os
from dotenv import load_dotenv

from src.utils.utils import get_latest_artifacts_dir

load_dotenv()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'brain'))
INPUT_DIR = f"{BASE_DIR}/input"
OUTPUT_DIR = f"{BASE_DIR}/output"
PROMPTS_DIR = f"{BASE_DIR}/prompts"
API_KEY = os.getenv("OPENAI_API_KEY")
SSL_CERT_PATH = '/opt/homebrew/etc/openssl@3/cert.pem'
CHUNK_SIZE = 300
CHUNK_OVERLAP = 200
MAX_TOKENS_GLOBAL = 12_000
MAX_TOKENS_LOCAL = 2_000
TEMPERATURE = 0.0
RESPONSE_TYPE = "multiple paragraphs"
CONCURRENT_COROUTINES = 32
RETRIEVER_TYPES = ('*.pdf', '*.pptx', '*.docx', '*.csv', '*.txt')
VECTORSTORE_DIR = './chromadb'
COLLECTION_NAME = 'knowledge_base_docs'
ARTIFACTS_DIR = get_latest_artifacts_dir(OUTPUT_DIR)
