class ChatViewModel:
    def __init__(self, retrieval_service, llm_service):
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    def ask(self, question, chunks, embeddings):
        sources = self.retrieval_service.search(
            question, chunks, embeddings
        )
        answer = self.llm_service.generate_answer(question, sources)

        return {"answer": answer, "sources": sources}
