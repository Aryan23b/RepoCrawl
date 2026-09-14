import time
from huggingface_hub import InferenceClient
from config.settings import HUGGINGFACE_TOKEN, LLM_MODEL

class LLMService:
    def __init__(self):
        self.client = InferenceClient(api_key=HUGGINGFACE_TOKEN)

    @staticmethod
    def _build_prompt(question, results):
        context = "\n\n".join(
            f"FILE: {r['chunk'].path}\n"
            f"LINES: {r['chunk'].start_line}-{r['chunk'].end_line}\n\n"
            f"{r['chunk'].content}"
            for r in results
        )

        return f"""You are an AI assistant that answers questions about a GitHub repository.

Use ONLY the repository context below.
If the answer cannot be found, say:
"I could not find this information in the repository."

Do not invent files, classes, functions, APIs, or behavior.

REPOSITORY CONTEXT
==================
{context}

USER QUESTION
=============
{question}

ANSWER
======
"""

    def generate_answer(self, question, search_results):
        if not search_results:
            return "I could not find relevant information in the repository."

        prompt = self._build_prompt(question, search_results)
        last_error = None

        for attempt in range(3):
            try:
                response = self.client.chat_completion(
                    model=LLM_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=700,
                )
                return response.choices[0].message.content

            except Exception as exc:
                last_error = exc
                text = str(exc)
                temporary = any(
                    code in text for code in
                    ("429", "500", "502", "503", "504", "UNAVAILABLE")
                )
                if temporary and attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                break

        raise RuntimeError(f"Hugging Face model failed after retries: {last_error}")
