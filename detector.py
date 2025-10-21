class Detector:
    
    def __init__(self, estrutura):
        self.estrutura = estrutura[:]

    def verificar_conflito(self, has_forwarding):
        num_linhas_conflito = []
        pos_linhas = []
        modif_forwarding = 0

        if has_forwarding:
            modif_forwarding = 1

        # num_linhas_conflito e pos_linhas andam juntos.
        # Um salva a linha que teve conflito para poder saber em que posição precisa ser arrumado e a partir de onde
        # E o outro salva quantas linhas precisa ser arrumado, quão longe vai esse conflito, se está logo abaixo ou 2 abaixo

        # Verificando conflito entre "rd"[1] e rs1[3]/rs2[4](Verificar se o OP code tem o rs2)
        for i in range(len(self.estrutura)-2):
            op_atual = self.estrutura[i][0]
            rd = self.estrutura[i][1]
            escritores = {"0010011", "0110011"}
            load_word = {"0000011"}
            desvios = {"1100011", "1101111", "1100111"}

            prox1_rs1, prox1_rs2 = self.estrutura[i+1][3], self.estrutura[i+1][4]
            prox2_rs1, prox2_rs2 = self.estrutura[i+2][3], self.estrutura[i+2][4]

            if op_atual in escritores and rd != 0:
                # Caso tenha forwarding, zera, caso contrário, coloca o número padrão
                if rd == prox1_rs1 or rd == prox1_rs2:
                    num_linhas_conflito.append(2*(1-modif_forwarding))
                    pos_linhas.append(i)
                    continue
                elif rd == prox2_rs1 or rd == prox2_rs2:
                    num_linhas_conflito.append(1*(1-modif_forwarding))
                    pos_linhas.append(i)
                    continue

            if op_atual in load_word and rd != 0:
                if rd == prox1_rs1 or rd == prox1_rs2:
                    num_linhas_conflito.append(2-modif_forwarding)
                    # Independente de haver forwarding ou não, precisa de 1 NOP por ser a última instrução. Sem forwarding precisa de 2
                    pos_linhas.append(i)
                    continue
                elif rd == prox2_rs1 or rd == prox2_rs2:
                    num_linhas_conflito.append(1-modif_forwarding)
                    pos_linhas.append(i)
                    continue

            if op_atual in desvios:
                num_linhas_conflito.append(3)
                pos_linhas.append(i)
                continue

        print("Quantos pular: ", num_linhas_conflito)
        print("Quais linhas: ", pos_linhas)

        return num_linhas_conflito, pos_linhas