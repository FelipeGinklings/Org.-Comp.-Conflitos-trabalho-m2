# Trabalho de Organização de Computadores - 2025/2
# Grupo:
# Eduardo José de Souza
# Felipe Ginklings Froes da Cruz
from linhas import Linhas
from questoes import Questoes

if __name__ == "__main__":
    try:
        # Processar questões
        questoes = [1, 2, 3, 4, 5]
        linhas_obj = Linhas(pedir_por_input=True)
        linhas = linhas_obj.getLinhas()
        for questao in questoes:
            resposta = Questoes(linhas)
            print(f"Questão Número - {questao}")
            print("Sem Forwarding\n")
            match questao:
                case 1:
                    resposta.questao_1()
                    print("Com Forwarding")
                    resposta.questao_1(True)
                case 2:
                    resposta.questao_2()
                    print("Com Forwarding")
                    resposta.questao_2(True)
                case 3:
                    resposta.questao_3()
                    print("Com Forwarding")
                    resposta.questao_3(True)
                case 4:
                    resposta.questao_4()
                    print("Com Forwarding")
                    resposta.questao_4(True)
                case 5:
                    resposta.questao_5()
                    print("Com Forwarding")
                    resposta.questao_5(True)
                case _:
                    print("Foram todas as questões!")
        # questoes.executar_todas_questoes()

    except FileNotFoundError:
        print("Nome do arquivo inválido. Tente novamente.")
    except ValueError as e:
        print(f"Erro: {e}")

    print("Programa finalizado!")
