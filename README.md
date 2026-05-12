# Desafio MBA Engenharia de Software com IA - Full Cycle

Instruções de como preparar o ambiente e executar a aplicação

# 1. API_KEY
Inclua a API_KEY da Gemini no parametro GOOGLE_API_KEY do arquivo .en

# 2. Crie e ative um ambiente virtual antes de instalar dependências:
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Subir o banco de dados:
docker compose up -d

# 5. Executar ingestão do PDF:
python src/ingest.py

# 6. Rodar o chat:
python src/chat.py

## Usando a aplicação

# 7. Realizar perguntas sobre o PDF

# 8. Se deseja sair digite 'sair'