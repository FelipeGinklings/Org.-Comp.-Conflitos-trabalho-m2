from instrucao import Instrucao
from collections import defaultdict


class Desmontador:
    def criar_nome(self, opcode, func3):
        traduzir = {
            "1100011": {
                "000": "beq",
                "001": "bne",
                "100": "blt",
                "101": "bge",
                "110": "bltu",
                "111": "bgeu",
            },
            "0100011": {
                "000": "sb",
                "001": "sh",
                "010": "sw",
            },
            "0110011": {
                "0001": "sub",
                "1011": "sra",
                "0000": "add",
                "1010": "srl",
                "0010": "sll",
                "0100": "slt",
                "0110": "sltu",
                "1000": "xor",
                "1100": "or",
                "1110": "and",
            },
            "0000011": {
                "000": "lb",
                "001": "lh",
                "010": "lw",
                "100": "lbu",
                "101": "lhu",
            },
            "0010011-A": {
                "000": "addi",
                "010": "slti",
                "011": "sltiu",
                "100": "xori",
                "110": "ori",
                "111": "andi",
            },
            "0010011": {
                "51": "srai",
                "50": "srli",
                "10": "slli",
            },
        }
        traduzir_default = defaultdict(lambda: f"error - opcode: {opcode}", traduzir)
        return traduzir_default[opcode][func3]

    def cortar_strings(self, linhas):
        linhas_formatadas = []

        for linha in linhas:
            op_code = linha[-7:]
            rd = linha[-12:-7]
            func_3 = linha[-15:-12]
            rs1 = linha[-20:-15]
            resto = linha[:-20]
            linhas_formatadas.append((op_code, rd, func_3, rs1, resto))
        return linhas_formatadas

    def bin_para_int(self, bin_str, signed=False):
        if signed and bin_str[0] == "1":
            return int(bin_str, 2) - (1 << len(bin_str))
        else:
            return int(bin_str, 2)

    def dividir_e_linkar(self, linhas_divididas):
        instrucoes = []
        estrutura_instrucoes = []
        branch_jal_index = []
        for index, linha in enumerate(linhas_divididas):
            op_code, rd, func_3, rs1, resto = linha

            rd_int = self.bin_para_int(rd)
            rs1_int = self.bin_para_int(rs1)
            func3_int = self.bin_para_int(func_3)

            match linha[0]:
                # --- Tipo I com shamt ---
                case "0010011" if linha[2] in ("001", "101"):
                    shamt = self.bin_para_int(resto[-5:])
                    nome = self.criar_nome(
                        linha[0],
                        str(int(linha[2], 2))
                        + str(int(not (linha[linha[-1][1]] == "1"))),
                    )
                    intrucao = Instrucao(
                        linha[0],
                        "I",
                        nome,
                        rd_int,
                        rs1_int,
                        func3=func3_int,
                        shamt=shamt,
                    )

                # --- Tipo I padrão ---
                case "0010011":
                    immed = self.bin_para_int(resto, signed=True)
                    nome = self.criar_nome(linha[0] + "-A", linha[2])
                    intrucao = Instrucao(
                        linha[0],
                        "I",
                        nome,
                        rd_int,
                        rs1_int,
                        func3=func3_int,
                        immed=immed,
                    )

                # --- Load ---
                case "0000011":
                    immed = self.bin_para_int(resto, signed=True)
                    nome = self.criar_nome(linha[0], linha[2])
                    intrucao = Instrucao(
                        linha[0],
                        "I",
                        nome,
                        rd_int,
                        rs1_int,
                        func3=func3_int,
                        immed=immed,
                    )

                # --- ecall ---
                case "1110011":
                    intrucao = Instrucao(
                        linha[0],
                        "I",
                        "ecall",
                        rd_int,
                        rs1_int,
                        func3=func3_int,
                        immed=0,
                    )

                # --- jalr ---
                case "1100111":
                    immed = self.bin_para_int(resto, signed=True)
                    intrucao = Instrucao(
                        linha[0],
                        "I",
                        "jalr",
                        rd_int,
                        rs1_int,
                        func3=func3_int,
                        immed=immed,
                    )

                # --- Tipo R ---
                case "0110011":
                    rs2_bin = resto[-5:]
                    func7 = resto[:-5]
                    rs2_int = self.bin_para_int(rs2_bin)
                    func3_com_func7 = linha[2] + str(int(func7 == "0100000"))
                    nome = self.criar_nome(linha[0], func3_com_func7)
                    intrucao = Instrucao(
                        linha[0],
                        "R",
                        nome,
                        rd_int,
                        rs1_int,
                        rs2_int,
                        func3=func3_int,
                        func7=int(func7, 2),
                    )

                # --- lui ---
                case "0110111":
                    immed_bin = resto + func_3 + rs1
                    immed = self.bin_para_int(immed_bin)
                    intrucao = Instrucao(
                        linha[0],
                        "U",
                        "lui",
                        rd_int,
                        rs1_int,
                        func3=func3_int,
                        immed=immed,
                    )

                # --- auipc ---
                case "0010111":
                    immed_bin = resto + func_3 + rs1
                    immed = self.bin_para_int(immed_bin)
                    intrucao = Instrucao(
                        linha[0],
                        "U",
                        "auipc",
                        rd_int,
                        rs1_int,
                        func3=func3_int,
                        immed=immed,
                    )

                # --- Tipo S ---
                case "0100011":
                    rs2_bin = resto[-5:]
                    immed_high = resto[:-5]  # 7 bits
                    immed_low = rd  # 5 bits
                    rs2_int = self.bin_para_int(rs2_bin)
                    immed = self.bin_para_int(immed_high + immed_low, signed=True)
                    nome = self.criar_nome(linha[0], linha[2])
                    intrucao = Instrucao(
                        linha[0],
                        "S",
                        nome,
                        rd_int,
                        rs1_int,
                        rs2_int,
                        func3=func3_int,
                        immed=immed,
                    )

                # --- Tipo B ---
                case "1100011":
                    branch_jal_index.append(index)
                    rs2_bin = resto[-5:]
                    upper = resto[:-5]
                    immed_12 = upper[0]
                    immed_10_5 = upper[1:]
                    immed_4_1 = rd[:4]
                    immed_11 = rd[4]
                    rs2_int = self.bin_para_int(rs2_bin)
                    imm_bits = immed_12 + immed_11 + immed_10_5 + immed_4_1
                    immed = self.bin_para_int(imm_bits + "0", signed=True)
                    nome = self.criar_nome(linha[0], linha[2])
                    intrucao = Instrucao(
                        linha[0],
                        "B",
                        nome,
                        rs1=rs1_int,
                        rs2=rs2_int,
                        func3=func3_int,
                        immed=immed,
                    )

                # --- Tipo J ---
                case "1101111":
                    upper20 = resto + rs1 + func_3
                    branch_jal_index.append(index)
                    imm_20 = upper20[0]
                    imm_10_1 = upper20[1:11]
                    imm_11 = upper20[11]
                    imm_19_12 = upper20[12:20]
                    imm_bits = imm_20 + imm_19_12 + imm_11 + imm_10_1
                    immed = self.bin_para_int(imm_bits + "0", signed=True)
                    intrucao = Instrucao(linha[0], "J", "jal", rd_int, immed=immed)

                case _:
                    continue  # ignora formatos desconhecidos
            instrucoes.append(intrucao)
            estrutura_instrucoes.append(
                (op_code, rd_int, func3_int, rs1_int, getattr(intrucao, "rs2", 0))
            )

        for branch in branch_jal_index:
            instrucao_J_B: Instrucao = instrucoes[branch]
            intrucao_destino = instrucoes[int(branch + instrucao_J_B.immed / 4)]
            instrucao_J_B.set_id_destino(id(intrucao_destino))

        # Adiciona duas instruções "addi 0,0,0" no final
        addi_zero = Instrucao(linha[0], "I", "addi", 0, 0, func3=0, immed=0)
        instrucoes.extend([addi_zero, addi_zero])
        estrutura_instrucoes.extend([("0010011", 0, 0, 0, 0), ("0010011", 0, 0, 0, 0)])
        return instrucoes, estrutura_instrucoes

    def desmontar_instrucoes(self, linhas):
        linhas_divididas = self.cortar_strings(linhas)
        codigo_completo, estrutura = self.dividir_e_linkar(linhas_divididas)
        return codigo_completo, estrutura

    def imprimir_instrucoes(self, codigo_completo):
        for i, codigo in enumerate(codigo_completo, 1):
            print(f"Linha {i:02}: {codigo}")
