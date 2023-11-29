import pandas as pd
from model.profissionais import Profissional
from conexion.mongo_queries import MongoQueries

class Controller_Profissional:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_profissional(self) -> Profissional:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuario o novo Licença
        licenca = input("Licença (Novo): ")

        if self.verifica_existencia_profissional(licenca):
            nome_profissional = input("Nome (Novo): ")
            especialidade = input("Especialidade (Novo): ")
            contato_envio = input("Contato (Novo): ")
            # Insere e persiste o novo profissional
            self.mongo.db["profissionais"].insert_one({"licenca": licenca, "nome_profissional": nome_profissional, "especialidade": especialidade, "contato_envio": contato_envio})
            # Recupera os dados do novo profissional criado transformando em um DataFrame
            df_profissional = self.recupera_profissional(licenca)
            # Cria um novo objeto profissional
            novo_profissional = Profissional(df_profissional.licenca.values[0], df_profissional.nome_profissional.values[0], df_profissional.especialidade.values[0], df_profissional.contato_envio.values[0])
            # Exibe os atributos do novo profissional
            print(novo_profissional.to_string())
            self.mongo.close()
            # Retorna o objeto profissional para utilização posterior, caso necessário
            return novo_profissional
        else:
            self.mongo.close()
            print(f"A licença {licenca} já está cadastrado.")
            return None
        
    def atualizar_profissional(self) -> Profissional:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do profissional a ser alterado
        licenca = int(input("Licença do profissional que deseja atualizar: "))

        # Verifica se o profissional existe na base de dados
        if not self.verifica_existencia_profissional(licenca):
            # Solicita ao usuario a nova Valor Consulta
            nome_profissional = input("Nome (Novo): ")
            especialidade = input("Especialidade (Novo): ")
            contato_envio = input("Contato (Novo): ")         
            # Atualiza o nome do profissional existente
            self.mongo.db["profissionais"].update_one({"licenca": f"{licenca}"}, {"$set": {"nome_profissional": nome_profissional}, "$set": {"especialidade": especialidade}, "$set": {"contato_envio": contato_envio}})

            # Recupera os dados do novo profissional criado transformando em um DataFrame
            df_profissional = self.recupera_profissional(licenca)
            # Cria um novo objeto profissional
            profissional_atualizado = Profissional(df_profissional.licenca.values[0], df_profissional.nome_profissional.values[0], df_profissional.especialidade.values[0], df_profissional.contato_envio.values[0])
            # Exibe os atributos do novo profissional
            print(profissional_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto profissional_atualizado para utilização posterior, caso necessário
            return profissional_atualizado
        else:
            self.mongo.close()
            print(f"A licença {licenca} não existe.")
            return None

    def excluir_profissional(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o CPF do profissional a ser alterado
        licenca = int(input("Licença do profissional que irá excluir: "))        

        # Verifica se o profissional existe na base de dados
        if not self.verifica_existencia_profissional(licenca):            
            # Recupera os dados do novo profissional criado transformando em um DataFrame
            df_profissional = self.recupera_profissional(licenca)
            # Revome o profissional da tabela
            self.mongo.db["profissionais"].delete_one({"licenca":f"{licenca}"})
            # Cria um novo objeto profissional para informar que foi removido
            profissional_excluido = Profissional(df_profissional.licenca.values[0], df_profissional.nome_profissional.values[0], df_profissional.especialidade.values[0], df_profissional.contato_envio.values[0])
            self.mongo.close()
            # Exibe os atributos do profissional excluído
            print("profissional Removido com Sucesso!")
            print(profissional_excluido.to_string())
        else:
            self.mongo.close()
            print(f"A licença {licenca} não existe.")

    def verifica_existencia_profissional(self, licenca:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo profissional criado transformando em um DataFrame
        df_profissional = pd.DataFrame(self.mongo.db["profissionais"].find({"licenca":f"{licenca}"}, {"licenca": 1, "nome_profissional": 1, "especialidade": 1, "contato_envio":1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_profissional.empty

    def recupera_profissional(self, licenca:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo profissional criado transformando em um DataFrame
        df_profissional = pd.DataFrame(list(self.mongo.db["profissionais"].find({"licenca":f"{licenca}"}, {"licenca": 1, "nome_profissional": 1, "especialidade": 1, "contato_envio":1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_profissional