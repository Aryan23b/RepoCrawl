import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("huggingface_token")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
LLM_MODEL1 = "mistralai/Mistral-7B-Instruct-v0.3"
LLM_MODEL2 = "Qwen/Qwen2.5-Coder-32B-Instruct"


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 6
MAX_FILE_SIZE = 500_000


def validate_settings():
    missing = []
    if not GITHUB_TOKEN:
        missing.append("GITHUB_TOKEN")
    if not HUGGINGFACE_TOKEN:
        missing.append("HUGGINGFACE_TOKEN")
    if missing:
        raise ValueError(
            "Missing environment variable(s): "
            + ", ".join(missing)
            + "\n\nAdd them to your .env file."
        )
