import os


class Linhas:
    def __init__(self, pedir_por_input=False):
        if pedir_por_input:
            self._nome_arquivo = input("Escreva o nome do arquivo a ser aberto: ")
            self._nome_arquivo += ".txt"
            self._opcao = input(
                "O arquivo está em binário (bin) ou hexadecimal (hex)? "
            ).lower()
        else:
            self._nome_arquivo = "todasInstrucoes.txt"
            self._opcao = "bin"
        if not os.path.exists(self._nome_arquivo):
            self._linhas = []
            raise ValueError("O arquivo não existe ou o nome está incorreto")
        with open(self._nome_arquivo) as arquivo:
            self._linhas = [linha.rstrip() for linha in arquivo]

    def hex_para_bin(self, hex_str):
        return bin(int(hex_str, 16))[2:].zfill(32)

    def getLinhas(self):
        if self._opcao == "bin":
            return self._linhas
        elif self._opcao == "hex":
            convertido: list[str] = []
            for linha in self._linhas:
                convertido.append(self.hex_para_bin(linha))
            return convertido
        else:
            raise ValueError(
                "Insira uma opção válida! Ou 'bin' ou 'hex'."
            )  # O programa deve terminar aqui e não continuar em caso de opção errada
