from dataclasses import dataclass
from detector import Detector
from instrucao import Instrucao
import copy


@dataclass
class InseridorNOP:
    _instrucoes_originais: list[Instrucao]
    _pos_linhas: list[int]
    _num_linhas_conflito: list[int]

    @classmethod
    def from_detector(cls, detector: Detector):
        # Usar deepcopy para evitar mutação compartilhada
        return cls(
            _instrucoes_originais=copy.deepcopy(detector.desmontador.instrucoes),
            _pos_linhas=detector.pos_linhas[:],
            _num_linhas_conflito=detector.num_linhas_conflito[:],
        )

    def gerar_instrucoes_com_nop(self) -> list[Instrucao]:
        """Método explícito ao invés de property com efeito colateral"""
        novas_instrucoes = copy.deepcopy(self._instrucoes_originais)
        offset = 0
        nop: Instrucao = Instrucao("0010011", "I", "addi")

        for index in range(len(self._pos_linhas)):
            pos = self._pos_linhas[index] + offset
            n = self._num_linhas_conflito[index]

            for _ in range(n):
                novas_instrucoes.insert(pos + 1, nop)
                offset += 1

        branch_jal_index = list(
            filter(lambda instrucao: instrucao.formato in "BJ", novas_instrucoes)
        )
        for instrucao_J_B in branch_jal_index:
            branch_posicao, _ = instrucao_J_B.esta_em(novas_instrucoes)
            intrucao_destino = instrucao_J_B.destino
            posicao, _ = intrucao_destino.esta_em(novas_instrucoes)
            endereco = (posicao - branch_posicao) * 4
            instrucao_J_B.set_immediato(endereco)

        return novas_instrucoes
