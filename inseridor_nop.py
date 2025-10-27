from instrucao import Instrucao


class InseridorNOP:
    def __init__(self, num_NOPS, pos_linhas, estrutura):
        self.num_NOPS = num_NOPS
        self.pos_linhas = pos_linhas
        self.estrutura = estrutura
        self.nop = Instrucao("0010011", "I", "addi")

    def adicionar_nops(self):

        estrutura_nops = self.estrutura[:]
        offset = 0

        for idx in range(len(self.pos_linhas)):
            pos = self.pos_linhas[idx] + offset
            n = self.num_NOPS[idx]

            for _ in range(n):
                estrutura_nops.insert(pos + 1, self.nop)
                offset += 1

        return estrutura_nops
