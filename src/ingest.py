import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

#1. Ingestão do PDF
#   O PDF deve ser dividido em chunks de 1000 caracteres com overlap de 150.
#   Cada chunk deve ser convertido em embedding.
#   Os vetores devem ser armazenados no banco de dados PostgreSQL com pgVector.

load_dotenv()

def ingest_pdf():
    PDF_PATH = os.getenv("PDF_PATH")

    print(f"Carregando PDF do caminho: {PDF_PATH}")
    
    # Valida as configs obrigatórias
    for k in ("GOOGLE_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

    PDF_PATH = Path(PDF_PATH)
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF file not found: {PDF_PATH}")

    # Carrega as páginas do PDF
    docs = PyPDFLoader(str(PDF_PATH)).load()

    # Divide o texto em pedaços menores
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150, add_start_index=False).split_documents(docs)
    if not splits:
        raise SystemExit(0)

    # Remove metadados vazios
    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]    

    ids = [f"doc-{i}" for i in range(len(enriched))]

    # Gera embeddings com Gemini
    embeddings = GoogleGenerativeAIEmbeddings(
        model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001")
    )

    # Conecta no PGVector/PostgreSQL
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    # Salva documentos e vetores no banco
    store.add_documents(documents=enriched, ids=ids)

if __name__ == "__main__":
    print("Iniciando processo de ingestão do PDF...")
    ingest_pdf()
