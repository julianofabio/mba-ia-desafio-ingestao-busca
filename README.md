# Desafio MBA Engenharia de Software com IA - Full Cycle

Descreva abaixo como executar a sua solução.

# 1. API_KEU
Inclua a API_KEY da Gemini no parametro GOOGLE_API_KEY do arquivo .en

# 2. Subir o banco de dados:
docker compose up -d

# 3. Executar ingestão do PDF:
python src/ingest.py

# 4. Rodar o chat:
python src/chat.py

# 5. Realizar perguntas sobre o PDF

# 6. Se deseja sair digite 'sair'