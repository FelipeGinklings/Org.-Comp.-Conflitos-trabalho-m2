# Trabalho de Organização de Computadores - 2025/2
# Grupo: 
# Eduardo José de Souza
# Felipe Ginklings Froes da Cruz

from desmontador import Desmontador
from detector import Detector
from inseridor_nop import InseridorNOP

def hex_to_bin(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(32)

def ler_arquivo(nome_arquivo):
    with open(nome_arquivo) as arquivo:
        linhas = [linha.rstrip() for linha in arquivo]
    return linhas

desmontador = Desmontador()

while True:
    nome_arquivo = input("Escreva o nome do arquivo a ser aberto: ")

    nome_arquivo += ".txt"

    opcao = input("O arquivo está em binário (bin) ou hexadecimal (hex)? ").lower()

    try:
        if opcao == "bin":
            linhas = ler_arquivo(nome_arquivo)
        elif opcao == "hex":
            convertido = []
            linhas = ler_arquivo(nome_arquivo)
            for linha in linhas:
                convertido.append(hex_to_bin(linha))
            linhas = convertido
        else:
            print("Insira uma opção válida! Ou 'bin' ou 'hex'.'")
        
        codigo_completo, estrutura = desmontador.desmontar_instrucoes(linhas)
        
        desmontador.imprimir_instrucoes(codigo_completo)
        desmontador.imprimir_instrucoes(estrutura)

        has_forwarding = False
        detec = Detector(estrutura)
        num_linhas_conflito, pos_linhas = detec.verificar_conflito(has_forwarding)

        inseridorNOP = InseridorNOP(num_linhas_conflito, pos_linhas, estrutura)

        estrutura_nops = inseridorNOP.adicionar_nops()

        desmontador.imprimir_instrucoes(estrutura_nops)
    
    except FileNotFoundError:
        print("Nome do arquivo inválido. Tente novamente.")
    except ValueError:
        print("O sistema de enumeração (bin/hex) foram escolhidos incorretamente. Tente novamente.")