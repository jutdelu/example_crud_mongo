MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir
3 - Atualizar
4 - Remover
5 - Sair
"""

MENU_RELATORIOS = """Relatórios
1 - Relatório de Pacientes com Profissionais
2 - Relatório de Pacientes
3 - Relatório de Profissionais
0 - Sair
"""

MENU_ENTIDADES = """Entidades
1 - PACIENTES
2 - PROFISSIONAIS
3 - AGENDAMENTOS
"""

# Consulta de contagem de registros por tabela
def query_count(collection_name):
   from conexion.mongo_queries import MongoQueries
   import pandas as pd

   mongo = MongoQueries()
   mongo.connect()

   my_collection = mongo.db[collection_name]
   total_documentos = my_collection.count_documents({})
   mongo.close()
   df = pd.DataFrame({f"total_{collection_name}": [total_documentos]})
   return df

def clear_console(wait_time:int=3):
    '''
       Esse método limpa a tela após alguns segundos
       wait_time: argumento de entrada que indica o tempo de espera
    '''
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")