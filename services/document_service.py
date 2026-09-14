import os
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP, MAX_FILE_SIZE
from models.chunk import CodeChunk

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".kt", ".kts",
    ".cpp", ".cc", ".c", ".h", ".hpp",
    ".cs", ".go", ".rs", ".php",
    ".html", ".css", ".scss",
    ".json", ".xml", ".yaml", ".yml",
    ".sql", ".md", ".txt", ".properties", ".gradle"
}

IGNORED_DIRECTORIES = {
    ".git", ".github", "node_modules", "__pycache__",
    ".venv", "venv", "dist", "build", "target", ".idea"
}

class DocumentService:
    def should_include_file(self, path: str) -> bool:
        parts = path.lower().split("/")
        if any(directory in parts for directory in IGNORED_DIRECTORIES):
            return False
        return os.path.splitext(path.lower())[1] in ALLOWED_EXTENSIONS

    def process_files(self, github_files):
        documents = []
        for file in github_files:
            if not self.should_include_file(file.path):
                continue
            if file.size and file.size > MAX_FILE_SIZE:
                continue
            try:
                content = file.decoded_content.decode("utf-8", errors="ignore")
                if content.strip():
                    documents.append({"path": file.path, "content": content})
            except Exception:
                continue
        return documents

    def chunk_document(self, path, content, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
        if overlap >= chunk_size:
            raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE.")

        lines = content.splitlines()
        chunks = []
        start = 0

        while start < len(lines):
            end = min(start + chunk_size, len(lines))
            text = "\n".join(lines[start:end])

            if text.strip():
                chunks.append(CodeChunk(
                    path=path,
                    content=text,
                    start_line=start + 1,
                    end_line=end,
                ))

            if end == len(lines):
                break
            start = end - overlap

        return chunks

    def create_chunks(self, documents):
        chunks = []
        for document in documents:
            chunks.extend(self.chunk_document(
                document["path"], document["content"]
            ))
        return chunks
