# RepoCrawl

**Talk to a GitHub repo like you'd talk to the person who wrote it.**

🔗 **Live app:** [repocrawl.streamlit.app](https://repocrawl.streamlit.app/)

Every codebase has that one engineer you go find when you need to understand something fast — "where's auth handled?", "why does this service call that one?", "what's actually going on in this 800-line class?" RepoCrawl is my attempt to put that person on call 24/7, for any public repo, using nothing but retrieval-augmented generation and open models.

Point it at a GitHub URL, and it reads the codebase, chunks it up, embeds it, and lets you ask it questions in plain English. It answers from the actual source — not from vibes — and shows you exactly which files it pulled the answer from.

```
"Where is authentication implemented?"
"Walk me through the service layer."
"How does this app handle API errors?"
"Which class owns the database access?"
"Where else is this function called?"
```

---

## Why I built it

I got tired of the ritual of cloning a new repo, opening fifteen tabs, and grep-ing my way to an understanding of a codebase before I could make a useful change. Most of that time isn't spent thinking — it's spent *searching*. RAG is a pretty natural fit for that problem: the repo is the knowledge base, your question is the query, and the LLM's job is just to read the right five files and explain them well.

RepoCrawl is that idea, built as a small, honest tool rather than a black box. It's deliberately simple under the hood so you can see (and trust) exactly what context the model is working from.

## How RepoCrawl Works

RepoCrawl uses a Retrieval-Augmented Generation (RAG) architecture.

The high-level pipeline is:
```

                GitHub Repository
                       │
                       ▼
                GitHub API
                       │
                       ▼
                Source Files
                       │
                       ▼
               Document Processing
                       │
                       ▼
                 Code Chunking
                       │
                       ▼
             Sentence Transformers
                       │
                       ▼
                 Vector Embeddings
                       │
                       ▼
                 Indexed Repository
                       │
                       │
              User asks a question
                       │
                       ▼
              Query Embedding
                       │
                       ▼
               Similarity Search
                       │
                       ▼
              Top Relevant Chunks
                       │
                       ▼
                RAG Prompt
                       │
                       ▼
                Qwen LLM
                       │
                       ▼
                Generated Answer
                       │
                       ▼
              Answer + Sources
```

## Under the hood

| Component | Choice | Why |
|---|---|---|
| Language | Python | fast to iterate on a RAG pipeline |
| UI | Streamlit | ships a usable interface without writing a frontend |
| GitHub access | PyGithub | clean wrapper over the GitHub API |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) | small, fast, good enough for code/doc semantic search, runs on CPU |
| Similarity search | NumPy | no need for a vector DB at this scale — cosine similarity over an array is plenty |
| LLM | Qwen2.5-Coder-7B-Instruct via Hugging Face | code-tuned, strong at reasoning over source, and free to call via the Inference API |
| Architecture | MVVM-inspired | keeps Streamlit's UI code from tangling with the retrieval/LLM logic |

## Project layout

```
RepoCrawl/
├── app.py            entry point — wires everything together
├── config/           settings & secrets loading
├── models/           plain data structures passed between layers
├── services/         GitHub, chunking, embeddings, retrieval, LLM
├── viewmodels/        orchestrates services for the UI (no Streamlit imports here)
├── views/             Streamlit UI — thin, no business logic
├── .streamlit/
├── requirements.txt
└── README.md
```

The rule I held myself to: `views` should only ever call into `viewmodels`, and `viewmodels` should only ever call into `services`. If you ever catch a Streamlit import inside `services/`, that's a bug — it means the layers have started bleeding into each other, which is exactly what this structure is meant to prevent.

## Getting it running

Want to try it without installing anything? Just use the live app: **[repocrawl.streamlit.app](https://repocrawl.streamlit.app/)**

To run it locally instead:

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/RepoCrawl.git
cd RepoCrawl

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your secrets
```

Create a `.env` file:

```env
GITHUB_TOKEN=your_github_token
HUGGINGFACE_TOKEN=your_huggingface_token
```

```bash
# 5. Run it
streamlit run app.py
```

Open the app, drop in a repo URL (`https://github.com/owner/repository`), hit **🚀 Load Repository**, and start asking questions once it's indexed.

## Deploying it

RepoCrawl is set up to run as-is on **Streamlit Community Cloud** — that's exactly how the [live version](https://repocrawl.streamlit.app/) is hosted. Just add the same two secrets in your deployment settings:

```
GITHUB_TOKEN
HUGGINGFACE_TOKEN
```

## About this project

RepoCrawl is a personal project exploring RAG, semantic code search, embeddings, and LLM-backed developer tooling — built by **Aryan Baranwal**.

Try it live at **[repocrawl.streamlit.app](https://repocrawl.streamlit.app/)** — if it's useful to you, a star helps others find it, and I'm always glad to hear what breaks or what you'd want it to do next.
