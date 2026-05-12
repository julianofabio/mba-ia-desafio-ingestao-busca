from search import search_prompt

def main():

    print("\nOlá, sou responsável por responder perguntas sobre o catálogo de empresas. Faça sua pergunda ou digite 'sair' para encerrar.\n")

    chain = search_prompt()
    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    while True:
        question = input("Faça sua pergunta: ").strip()
        if question.lower() == "sair":
            print("Encerrando o chat. Até mais!")
            break

        resposta = chain.invoke(question)
        print(resposta + "\n")

if __name__ == "__main__":
    main()
