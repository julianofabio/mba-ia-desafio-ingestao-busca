import os
from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector


load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def format_docs(results):
    return "\n\n".join(
        f"[score={score:.4f}]\n{doc.page_content}"
        for doc, score in results
    )


def search_prompt(question=None):
    for k in ("GOOGLE_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

    embeddings = GoogleGenerativeAIEmbeddings(
        model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001"),
        transport="rest",
    )

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    def search_context(question):
        return format_docs(store.similarity_search_with_score(question, k=10))

    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GOOGLE_CHAT_MODEL", "gemini-2.0-flash"),
        temperature=0,
        transport="rest",
    )

    return (
        {
            "contexto": RunnableLambda(search_context),
            "pergunta": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
