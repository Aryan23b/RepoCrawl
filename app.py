import streamlit as st

from config.settings import validate_settings
from services.github_service import GitHubService
from services.document_service import DocumentService
from services.embedding_service import EmbeddingService
from services.retrieval_service import RetrievalService
from services.llm_service import LLMService
from viewmodels.repository_viewmodel import RepositoryViewModel
from viewmodels.chat_viewmodel import ChatViewModel
from views.sidebar import render_sidebar
from views.repository_view import render_repository
from views.chat_view import render_chat

st.set_page_config(page_title="GitHub AI Chat", page_icon="💻", layout="wide")
st.title("💻 Chat with GitHub Repository")
st.write("Enter a GitHub repository and ask questions about its code.")

try:
    validate_settings()
except ValueError as exc:
    st.error(str(exc))
    st.stop()

github_service = GitHubService()
document_service = DocumentService()
embedding_service = EmbeddingService()
retrieval_service = RetrievalService(embedding_service)
llm_service = LLMService()

repository_vm = RepositoryViewModel(
    github_service, document_service, embedding_service
)
chat_vm = ChatViewModel(retrieval_service, llm_service)

defaults = {
    "repo_loaded": False,
    "current_repo": None,
    "documents": [],
    "embeddings": None,
    "messages": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

try:
    github_user = github_service.authenticate()
except Exception as exc:
    st.error(f"❌ GitHub authentication failed:\n\n{exc}")
    st.stop()

repo_input, load_clicked = render_sidebar(github_user)

if load_clicked:
    if not repo_input.strip():
        st.warning("⚠️ Please enter a GitHub repository.")
    else:
        try:
            with st.spinner("📥 Processing repository..."):
                result = repository_vm.load_repository(repo_input)

            st.session_state.documents = result["chunks"]
            st.session_state.embeddings = result["embeddings"]
            st.session_state.current_repo = result["repository"]
            st.session_state.repo_loaded = True
            st.session_state.messages = []

            st.success(
                f"✅ Loaded {result['repository'].full_name} "
                f"with {len(result['chunks'])} indexed chunks."
            )
            st.rerun()
        except ValueError as exc:
            st.error(f"❌ {exc}")
        except Exception as exc:
            st.error(f"❌ Failed to load repository:\n\n{exc}")

if st.session_state.repo_loaded:
    render_repository(
        st.session_state.current_repo,
        st.session_state.documents,
    )
    render_chat(chat_vm)
else:
    st.info("👈 Enter a GitHub repository in the sidebar and click **Load Repository**.")
    st.markdown("### Example\n```text\nhttps://github.com/openai/openai-python\n```")
