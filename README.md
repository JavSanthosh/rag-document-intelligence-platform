# 🤖 Multi-Agent RAG Document Intelligence Platform

Ask questions about any PDF or document using AI.  
Built with LangChain · ChromaDB · FastAPI · Docker · OpenAI

---

## 🧠 How This Project Works (Simple Explanation)

```
You upload a PDF
       ↓
System splits it into small chunks (e.g., 50 chunks from a 10-page PDF)
       ↓
Each chunk is converted to numbers (embeddings) using OpenAI
       ↓
Numbers are stored in ChromaDB (vector database on your computer)
       ↓
You ask a question
       ↓
Question is also converted to numbers
       ↓
ChromaDB finds the 3 most similar chunks to your question
       ↓
Those 3 chunks + your question are sent to GPT-3.5
       ↓
GPT-3.5 reads the chunks and answers your question
```

This is called **RAG (Retrieval Augmented Generation)** — the model doesn't guess, it reads YOUR document.

---

## 📁 Project Structure

```
rag-platform/
├── main.py              ← FastAPI app (API endpoints - the "doors" to your system)
├── rag_chain.py         ← Core RAG logic (LangChain + ChromaDB + OpenAI)
├── requirements.txt     ← All Python packages needed
├── Dockerfile           ← Instructions to build Docker container
├── docker-compose.yml   ← Run everything with one command
├── .env.example         ← Template for your API key
└── README.md            ← This file
```

---

## 🚀 Step-by-Step Setup (Follow in Order)

### STEP 1 — Install Required Tools

Install these on your computer if you don't have them:

1. **Python 3.11** → https://python.org/downloads
2. **Docker Desktop** → https://docker.com/products/docker-desktop
3. **VS Code** → https://code.visualstudio.com (for editing code)

Verify installations by opening terminal and typing:
```bash
python --version    # should show Python 3.11.x
docker --version    # should show Docker version
```

---

### STEP 2 — Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Click **"Create new secret key"**
3. Copy the key (starts with `sk-...`)
4. Add $5 credit to your account (enough for weeks of testing)

> ⚠️ Keep this key secret — never push it to GitHub

---

### STEP 3 — Set Up the Project

Open terminal in VS Code and run these commands one by one:

```bash
# 1. Go into the project folder
cd rag-platform

# 2. Create a virtual environment (isolated Python environment)
python -m venv venv

# 3. Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 4. Install all dependencies
pip install -r requirements.txt
```

You should see packages installing. This takes 2-3 minutes.

---

### STEP 4 — Add Your API Key

```bash
# Copy the example file
cp .env.example .env
```

Now open `.env` in VS Code and replace:
```
OPENAI_API_KEY=your-openai-api-key-here
```
with your actual key:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
```

---

### STEP 5 — Run the Project

**Option A: Run directly with Python (easier for beginners)**
```bash
uvicorn main:app --reload
```

**Option B: Run with Docker (more professional)**
```bash
docker-compose up --build
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### STEP 6 — Test the API

Open your browser and go to:
```
http://localhost:8000
```

You'll see the API is running. Now go to:
```
http://localhost:8000/docs
```

This is the **Swagger UI** — an automatic interface to test your API visually.

---

### STEP 7 — Upload a Document and Ask Questions

**Using Swagger UI (easiest):**
1. Go to `http://localhost:8000/docs`
2. Click **POST /upload** → Click "Try it out"
3. Choose any PDF from your computer → Click "Execute"
4. You'll see: `"chunks_stored": 45` (or similar number)
5. Now click **POST /ask** → Click "Try it out"
6. Type your question in the body: `{"question": "What is this document about?"}`
7. Click Execute → See the AI answer!

**Using curl (terminal):**
```bash
# Upload a document
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -F "file=@/path/to/your/document.pdf"

# Ask a question
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

---

## ✅ What to Test

Try these questions after uploading a document:
- `"Summarize this document in 3 points"`
- `"What are the main topics covered?"`
- `"What does it say about [specific topic]?"`

---

## 🐛 Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| `openai.AuthenticationError` | Check your `.env` file has the correct API key |
| `Port 8000 already in use` | Run `uvicorn main:app --port 8001` |
| `chromadb error` | Delete the `chroma_db/` folder and restart |

---

## 📌 Disclaimer

> This is a personal learning project built independently. It is not affiliated with or representative of any employer.

---

## 🛠 Tech Stack

- **LangChain** — RAG pipeline and LLM chaining
- **ChromaDB** — Vector database for storing document embeddings  
- **FastAPI** — REST API framework
- **OpenAI GPT-3.5** — Language model for answering questions
- **Docker** — Containerization
- **Python** — Core programming language
