def cortar_strings(linhas):
    linhas_formatadas = []

    for linha in linhas:
        op_code = linha[-7:]
        rd = linha[-12:-7]
        func_3 = linha[-15:-12]
        rs1 = linha[-20:-15]
        resto = linha[:-20]
        linhas_formatadas.append((op_code, rd, func_3, rs1, resto))
    return linhas_formatadas

def bin_to_int(bin_str, signed=False):
    if signed and bin_str[0] == '1':
        return int(bin_str, 2) - (1 << len(bin_str))
    else:
        return int(bin_str, 2)

def dividir_e_linkar(linhas_divididas):

    instrucoes = []
    estrutura_instrucoes = []

    for linha in linhas_divididas:

        op_code, rd, func_3, rs1, resto = linha

        rd_int = bin_to_int(rd)
        rs1_int = bin_to_int(rs1)
        func3_int = bin_to_int(func_3)

        match linha[0]:
            case "0010011" if (linha[2] == "001" or linha[2] == "101"):
                shamt = bin_to_int(resto[-5:])
                if linha[2] == "101":
                    if linha[linha[-1][1] == "1"]:
                        instrucoes.append(f"Formato = I srai | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | shamt = {shamt}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, shamt)) # op_code, rd, func_3, rs1, rs2/shamt/immed
                    else:
                        instrucoes.append(f"Formato = I srli | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | shamt = {shamt}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, shamt))
                if linha[2] == "001":
                    instrucoes.append(f"Formato = I slli | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | shamt = {shamt}")
                    estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, shamt))
            case "0010011":
                immed = bin_to_int(resto, signed=True)
                match linha[2]:
                    case "000":
                        instrucoes.append(f"Formato = I addi | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
                    case "010":
                        instrucoes.append(f"Formato = I slti | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
                    case "011":
                        instrucoes.append(f"Formato = I sltiu | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
                    case "100":
                        instrucoes.append(f"Formato = I xori | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
                    case "110":
                        instrucoes.append(f"Formato = I ori | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
                    case "111":
                        instrucoes.append(f"Formato = I andi | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
            case "0000011":
                immed = bin_to_int(resto, signed=True)
                match linha[2]:
                    case "000":
                        instrucoes.append(f"Formato = I lb | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
                    case "001":
                        instrucoes.append(f"Formato = I lh | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
                    case "010":
                        instrucoes.append(f"Formato = I lw | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
                    case "100":
                        instrucoes.append(f"Formato = I lbu | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
                    case "101":
                        instrucoes.append(f"Formato = I lhu | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
            case "1110011":
                instrucoes.append(f"Formato = I ecall | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = 0")
                estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, 0))
            case "1100111":
                immed = bin_to_int(resto, signed=True)
                instrucoes.append(f"Formato = I jalr | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
            case "0110011":
                rs2_bin = resto[-5:]
                func7 = resto[:-5]
                rs2_int = bin_to_int(rs2_bin)
                match linha[2]:
                    case "000":
                        if func7 == "0100000":
                            instrucoes.append(f"Formato = R sub | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int}")
                            estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
                        else:
                            instrucoes.append(f"Formato = R add | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int}")
                            estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
                    case "101":
                        if func7 == "0100000":
                            instrucoes.append(f"Formato = R sra | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int}")
                            estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
                        else:
                            instrucoes.append(f"Formato = R srl | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int}")
                            estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
                    case "001":
                        instrucoes.append(f"Formato = R sll | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
                    case "010":
                        instrucoes.append(f"Formato = R slt | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
                    case "011":
                        instrucoes.append(f"Formato = R sltu | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
                    case "100":
                        instrucoes.append(f"Formato = R xor | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
                    case "110":
                        instrucoes.append(f"Formato = R or | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
                    case "111":
                        instrucoes.append(f"Formato = R and | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
            case "0110111":
                immed_bin = resto + func_3 + rs1
                immed = bin_to_int(immed_bin) << 12
                instrucoes.append(f"Formato = U lui | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
            case "0010111":
                immed_bin = resto + func_3 + rs1
                immed = bin_to_int(immed_bin) << 12
                instrucoes.append(f"Formato = U auipc | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | imed = {immed}")
                estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, immed))
            case "0100011":
                rs2_bin = resto[-5:]
                immed_high = resto[:-5]  # 7 bits: imm[11:5]
                immed_low = rd  # 5 bits: imm[4:0]
                rs2_int = bin_to_int(rs2_bin)
                immed = bin_to_int(immed_high + immed_low, signed=True)
                match linha[2]:
                    case "000":
                        instrucoes.append(f"Formato = S sb | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
                    case "001":
                        instrucoes.append(f"Formato = S sh | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
                    case "010":
                        instrucoes.append(f"Formato = S sw | rd = x{rd_int} | f3 = {func3_int} | rs1 = x{rs1_int} | rs2 = x{rs2_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, rd_int, func3_int, rs1_int, rs2_int))
            case "1100011":
                rs2_bin = resto[-5:]
                upper = resto[:-5]  # 7 bits: imm[12] + imm[10:5]
                immed_12 = upper[0]
                immed_10_5 = upper[1:]  # 6 bits
                immed_4_1 = rd[:4]  # 4 bits
                immed_11 = rd[4]  # 1 bit
                rs2_int = bin_to_int(rs2_bin)
                imm_bits = immed_12 + immed_11 + immed_10_5 + immed_4_1
                immed = bin_to_int(imm_bits + "0", signed=True)
                match linha[2]:
                    case "000":
                        instrucoes.append(f"Formato = B beq | rs1 = x{rs1_int} | rs2 = x{rs2_int} | f3 = {func3_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, 0, func3_int, rs1_int, rs2_int))
                    case "001":
                        instrucoes.append(f"Formato = B bne | rs1 = x{rs1_int} | rs2 = x{rs2_int} | f3 = {func3_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, 0, func3_int, rs1_int, rs2_int))
                    case "100":
                        instrucoes.append(f"Formato = B blt | rs1 = x{rs1_int} | rs2 = x{rs2_int} | f3 = {func3_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, 0, func3_int, rs1_int, rs2_int))
                    case "101":
                        instrucoes.append(f"Formato = B bge | rs1 = x{rs1_int} | rs2 = x{rs2_int} | f3 = {func3_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, 0, func3_int, rs1_int, rs2_int))
                    case "110":
                        instrucoes.append(f"Formato = B bltu | rs1 = x{rs1_int} | rs2 = x{rs2_int} | f3 = {func3_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, 0, func3_int, rs1_int, rs2_int))
                    case "111":
                        instrucoes.append(f"Formato = B bgeu | rs1 = x{rs1_int} | rs2 = x{rs2_int} | f3 = {func3_int} | imed = {immed}")
                        estrutura_instrucoes.append((op_code, 0, func3_int, rs1_int, rs2_int))
            case "1101111":
                upper20 = resto + rs1 + func_3  # bits 31..12
                imm_20 = upper20[0]
                imm_10_1 = upper20[1:11]
                imm_11 = upper20[11]
                imm_19_12 = upper20[12:20]
                imm_bits = imm_20 + imm_19_12 + imm_11 + imm_10_1
                immed = bin_to_int(imm_bits + "0", signed=True)
                instrucoes.append(f"Formato = J jal | rd = x{rd_int} | imed = {immed}")
                estrutura_instrucoes.append((op_code, rd_int, 0, 0, immed))
    
    instrucoes.append(f"Formato = I addi | rd = x{0} | f3 = {0} | rs1 = x{0} | imed = {0}")
    instrucoes.append(f"Formato = I addi | rd = x{0} | f3 = {0} | rs1 = x{0} | imed = {0}")
    estrutura_instrucoes.append(("0010011", 0, 0, 0, 0))
    estrutura_instrucoes.append(("0010011", 0, 0, 0, 0))
    
    return instrucoes, estrutura_instrucoes

class Desmontador:
    def desmontar_instrucoes(self, linhas):
        linhas_divididas = cortar_strings(linhas)
        codigo_completo, estrutura = dividir_e_linkar(linhas_divididas)
        return codigo_completo, estrutura
    
    def imprimir_instrucoes(self, codigo_completo):
        for i, codigo in enumerate(codigo_completo, 1):
                print(f"Linha {i:02}: {codigo}")