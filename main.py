# main.py
# This is the API layer - users interact with the project through these endpoints
# Think of endpoints like buttons: /upload = upload a doc, /ask = ask a question

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
from rag_chain import RAGChain
import os
import shutil
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent RAG Document Intelligence Platform",
    description="Upload documents and ask questions using AI",
    version="1.0.0"
)

# Allow all origins (needed if you build a frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our RAG chain (this loads ChromaDB and connects to OpenAI)
rag = RAGChain()

# ── Request/Response Models ──────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    question: str
    answer: str

# ── Endpoints ────────────────────────────────────────────────────

@app.get("/")
def root():
    """Home endpoint - just to confirm the API is running"""
    return {
        "message": "RAG Document Intelligence Platform is running!",
        "endpoints": {
            "upload": "POST /upload - Upload a PDF or text file",
            "ask": "POST /ask - Ask a question about uploaded documents",
            "health": "GET /health - Check API status"
        }
    }

@app.get("/health")
def health_check():
    """Health check - recruiters/interviewers love seeing this"""
    return {"status": "healthy", "service": "RAG Platform"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF or .txt file.
    The file gets chunked and stored in ChromaDB automatically.
    """
    # Only allow PDF and text files
    allowed_types = ["application/pdf", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and .txt files are supported"
        )

    # Save file temporarily to /tmp folder
    temp_path = f"temp_{uuid.uuid4()}_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Process document through RAG pipeline
        chunk_count = rag.ingest_document(temp_path)
    finally:
        # Always delete temp file after processing
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return {
        "message": f"✅ Document '{file.filename}' uploaded and processed successfully",
        "chunks_stored": chunk_count,
        "status": "ready to answer questions"
    }

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask any question about the uploaded documents.
    The system retrieves relevant context and answers using AI.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    answer = rag.ask(request.question)

    return QuestionResponse(
        question=request.question,
        answer=answer
    )
