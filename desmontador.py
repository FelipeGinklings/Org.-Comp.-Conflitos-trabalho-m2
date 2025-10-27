from dataclasses import dataclass


@dataclass(frozen=True)
class Instrucao:
    formato: str
    nome: str
    rd: int = 0
    rs1: int = 0
    rs2: int = 0
    func3: int = 0
    shamt: int | None = None
    immed: int | None = None

    def __str__(self):
        base = f"Formato = {self.formato} {self.nome}"
        campos = []

        if self.rd is not None:
            campos.append(f"rd = x{self.rd}")
        if self.func3 is not None:
            campos.append(f"f3 = {self.func3}")
        if self.rs1 is not None:
            campos.append(f"rs1 = x{self.rs1}")
        if self.rs2 is not None and self.formato in ("R", "S", "B"):
            campos.append(f"rs2 = x{self.rs2}")

        if self.shamt is not None:
            campos.append(f"shamt = {self.shamt}")
        elif self.immed is not None:
            campos.append(f"imed = {self.immed}")

        return base + " | " + " | ".join(campos)


class Desmontador:
    def criarNome(self, opcode, func3):
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
                "00": "sub",
                "01": "add",
                "50": "sra",
                "51": "srl",
                "10": "sll",
                "20": "slt",
                "30": "sltu",
                "40": "xor",
                "60": "or",
                "70": "and",
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
        return traduzir[opcode][func3]

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

        for linha in linhas_divididas:

            op_code, rd, func_3, rs1, resto = linha

            rd_int = self.bin_para_int(rd)
            rs1_int = self.bin_para_int(rs1)
            func3_int = self.bin_para_int(func_3)

            match linha[0]:
                case "0010011" if linha[2] == "001" or linha[2] == "101":
                    shamt = self.bin_para_int(resto[-5:])
                    nome = self.criarNome(
                        linha[0],
                        str(int(linha[2], 2))
                        + str(int(not (linha[linha[-1][1]] == "1"))),
                    )
                    instrucoes.append(
                        f"Formato = I {nome} | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | shamt = {shamt}"
                    )
                    estrutura_instrucoes.append(
                        (op_code, rd_int, func3_int, rs1_int, rs2_int)
                    )
                case "0010011":
                    immed = self.bin_para_int(resto, signed=True)
                    nome = self.criarNome(linha[0] + "-A", linha[2])
                    instrucoes.append(
                        f"Formato = I {nome} | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}"
                    )
                    estrutura_instrucoes.append(
                        (op_code, rd_int, func3_int, rs1_int, immed)
                    )
                case "0000011":
                    immed = self.bin_para_int(resto, signed=True)
                    nome = self.criarNome(linha[0], linha[2])
                    instrucoes.append(
                        f"Formato = I {nome} | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}"
                    )
                    estrutura_instrucoes.append(
                        (op_code, rd_int, func3_int, rs1_int, immed)
                    )
                case "1110011":
                    instrucoes.append(
                        f"Formato = I ecall | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = 0"
                    )
                    estrutura_instrucoes.append(
                        (op_code, rd_int, func3_int, rs1_int, 0)
                    )
                case "1100111":
                    immed = self.bin_para_int(resto, signed=True)
                    instrucoes.append(
                        f"Formato = I jalr | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}"
                    )
                    estrutura_instrucoes.append(
                        (op_code, rd_int, func3_int, rs1_int, immed)
                    )
                case "0110011":
                    rs2_bin = resto[-5:]
                    func7 = resto[:-5]
                    rs2_int = self.bin_para_int(rs2_bin)
                    nome = self.criarNome(
                        linha[0],
                        str(int(linha[2], 2)) + str(int(not (func7 == "0100000"))),
                    )
                    instrucoes.append(
                        f"Formato = R {nome} | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int}"
                    )
                    estrutura_instrucoes.append(
                        (op_code, rd_int, func3_int, rs1_int, rs2_int)
                    )
                case "0110111":
                    immed_bin = resto + func_3 + rs1
                    immed = self.bin_para_int(immed_bin) << 12
                    instrucoes.append(
                        f"Formato = U lui | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}"
                    )
                    estrutura_instrucoes.append(
                        (op_code, rd_int, func3_int, rs1_int, immed)
                    )
                case "0010111":
                    immed_bin = resto + func_3 + rs1
                    immed = self.bin_para_int(immed_bin) << 12
                    instrucoes.append(
                        f"Formato = U auipc | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}"
                    )
                    estrutura_instrucoes.append(
                        (op_code, rd_int, func3_int, rs1_int, immed)
                    )
                case "0100011":
                    rs2_bin = resto[-5:]
                    immed_high = resto[:-5]  # 7 bits: imm[11:5]
                    immed_low = rd  # 5 bits: imm[4:0]
                    rs2_int = self.bin_para_int(rs2_bin)
                    immed = self.bin_para_int(immed_high + immed_low, signed=True)
                    nome = self.criarNome(linha[0], linha[2])
                    instrucoes.append(
                        f"Formato = S {nome} | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int} | imed = {immed}"
                    )
                    estrutura_instrucoes.append(
                        (op_code, rd_int, func3_int, rs1_int, rs2_int)
                    )
                case "1100011":  # branches
                    rs2_bin = resto[-5:]
                    upper = resto[:-5]  # 7 bits: imm[12] + imm[10:5]
                    immed_12 = upper[0]
                    immed_10_5 = upper[1:]  # 6 bits
                    immed_4_1 = rd[:4]  # 4 bits
                    immed_11 = rd[4]  # 1 bit
                    rs2_int = self.bin_para_int(rs2_bin)
                    imm_bits = immed_12 + immed_11 + immed_10_5 + immed_4_1
                    immed = self.bin_para_int(imm_bits + "0", signed=True)
                    nome = self.criarNome(linha[0], linha[2])
                    instrucoes.append(
                        f"Formato = B {nome} | rs1 = x{rs1_int} | rs2 = x{rs2_int} | f3 = {func3_int} | imed = {immed}"
                    )
                    estrutura_instrucoes.append(
                        (op_code, 0, func3_int, rs1_int, rs2_int)
                    )
                case "1101111":
                    upper20 = resto + rs1 + func_3  # bits 31..12
                    imm_20 = upper20[0]
                    imm_10_1 = upper20[1:11]
                    imm_11 = upper20[11]
                    imm_19_12 = upper20[12:20]
                    imm_bits = imm_20 + imm_19_12 + imm_11 + imm_10_1
                    immed = self.bin_para_int(imm_bits + "0", signed=True)
                    instrucoes.append(
                        f"Formato = J jal | rd = x{rd_int} | imed = {immed}"
                    )
                    estrutura_instrucoes.append((op_code, rd_int, 0, 0, immed))

        instrucoes.append(
            f"Formato = I addi | rd = x{0} | f3 = {0} | rs1 = x{0} | imed = {0}"
        )
        instrucoes.append(
            f"Formato = I addi | rd = x{0} | f3 = {0} | rs1 = x{0} | imed = {0}"
        )
        estrutura_instrucoes.append(("0010011", 0, 0, 0, 0))
        estrutura_instrucoes.append(("0010011", 0, 0, 0, 0))

        return instrucoes, estrutura_instrucoes

    def desmontar_instrucoes(self, linhas):
        linhas_divididas = self.cortar_strings(linhas)
        codigo_completo, estrutura = self.dividir_e_linkar(linhas_divididas)
        return codigo_completo, estrutura

    def imprimir_instrucoes(self, codigo_completo):
        for i, codigo in enumerate(codigo_completo, 1):
            print(f"Linha {i:02}: {codigo}")
