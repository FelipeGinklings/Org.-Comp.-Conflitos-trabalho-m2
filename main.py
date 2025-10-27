# Trabalho de Organização de Computadores - 2025/2
# Grupo:
# Eduardo José de Souza
# Felipe Ginklings Froes da Cruz

from desmontador import Desmontador
from detector import Detector
from inseridor_nop import InseridorNOP
from linhas import Linhas

if __name__ == "__main__":
    desmontador = Desmontador()
    linhas = Linhas()
    while True:
        try:
            linhas = linhas.getLinhas()
            codigo_completo, estrutura = desmontador.desmontar_instrucoes(linhas)
            tem_forwarding = False
            deteccao = Detector(estrutura)
            num_linhas_conflito, pos_linhas = deteccao.verificar_conflito(
                tem_forwarding
            )
            inseridor_NOP = InseridorNOP(num_linhas_conflito, pos_linhas, estrutura)
            estrutura_nops = inseridor_NOP.adicionar_nops()

        except FileNotFoundError:
            print("Nome do arquivo inválido. Tente novamente.")
        except ValueError:
            print(
                "O sistema de enumeração (bin/hex) foram escolhidos incorretamente. Tente novamente."
            )
        finally:
            # continuar = input("Continuar (s/n)? ").lower()
            continuar = "n"
            if continuar in ["n", "nao", "não"]:
                break

    print("Programa finalizado!")
