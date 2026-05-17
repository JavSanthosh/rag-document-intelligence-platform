# 🤖 RAG Document Intelligence Platform

Ask questions about PDFs and documents using AI using Retrieval Augmented Generation (RAG).

Built with:
- FastAPI
- LangChain
- ChromaDB
- Groq Llama 3.1 8B Instant
- FastEmbed
- Docker
- Render

---

## 🚀 Features

✅ Upload PDF or TXT documents  
✅ Automatic document chunking  
✅ Lightweight vector embeddings using FastEmbed  
✅ Semantic search using ChromaDB  
✅ AI-powered question answering using Groq Llama 3.1 8B Instant  
✅ REST API with FastAPI  
✅ Dockerized setup  
✅ Cloud deployment using Render  

---

## 🧠 How It Works

```text
Upload Document
       ↓
Text Extraction
       ↓
Chunking
       ↓
Embeddings Generation
       ↓
Store in ChromaDB
       ↓
Ask Question
       ↓
Retrieve Relevant Chunks
       ↓
LLM Generates Answer

This architecture is called:

### Retrieval Augmented Generation (RAG)

---

## 📁 Project Structure

```text
rag-document-intelligence-platform/
│
├── main.py
├── rag_chain.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── README.md
├── screenshots/
│   ├── swagger.png
│   ├── upload.png
│   └── ask.png
└── chroma_db/
```

---

## ⚙️ Tech Stack

| Component        | Technology                |
| ---------------- | ------------------------- |
| Backend API      | FastAPI                   |
| LLM              | Groq Llama 3.1 8B Instant |
| Embeddings       | FastEmbed                 |
| Vector Database  | ChromaDB                  |
| Framework        | LangChain                 |
| Containerization | Docker                    |
| Deployment       | Render                    |

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 🛠 Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/JavSanthosh/rag-document-intelligence-platform.git

cd rag-document-intelligence-platform
```

---

### 2. Create Virtual Environment

#### Windows

```bash
py -3.11 -m venv venv

venv\Scripts\activate
```

#### Mac/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run Application

```bash
uvicorn main:app --reload
```

Application runs at:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

## 🐳 Docker Setup

### Build and Run

```bash
docker-compose up --build
```

---

## 📌 API Endpoints

| Endpoint  | Method | Description     |
| --------- | ------ | --------------- |
| `/`       | GET    | API status      |
| `/health` | GET    | Health check    |
| `/upload` | POST   | Upload document |
| `/ask`    | POST   | Ask questions   |

---

## 🌐 Live Deployment

### API URL

```text
https://rag-platform-gbv3.onrender.com/
```

### Swagger Documentation

```text
https://rag-platform-gbv3.onrender.com/docs
```

---

## 🧪 Example Question

```json
{
  "question": "Summarize the document"
}
```

---

## 📦 Example Response

```json
{
  "question": "Summarize the document",
  "answer": "The document discusses..."
}
```

---

## 📸 Screenshots

### Swagger API Documentation

![Swagger Docs](screenshots/swagger.png)

---

### Document Upload

![Upload](screenshots/upload.png)

---

### AI Question Answering

![Ask](screenshots/ask.png)

---

## 🐛 Common Errors

| Error                | Fix                               |
| -------------------- | --------------------------------- |
| Missing dependencies | `pip install -r requirements.txt` |
| Invalid API key      | Check `.env`                      |
| Port already in use  | Change port                       |
| ChromaDB issues      | Delete `chroma_db/`               |

---

## 🔒 Security

Never upload:

* `.env`
* API keys
* secrets

Use `.gitignore` properly.

---

## 📌 Disclaimer

This is a personal educational and portfolio project built for learning purposes.

---

## 👨‍💻 Author

Santhosh
