from model.pacientes import Paciente
from model.profissionais import Profissional

class Agendamento:
    def __init__(self, 
                 cod_relacionamento: int = None,
                 paciente: Paciente = None,
                 profissional: Profissional = None
                 ):
        self.set_cod_relacionamento(cod_relacionamento)
        self.set_paciente(paciente)
        self.set_profissional(profissional)

    def set_cod_relacionamento(self, cod_relacionamento: int):
        self.cod_relacionamento = cod_relacionamento

    def set_paciente(self, paciente: Paciente):
        self.paciente = paciente

    def set_profissional(self, profissional: Profissional):
        self.profissional = profissional

    def get_cod_relacionamento(self) -> int:
        return self.cod_relacionamento

    def get_paciente(self) -> Paciente:
        return self.paciente

    def get_profissional(self) -> Profissional:
        return self.profissional

    def to_string(self) -> str:
        return f"Codigo Relacionamento: {self.get_cod_relacionamento()} | Paciente: {self.get_paciente().get_nome()} | Profissional: {self.get_profissional().get_nome_profissional()}"