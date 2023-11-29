class Paciente:
    def __init__(self,
                 cpf: str = None, 
                 nome: str = None,
                 idade: int = None,
                 tamanho_abdominal: float = None,
                 altura_cm: float = None,
                 peso_kg: float = None,
                ):
        self.set_cpf(cpf)
        self.set_nome(nome)
        self.set_idade(idade)
        self.set_tamanho_abdominal(tamanho_abdominal)
        self.set_altura_cm(altura_cm)
        self.set_peso_kg(peso_kg)
    
    def set_cpf(self, cpf: str):
        self.cpf = cpf

    def set_nome(self, nome: str):
        self.nome = nome

    def set_idade(self, idade: int):
        self.idade = idade 

    def set_tamanho_abdominal(self, tamanho_abdominal: float):
        self.tamanho_abdominal = tamanho_abdominal

    def set_altura_cm(self, altura_cm: float):
        self.altura_cm = altura_cm

    def set_peso_kg(self, peso_kg: float):
        self.peso_kg = peso_kg

    def get_cpf(self) -> str:
        return self.cpf

    def get_nome(self) -> str:
        return self.nome

    def get_idade(self) -> int:
        return self.idade

    def get_tamanho_abdominal(self) -> float:
        return self.tamanho_abdominal

    def get_altura_cm(self) -> float:
        return self.altura_cm

    def get_peso_kg(self) -> float:
        return self.peso_kg

    def get_peso_kg(self) -> float:
        return self.peso_kg

    def to_string(self) -> str:
        return f"CPF: {self.get_cpf()} | Nome: {self.get_nome()} | Idade: {self.get_idade()} | Tamanho Abdominal: {self.get_tamanho_abdominal()} | Altura: {self.get_altura_cm()} | Peso: {self.get_peso_kg()} | Peso Objetivo: {self.get_peso_kg()}"