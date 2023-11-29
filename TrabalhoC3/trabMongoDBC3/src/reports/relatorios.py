from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_pacientes(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["pacientes"].find({}, 
                                                 {"cpf": 1, 
                                                  "nome": 1, 
                                                  "idade": 1,
                                                  "tamanho_abdominal": 1,
                                                  "altura_cm": 1,
                                                  "peso_kg": 1,
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        df_paciente = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_paciente)
        input("Pressione Enter para Sair do Relatório de Pacientes")

    def get_relatorio_profissionais(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["profissionais"].find({}, 
                                                     {"licenca": 1, 
                                                      "nome_profissional": 1, 
                                                      "especialidade": 1,
                                                      "contato_envio": 1,
                                                      "_id": 0
                                                     }).sort("nome", ASCENDING)
        df_profissional = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_profissional)        
        input("Pressione Enter para Sair do Relatório de Profissionais")

    def get_relatorio_agendamentos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["agendamentos"].aggregate([
                                                    {
                                                        '$lookup': {
                                                            'from': 'profissionais', 
                                                            'localField': 'licenca', 
                                                            'foreignField': 'licenca', 
                                                            'as': 'profissional'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$profissional'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'cod_relacionamento': 1, 
                                                            'profissional': '$profissional.nome_profissional', 
                                                            'cpf': 1, 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'pacientes', 
                                                            'localField': 'cpf', 
                                                            'foreignField': 'cpf', 
                                                            'as': 'paciente'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$paciente'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'cod_relacionamento': 1, 
                                                            'profissional': 1, 
                                                            'paciente': '$paciente.nome', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$sort': {
                                                            'paciente': 1,
                                                            'item_agendamento': 1
                                                        }
                                                    }
                                                ])
        df_agendamento = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        print(df_agendamento[["cod_relacionamento", "paciente", "profissional"]])
        input("Pressione Enter para Sair do Relatório de Agendamento")