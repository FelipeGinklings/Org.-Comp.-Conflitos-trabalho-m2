from instrucao import Instrucao


class InseridorNOP:
    def __init__(self, num_NOPS, pos_linhas, estrutura: list[Instrucao]):
        self.num_NOPS = num_NOPS
        self.pos_linhas = pos_linhas
        self.estrutura = estrutura
        self.nop = Instrucao("0010011", "I", "addi")

    def adicionar_nops(self):

        estrutura_nops = self.estrutura[:]
        offset = 0

        for index in range(len(self.pos_linhas)):
            pos = self.pos_linhas[index] + offset
            n = self.num_NOPS[index]

            for _ in range(n):
                estrutura_nops.insert(pos + 1, self.nop)
                offset += 1

        branch_jal_index = list(
            filter(lambda instrucao: instrucao.formato in "BJ", estrutura_nops)
        )

        for branch_posicao, branch in enumerate(branch_jal_index):
            instrucao_J_B: Instrucao = estrutura_nops[branch]
            intrucao_destino = instrucao_J_B.destino
            posicao, _ = intrucao_destino.esta_em(estrutura_nops)
            endereco = (posicao - branch_posicao) * 4
            instrucao_J_B.set_immed(endereco)

        return estrutura_nops
