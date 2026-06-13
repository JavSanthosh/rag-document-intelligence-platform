# rag_chain.py

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

        # FastEmbed converts document text into vector embeddings for semantic search
        self.embeddings = FastEmbedEmbeddings()

        # Groq-hosted Llama 3.1 model used for answer generation
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        # ChromaDB stores vector embeddings
        self.vectorstore = Chroma(
            collection_name="rag_documents",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db"
        )

        # Recursive chunking with overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def ingest_document(self, file_path: str):
        """
        Loads document → chunks text → stores embeddings in ChromaDB
        """

        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)

        documents = loader.load()

        chunks = self.text_splitter.split_documents(documents)

        if not chunks:
            raise ValueError("No text chunks were created from the document.")

        chunks = [
            chunk
            for chunk in chunks
            if chunk.page_content.strip()
        ]

        self.vectorstore.add_documents(chunks)

        print(f"[RAG] Stored {len(chunks)} chunks in ChromaDB")

        return len(chunks)

    def ask(self, question: str) -> str:
        """
        Retrieves relevant chunks and generates an answer using Groq.
        """

        prompt_template = """
You are an expert document intelligence assistant.

Use ONLY the provided context to answer.

Instructions:
- Provide concise and accurate answers.
- Use headings when appropriate.
- Use bullet points for lists.
- Use numbered steps for processes.
- Do not make up information.
- If the answer is not found in the context, say:
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

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}
            ),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )

        result = qa_chain.invoke({"query": question})

        return result["result"]
