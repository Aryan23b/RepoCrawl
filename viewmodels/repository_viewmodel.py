class RepositoryViewModel:
    def __init__(self, github_service, document_service, embedding_service):
        self.github_service = github_service
        self.document_service = document_service
        self.embedding_service = embedding_service

    def load_repository(self, repo_input):
        repo_name = self.github_service.extract_repo_name(repo_input)

        if not repo_name:
            raise ValueError(
                "Invalid GitHub repository. Use https://github.com/owner/repository "
                "or owner/repository."
            )

        repo, github_files = self.github_service.get_source_files(repo_name)
        documents = self.document_service.process_files(github_files)

        if not documents:
            raise ValueError("No supported source files were found.")

        chunks = self.document_service.create_chunks(documents)
        embeddings = self.embedding_service.create_embeddings(chunks)

        return {
            "repository": self.github_service.get_repository_info(repo),
            "documents": documents,
            "chunks": chunks,
            "embeddings": embeddings,
        }
