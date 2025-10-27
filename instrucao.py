from dataclasses import dataclass


@dataclass
class Instrucao:
    opcode: str
    formato: str
    nome: str
    rd: int = 0
    rs1: int = 0
    rs2: int = 0
    func3: int = 0
    shamt: int | None = None
    immed: int | None = None
    func7: int | None = None
    id_destino: int | None = None

    def setImmed(self, immed: int):
        self.immed = immed

    def setIdDestino(self, _id: int):
        self.id_destino = _id

    def estaEm(self, instrucoes: list):
        for index, intrucao in enumerate(instrucoes):
            if id(intrucao) == id(self):
                return index, intrucao
        return -1, None

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
        elif self.func7 is not None:
            campos.append(f"func7 = {self.func7}")

        return base + " | " + " | ".join(campos)


if __name__ == "__main__":
    instrucao1 = Instrucao("0010011", "I", "addi")
    instrucao2 = Instrucao("0010011", "J", "jal")
    instrucao3 = Instrucao("0010011", "I", "addi")

    instrucao2.setIdDestino(id(instrucao3))

    instrucoes = [instrucao1, instrucao2, instrucao3]
    index, instrucao = instrucao1.estaEm(instrucoes)
    print(index, instrucao)
    # print(type(id(teste)), id(teste))
