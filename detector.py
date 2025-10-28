from dataclasses import dataclass, field
from desmontador import Desmontador


@dataclass
class Detector:
    desmontador: Desmontador
    _num_linhas_conflito: list[int] = field(default_factory=list)
    _pos_linhas: list[int] = field(default_factory=list)

    def _verificar_conflito(
        self, tem_forwarding=False, somente_dados=False, somente_controle=False
    ):
        estrutura = self.desmontador.estrutura
        num_linhas_conflito = []
        pos_linhas = []
        modificador_do_forwarding = 0

        if tem_forwarding:
            modificador_do_forwarding = 1

        # num_linhas_conflito e pos_linhas andam juntos.
        # Um salva a linha que teve conflito para poder saber em que posição precisa ser arrumado e a partir de onde
        # E o outro salva quantas linhas precisa ser arrumado, quão longe vai esse conflito, se está logo abaixo ou 2 abaixo

        # Verificando conflito entre "rd"[1] e rs1[3]/rs2[4](Verificar se o OP code tem o rs2)

        for i in range(len(estrutura) - 2):
            op_atual = estrutura[i][0]
            rd = estrutura[i][1]
            escritores = {"0010011", "0110011"}
            load_word = {"0000011"}
            desvios = {"1100011", "1101111", "1100111"}

            prox1_rs1, prox1_rs2 = estrutura[i + 1][3], estrutura[i + 1][4]
            prox2_rs1, prox2_rs2 = estrutura[i + 2][3], estrutura[i + 2][4]

            if not somente_controle:
                if op_atual in escritores and rd != 0:
                    if rd == prox1_rs1 or rd == prox1_rs2:
                        num_linhas_conflito.append(2 * (1 - modificador_do_forwarding))
                        pos_linhas.append(i)
                        continue
                    elif rd == prox2_rs1 or rd == prox2_rs2:
                        num_linhas_conflito.append(1 * (1 - modificador_do_forwarding))
                        pos_linhas.append(i)
                        continue
                elif op_atual in load_word and rd != 0:
                    if rd == prox1_rs1 or rd == prox1_rs2:
                        num_linhas_conflito.append(2 - modificador_do_forwarding)
                        pos_linhas.append(i)
                        continue
                    elif rd == prox2_rs1 or rd == prox2_rs2:
                        num_linhas_conflito.append(1 - modificador_do_forwarding)
                        pos_linhas.append(i)
                        continue
            if not somente_dados:
                if op_atual in desvios:
                    num_linhas_conflito.append(3)
                    pos_linhas.append(i)
                    continue

        self._num_linhas_conflito = num_linhas_conflito
        self._pos_linhas = pos_linhas

    @property
    def _sobrecusto(self):
        return sum(self._num_linhas_conflito)

    @property
    def num_linhas_conflito(self):
        return self._num_linhas_conflito

    @property
    def pos_linhas(self):
        return self._pos_linhas
