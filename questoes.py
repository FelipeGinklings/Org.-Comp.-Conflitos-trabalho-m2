import os
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
        # Criar pasta respostas se não existir
        os.makedirs("respostas", exist_ok=True)

    def _salvar_questao(self, numero_questao, conteudo):
        """Salva o conteúdo em um arquivo para a questão especificada"""
        nome_arquivo = f"respostas/questao_{numero_questao}{'_com_forwarding' if self._tem_forwarding else '_sem_forwarding'}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
        print(f"Resultado salvo em: {nome_arquivo}")
        print(f"Sobrecusto: {self.detector._sobrecusto} instruções\n\n")

    def questao_1(self, tem_forwarding=False):
        """Detectar conflito de dados"""
        self._tem_forwarding = tem_forwarding
        self.detector._verificar_conflito(self._tem_forwarding, somente_dados=True)
        self.inseridor = InseridorNOP.from_detector(self.detector)

        conteudo = "=== QUESTÃO 1: Detectar conflito de dados ===\n"
        conteudo += "COM FORWARDING\n" if self._tem_forwarding else "SEM FORWARDING\n"
        conteudo += f"Sobrecusto: {self.detector._sobrecusto} instruções\n"
        conteudo += f"Conflitos detectados: {self.detector.num_linhas_conflito}\n"
        conteudo += f"Posições dos conflitos: {self.detector.pos_linhas}\n"

        self._salvar_questao(1, conteudo)

    def questao_2(self, tem_forwarding=False):
        """Detectar conflito de controle"""
        self._tem_forwarding = tem_forwarding
        self.detector._verificar_conflito(self._tem_forwarding, somente_controle=True)
        self.inseridor = InseridorNOP.from_detector(self.detector)

        conteudo = "=== QUESTÃO 2: Detectar conflito de controle ===\n"
        conteudo += "COM FORWARDING\n" if self._tem_forwarding else "SEM FORWARDING\n"
        conteudo += f"Sobrecusto: {self.detector._sobrecusto} instruções\n"
        conteudo += f"Conflitos detectados: {self.detector.num_linhas_conflito}\n"
        conteudo += f"Posições dos conflitos: {self.detector.pos_linhas}\n"

        self._salvar_questao(2, conteudo)

    def questao_3(self, tem_forwarding=False):
        """Corrigir conflito de dados com NOPs"""
        self._tem_forwarding = tem_forwarding
        self.detector._verificar_conflito(self._tem_forwarding, somente_dados=True)
        self.inseridor = InseridorNOP.from_detector(self.detector)

        conteudo = "=== QUESTÃO 3: Corrigir conflito de dados com NOPs ===\n"
        conteudo += "COM FORWARDING\n" if self._tem_forwarding else "SEM FORWARDING\n"
        conteudo += (
            f"Sobrecusto: {self.detector._sobrecusto} instruções NOP inseridas\n"
        )
        conteudo += "\nCódigo corrigido:\n"

        # Capturar a saída do imprimir_instrucoes
        instrucoes_corrigidas = self.inseridor.gerar_instrucoes_com_nop()
        # Se o método retornar uma string, use diretamente
        if isinstance(instrucoes_corrigidas, str):
            conteudo += instrucoes_corrigidas
        else:
            # Se for uma lista ou outro tipo, converta para string
            conteudo += "\n".join(str(inst) for inst in instrucoes_corrigidas)

        self._salvar_questao(3, conteudo)

    def questao_4(self, tem_forwarding=False):
        """Corrigir conflito de controle com NOPs"""
        self._tem_forwarding = tem_forwarding
        self.detector._verificar_conflito(self._tem_forwarding, somente_controle=True)
        self.inseridor = InseridorNOP.from_detector(self.detector)

        conteudo = "=== QUESTÃO 4: Corrigir conflito de controle com NOPs ===\n"
        conteudo += "COM FORWARDING\n" if self._tem_forwarding else "SEM FORWARDING\n"
        conteudo += (
            f"Sobrecusto: {self.detector._sobrecusto} instruções NOP inseridas\n"
        )
        conteudo += "\nCódigo corrigido:\n"

        instrucoes_corrigidas = self.inseridor.gerar_instrucoes_com_nop()
        if isinstance(instrucoes_corrigidas, str):
            conteudo += instrucoes_corrigidas
        else:
            conteudo += "\n".join(str(inst) for inst in instrucoes_corrigidas)

        self._salvar_questao(4, conteudo)

    def questao_5(self, tem_forwarding=False):
        """Solução integrada: dados + controle"""
        self._tem_forwarding = tem_forwarding
        self.detector._verificar_conflito(self._tem_forwarding)
        self.inseridor = InseridorNOP.from_detector(self.detector)

        conteudo = "=== QUESTÃO 5: Solução integrada (dados + controle) ===\n"
        conteudo += "COM FORWARDING\n" if self._tem_forwarding else "SEM FORWARDING\n"
        conteudo += (
            f"Sobrecusto total: {self.detector._sobrecusto} instruções NOP inseridas\n"
        )
        conteudo += "\nCódigo corrigido:\n"

        instrucoes_corrigidas = self.inseridor.gerar_instrucoes_com_nop()
        if isinstance(instrucoes_corrigidas, str):
            conteudo += instrucoes_corrigidas
        else:
            conteudo += "\n".join(str(inst) for inst in instrucoes_corrigidas)

        self._salvar_questao(5, conteudo)

    def executar_todas_questoes(self):
        """Executa todas as questões com e sem forwarding"""
        for forwarding in [False, True]:
            self._tem_forwarding = forwarding
            self.questao_1()
            self.questao_2()
            self.questao_3()
            self.questao_4()
            self.questao_5()
            print(f"Questões com forwarding={forwarding} concluídas!\n")
