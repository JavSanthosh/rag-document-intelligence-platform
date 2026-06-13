# rag_chain.py
# This file contains ALL the RAG logic
# RAG = Retrieval Augmented Generation
# Simple explanation: Upload doc → store it → user asks question → find relevant parts → LLM answers

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os

class RAGChain:
    def __init__(self):
        # Step 1: Embeddings = converts text into numbers (vectors) so we can do similarity search
        self.embeddings = FastEmbedEmbeddings()
        

        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        # Step 3: ChromaDB = vector database (stores embeddings on disk)
        self.vectorstore = Chroma(
            collection_name="documents",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db"   # saves to this folder
        )

        # Step 4: Text Splitter = breaks big documents into small chunks
        # chunk_size=1000 means each chunk is ~1000 characters
        # chunk_overlap=200 means chunks share 200 chars (so context isn't lost at edges)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def ingest_document(self, file_path: str):
        """
        Takes a document path → loads it → splits into chunks → stores in ChromaDB
        Returns: number of chunks stored
        """
        # Load the document based on file type
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)

        # Load raw text from file
        documents = loader.load()

        # Split into chunks
        chunks = self.text_splitter.split_documents(documents)

        if not chunks:
            raise ValueError("No text chunks were created from the document.")

        # Remove empty chunks
        chunks = [chunk for chunk in chunks if chunk.page_content.strip()]

        # Store all chunks in ChromaDB (each chunk gets embedded automatically)
        self.vectorstore.add_documents(chunks)
        

        print(f"✅ Stored {len(chunks)} chunks in ChromaDB")
        return len(chunks)

    def ask(self, question: str) -> str:
        """
        Takes a question → finds relevant chunks → sends to LLM → returns answer
        """
        # This is our custom prompt template
        # {context} = the relevant chunks retrieved from ChromaDB
        # {question} = user's question
prompt_template = """You are a helpful AI assistant.

Use ONLY the provided context.

Instructions:
- Format the answer clearly.
- Use headings when needed.
- Use bullet points.
- Use numbered lists for steps or strategies.
- Keep answers structured and readable.
- Do not write one large paragraph.

If the answer is not in the context, say:
"I don't have enough information in the document to answer this."

Context:
{context}

Question:
{question}

Answer:
"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # RetrievalQA chain = retrieves chunks + sends to LLM automatically
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",   # "stuff" = put all chunks into one prompt
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}  # retrieve top 3 most relevant chunks
            ),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )

        result = qa_chain.invoke({"query": question})
        return result["result"]
