from dataclasses import dataclass
from desmontador import Desmontador
from detector import Detector
from inseridor_nop import InseridorNOP


@dataclass
class Questoes:
    linhas: list[str]
    _tem_forwarding: bool = False

    def __post_init__(self):
        self.desmontador = Desmontador(self.linhas)
        self.detector = Detector(self.desmontador)
        self.inseridor = None

    def questao_1(self):
        """Detectar conflito de dados"""
        self.detector._verificar_conflito(self._tem_forwarding, somente_dados=True)
        self.inseridor = InseridorNOP.from_detector(self.detector)
        print("\n=== QUESTÃO 1: Detectar conflito de dados ===")
        print("COM FORWARDING" if self._tem_forwarding else "SEM FORWARDING")
        print(f"Sobrecusto: {self.detector._sobrecusto} instruções")
        print(f"Conflitos detectados: {self.detector.num_linhas_conflito}")
        print(f"Posições dos conflitos: {self.detector.pos_linhas}")

    def questao_2(self):
        """Detectar conflito de controle"""
        self.detector._verificar_conflito(self._tem_forwarding, somente_controle=True)
        self.inseridor = InseridorNOP.from_detector(self.detector)
        print("\n=== QUESTÃO 2: Detectar conflito de controle ===")
        print("COM FORWARDING" if self._tem_forwarding else "SEM FORWARDING")
        print(f"Sobrecusto: {self.detector._sobrecusto} instruções")
        print(f"Conflitos detectados: {self.detector.num_linhas_conflito}")
        print(f"Posições dos conflitos: {self.detector.pos_linhas}")

    def questao_3(self):
        """Corrigir conflito de dados com NOPs"""
        self.detector._verificar_conflito(self._tem_forwarding, somente_dados=True)
        self.inseridor = InseridorNOP.from_detector(self.detector)
        print("\n=== QUESTÃO 3: Corrigir conflito de dados com NOPs ===")
        print("COM FORWARDING" if self._tem_forwarding else "SEM FORWARDING")
        print(f"Sobrecusto: {self.detector._sobrecusto} instruções NOP inseridas")
        print("\nCódigo corrigido:")
        self.desmontador.imprimir_instrucoes(self.inseridor.gerar_instrucoes_com_nop())

    def questao_4(self):
        """Corrigir conflito de controle com NOPs"""
        self.detector._verificar_conflito(self._tem_forwarding, somente_controle=True)
        self.inseridor = InseridorNOP.from_detector(self.detector)
        print("\n=== QUESTÃO 4: Corrigir conflito de controle com NOPs ===")
        print("COM FORWARDING" if self._tem_forwarding else "SEM FORWARDING")
        print(f"Sobrecusto: {self.detector._sobrecusto} instruções NOP inseridas")
        print("\nCódigo corrigido:")
        self.desmontador.imprimir_instrucoes(self.inseridor.gerar_instrucoes_com_nop())

    def questao_5(self):
        """Solução integrada: dados + controle"""
        self.detector._verificar_conflito(self._tem_forwarding)
        self.inseridor = InseridorNOP.from_detector(self.detector)
        print("\n=== QUESTÃO 5: Solução integrada (dados + controle) ===")
        print("COM FORWARDING" if self._tem_forwarding else "SEM FORWARDING")
        print(f"Sobrecusto total: {self.detector._sobrecusto} instruções NOP inseridas")
        print("\nCódigo corrigido:")
        self.desmontador.imprimir_instrucoes(self.inseridor.gerar_instrucoes_com_nop())

    def executar_todas_questoes(self):
        """Executa todas as questões com e sem forwarding"""
        for forwarding in [False, True]:
            self._tem_forwarding = forwarding
            self.questao_1()
            self.questao_2()
            self.questao_3()
            self.questao_4()
            self.questao_5()
            print("\n" + "=" * 60 + "\n")
