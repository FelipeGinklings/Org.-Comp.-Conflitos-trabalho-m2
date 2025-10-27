from dataclasses import dataclass


@dataclass(frozen=True)
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
