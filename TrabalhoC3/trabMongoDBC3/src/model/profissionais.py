class Profissional:
    def __init__(self, licenca: str = None, 
                 nome_profissional: str = None, 
                 especialidade: str = None, 
                 contato_envio: str = None):
        self.licenca = licenca
        self.set_nome_profissional(nome_profissional)
        self.set_especialidade(especialidade)
        self.set_contato_envio(contato_envio)

    def set_nome_profissional(self, nome_profissional: str):
        self.nome_profissional = nome_profissional

    def set_especialidade(self, especialidade: str):
        self.especialidade = especialidade

    def set_contato_envio(self, contato_envio: str):
        self.contato_envio = contato_envio

    def get_licenca(self) -> str:
        return self.licenca

    def get_nome_profissional(self) -> str:
        return self.nome_profissional

    def get_especialidade(self) -> str:
        return self.especialidade

    def get_contato_envio(self) -> str:
        return self.contato_envio

    def to_string(self) -> str:
        return f"Licença: {self.get_licenca()} | Nome Profissional: {self.get_nome_profissional()} | Especialidade: {self.get_especialidade()} | Contato para Envio: {self.get_contato_envio()}"