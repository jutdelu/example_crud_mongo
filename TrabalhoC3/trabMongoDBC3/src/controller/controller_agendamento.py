import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.agendamentos import Agendamento
from model.pacientes import Paciente
from model.profissionais import Profissional

from controller.controller_paciente import Controller_Paciente
from controller.controller_profissional import Controller_Profissional

from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Agendamento:
    def __init__(self):
        self.ctrl_paciente = Controller_Paciente()
        self.ctrl_profissional = Controller_Profissional()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_agendamento(self) -> Agendamento:
        # Cria uma nova conexão com o banco
        self.mongo.connect()

        # Lista os pacientes existentes para inserir no agendamento
        self.relatorio.get_relatorio_pacientes()
        cpf = str(input("Digite o número do CPF do Paciente: "))
        paciente = self.valida_paciente(cpf)
        if paciente is None:
            return None

        # Lista os profissionais existentes para inserir no agendamento
        self.relatorio.get_relatorio_profissionais()
        licenca = str(input("Digite o número da Licença do Profissional: "))
        profissional = self.valida_profissional(licenca)
        if profissional is None:
            return None

        data_hoje = datetime.today().strftime("%m-%d-%Y")

        proximo_agendamento = self.mongo.db["agendamentos"].aggregate([
            {
                '$group': {
                    '_id': '$agendamentos',
                    'proximo_agendamento': {'$max': '$cod_relacionamento'}
                }
            }, {
                '$project': {
                    'proximo_agendamento': {'$sum': ['$proximo_agendamento', 1]},
                    '_id': 0
                }
            }
        ])

        proximo_agendamento_lista = list(proximo_agendamento)
        if proximo_agendamento_lista:
            proximo_agendamento = int(proximo_agendamento_lista[0]['proximo_agendamento'])
        else:
            proximo_agendamento = 1  # ou outro valor padrão se a lista estiver vazia

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(cod_relacionamento=proximo_agendamento, cpf=paciente.get_cpf(), licenca=profissional.get_licenca())
        
        # Insere e Recupera o _id do novo agendamento
        id_agendamento = self.mongo.db["agendamentos"].insert_one(data).inserted_id

        # Recupera os dados do novo agendamento criado transformando em um DataFrame
        df_agendamento = self.recupera_agendamento(id_agendamento)

        # Cria um novo objeto Agendamento
        novo_agendamento = Agendamento(df_agendamento.cod_relacionamento.values[0], paciente, profissional)

        # Exibe os atributos do novo agendamento
        print(novo_agendamento.to_string())

        self.mongo.close()

        # Retorna o objeto novo_agendamento para utilização posterior, caso necessário
        return novo_agendamento

    def atualizar_agendamento(self) -> Agendamento:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        cod_relacionamento = int(input("Código de Agendamento/Relacionamento que irá alterar: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_agendamento(cod_relacionamento):

            # Lista os pacientes existentes para inserir no agendamento
            self.relatorio.get_relatorio_pacientes()
            cpf = str(input("Digite o número do CPF do Paciente: "))
            paciente = self.valida_paciente(cpf)
            if paciente == None:
                return None

            # Lista os profissionais existentes para inserir no agendamento
            self.relatorio.get_relatorio_profissionais()
            licenca = str(input("Digite a licença do Profissional: "))
            profissional = self.valida_profissional(licenca)
            if profissional == None:
                return None

            data_hoje = datetime.today().strftime("%m-%d-%Y")

            # Atualiza a descrição do produto existente
            self.mongo.db["agendamentos"].update_one({"cod_relacionamento":cod_relacionamento}, {"$set": {"licenca": f'{profissional.get_licenca()}', "cpf":  f'{paciente.get_cpf()}'}})
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_agendamento = self.recupera_agendamento_codigo(cod_relacionamento)
            # Cria um novo objeto Produto
            agendamento_atualizado = Agendamento(df_agendamento.cod_relacionamento.values[0], paciente, profissional)
            # Exibe os atributos do novo produto
            print(agendamento_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto agendamento_atualizado para utilização posterior, caso necessário
            return agendamento_atualizado
        else:
            self.mongo.close()
            print(f"O código {cod_relacionamento} não existe.")
            return None

    def excluir_agendamento(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        cod_relacionamento = int(input("Código do Agendamento/Relacionamento que irá excluir: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_agendamento(cod_relacionamento):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_agendamento = self.recupera_agendamento_codigo(cod_relacionamento)
            paciente = self.valida_paciente(df_agendamento.cpf.values[0])
            profissional = self.valida_profissional(df_agendamento.licenca.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o agendamento {cod_relacionamento} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, caso o agendamento possua itens, também serão excluídos!")
                opcao_excluir = input(f"Tem certeza que deseja excluir o agendamento {cod_relacionamento} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome o produto da tabela
                    self.mongo.db["itens_agendamento"].delete_one({"cod_relacionamento": cod_relacionamento})
                    print("Itens do agendamento removidos com sucesso!")
                    self.mongo.db["agendamentos"].delete_one({"cod_relacionamento": cod_relacionamento})
                    # Cria um novo objeto Produto para informar que foi removido
                    agendamento_excluido = Agendamento(df_agendamento.cod_relacionamento.values[0], paciente, profissional)
                    self.mongo.close()
                    # Exibe os atributos do produto excluído
                    print("Agendamento Removido com Sucesso!")
                    print(agendamento_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O código {cod_relacionamento} não existe.")

    def verifica_existencia_agendamento(self, codigo:int=None, external: bool = False) -> bool:
        # Recupera os dados do novo agendamento criado transformando em um DataFrame
        df_agendamento = self.recupera_agendamento_codigo(codigo=codigo, external=external)
        return df_agendamento.empty

    def recupera_agendamento(self, _id:ObjectId=None) -> bool:
        # Recupera os dados do novo agendamento criado transformando em um DataFrame
        df_agendamento = pd.DataFrame(list(self.mongo.db["agendamentos"].find({"_id":_id}, {"cod_relacionamento": 1, "cpf": 1, "licenca": 1, "_id": 0})))
        return df_agendamento

    def recupera_agendamento_codigo(self, codigo:int=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo agendamento criado transformando em um DataFrame
        df_agendamento = pd.DataFrame(list(self.mongo.db["agendamentos"].find({"cod_relacionamento": codigo}, {"cod_relacionamento": 1, "cpf": 1, "licenca": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_agendamento









    def valida_paciente(self, cpf:str=None) -> Paciente:
        if self.ctrl_paciente.verifica_existencia_paciente(cpf=cpf, external=True):
            print(f"O CPF {cpf} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo paciente criado transformando em um DataFrame
            df_paciente = self.ctrl_paciente.recupera_paciente(cpf=cpf, external=True)
            # Cria um novo objeto paciente
            paciente = Paciente(df_paciente.cpf.values[0], df_paciente.nome.values[0], df_paciente.idade.values[0], df_paciente.tamanho_abdominal.values[0], df_paciente.altura_cm.values[0], df_paciente.peso_kg.values[0])
            return paciente

    def valida_profissional(self, licenca:str=None) -> Profissional:
        if self.ctrl_profissional.verifica_existencia_profissional(licenca, external=True):
            print(f"A licença {licenca} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo profissional criado transformando em um DataFrame
            df_profissional = self.ctrl_profissional.recupera_profissional(licenca, external=True)
            # Cria um novo objeto profissional
            profissional = Profissional(df_profissional.licenca.values[0], df_profissional.nome_profissional.values[0], df_profissional.especialidade.values[0], df_profissional.contato_envio.values[0])
            return profissional