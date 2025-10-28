# Trabalho de Organização de Computadores - 2025/2
# Grupo:
# Eduardo José de Souza
# Felipe Ginklings Froes da Cruz
from linhas import Linhas
from questoes import Questoes

if __name__ == "__main__":
    try:
        # Obter linhas do arquivo
        linhas_obj = Linhas(nome_arquivo="todasIntrucoes.txt")
        linhas_obj.pedirPorInput()
        linhas = linhas_obj.getLinhas()

        # Processar questões
        questoes = Questoes(linhas)
        questoes.executar_todas_questoes()

    except FileNotFoundError:
        print("Nome do arquivo inválido. Tente novamente.")
    except ValueError as e:
        print(f"Erro: {e}")

    print("Programa finalizado!")

