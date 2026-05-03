# TraceX AI

> An AI-powered codebase understanding assistant built with FastAPI, React, and Hybrid RAG.

TraceX AI lets you ingest any local or GitHub repository and ask natural language questions about it — architecture, data flow, function locations, and impact analysis — powered by AST-aware chunking, hybrid retrieval (FAISS + BM25), dependency graph traversal, and Groq AI generation.

---

## Features

- **Hybrid RAG** — Combines dense semantic search (FAISS) with keyword search (BM25) for high-precision retrieval
- **AST-Aware Chunking** — Parses Python/JS code at function and class level, not arbitrary character splits
- **Dependency Graph** — Builds a cross-file dependency graph to enrich context with related code
- **4 Query Modes** — Explain, Flow, Navigate, Impact
- **GitHub Ingestion** — Paste a public GitHub URL to clone and index automatically
- **Context Panel** — Shows exactly which files and code chunks the AI used to answer
- **Light / Dark Mode** — Full theme support

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Zustand |
| Backend | FastAPI, Python 3.10+ |
| Embeddings | Sentence Transformers |
| Vector Store | FAISS |
| Keyword Search | BM25 (rank-bm25) |
| LLM | Groq AI (xAI API) |
| Parsing | Python AST, Tree-sitter |
| Logging | Loguru |

---

## Prerequisites

- Python 3.10+
- Node.js 18+
- Git (required for GitHub URL ingestion)
- Groq AI API key from [console.groq.com](https://console.groq.com)

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/TraceX.git
cd TraceX
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables

Copy the example file and fill in your values:

```bash
# Windows
copy .env.example .env

# Linux / Mac
cp .env.example .env
```

Then open `.env` and set your Groq API key:

```env
GROQ_API_KEY=your_actual_key_here
```

> **Get your Groq API key:** Sign up at [console.groq.com](https://console.groq.com) → API Keys → Create new key. It is free to use.
>
> **Never commit `.env` to Git.** It is listed in `.gitignore` and will not be pushed. Only `.env.example` (with no real values) is committed as a reference for other developers.

### 4. Start the Backend

```bash
python main.py
```

The API will be available at `http://localhost:8000`.  
API docs available at `http://localhost:8000/docs`.

### 5. Frontend Setup

```bash
cd tracex-frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## API Reference

### `POST /api/v1/index`

Index a repository.

```json
// Local path
{
  "repo_path": "D:\\Projects\\my-repo"
}

// GitHub URL
{
  "github_url": "https://github.com/username/repository"
}
```

**Response:**
```json
{
  "status": "indexed",
  "total_files": 42,
  "total_chunks": 318,
  "source": "D:\\Projects\\my-repo"
}
```

---

### `POST /api/v1/query`

Query the indexed repository.

```json
{
  "query": "How does authentication work?",
  "query_type": "explain",
  "top_k": 5
}
```

**Query types:** `explain` | `flow` | `navigate` | `impact`

**Response:**
```json
{
  "query_type": "explain",
  "answer": "**Overview**\n...\n**Location**\n...",
  "sections": [],
  "references": [
    { "file": "auth/middleware.py", "snippet": "...", "score": 0.91 }
  ],
  "navigation_hints": [],
  "usages": []
}
```

---

## Usage

1. Start both backend and frontend servers
2. Open `http://localhost:5173`
3. Click **+ Ingest Repository** in the sidebar
4. Enter a local path (`D:\Projects\my-repo`) or a public GitHub URL
5. Press **Enter** or click **Index Repository**
6. Once indexed (green status indicator), type your question
7. Select a query mode: **Explain**, **Flow**, **Navigate**, or **Impact**
8. Press **Enter** or click **Send**
9. Toggle **Context Panel** to see which files were used to generate the answer

---

## Query Modes Explained

| Mode | Use When You Want To |
|---|---|
| **Explain** | Understand what a module, class, or function does |
| **Flow** | Trace how data moves from input to output |
| **Navigate** | Find where specific logic is implemented |
| **Impact** | Understand what would break if you changed something |

---

## Requirements

```txt
fastapi
uvicorn
pydantic
loguru
sentence-transformers
faiss-cpu
rank-bm25
python-dotenv
gitpython
requests
groq
```

> Install all with: `pip install -r requirements.txt`

---

## Contributing

Contributions are welcome! Here's how to get started:

### Fork and Clone

```bash
# 1. Fork the repo on GitHub (click Fork top-right)

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/TraceX.git
cd TraceX

# 3. Add upstream remote
git remote add upstream https://github.com/original-username/TraceX.git
```

### Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### Make Changes and Commit

```bash
git add .
git commit -m "feat: add your feature description"
```

### Push and Open a PR

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub from your fork to the main repo.

### Contribution Guidelines

- Follow existing code style (no emojis in UI, inline styles for React components)
- Keep backend modules single-responsibility
- Test your changes against at least one local repo before submitting
- Add a clear description in your PR explaining what and why

### Good First Issues

- Add streaming response support for LLM output
- Add support for more languages in AST parser (Java, Go, Rust)
- Persist chat sessions to localStorage
- Add export chat as Markdown feature
- Implement dependency graph visualization in the Context Panel

---

## Author

Built by **Vighnesh** — AI/ML Engineer

---

## License

MIT License. See `LICENSE` for details.
