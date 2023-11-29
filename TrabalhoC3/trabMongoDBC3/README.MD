# Exemplo de Sistema em Python fazendo CRUD no Oracle

Esse sistema de exemplo é composto por um conjunto de tabelas que representam agendamentos de consultas, contendo tabelas como: pacientes, medicos, agendamentos.

O sistema exige que as coleções existam, então basta executar o script Python a seguir para criação das coleções e preenchimento de dados de exemplos:
```shell
~$ python createCollectionsAndData.py
```

Para executar o sistema basta executar o script Python a seguir:
```shell
~$ python principal.py
```


## Organização
- [diagrams](diagrams): Nesse diretório está o [diagrama relacional](diagrams/SistemaConsulta.pdf) (lógico) do sistema.
    * O sistema possui três entidades: PACIENTES, MEDICOS, AGENDAMENTOS
    * [conexion](src/conexion): * [conexion](src/conexion): Nesse repositório encontra-se o [módulo de conexão com o banco de dados Oracle](src/conexion/oracle_queries.py) e o [módulo de conexão com o banco de dados Mongo](src/conexion/mongo_queries.py). Esses módulos possuem algumas funcionalidades úteis para execução de instruções. O módulo do Oracle permite obter como resultado das queries JSON, Matriz e Pandas DataFrame. Já o módulo do Mongo apenas realiza a conexão, os métodos CRUD e de recuperação de dados são implementados diretamente nos objetos controladores (_Controllers_) e no objeto de Relatório (_reports_).

      - Exemplo de utilização para consultas simples:

        - Exemplo de utilização para conexão no Mongo;
      ```python
            # Importa o módulo MongoQueries
            from conexion.mongo_queries import MongoQueries
            
            # Cria o objeto MongoQueries
            mongo = MongoQueries()

            # Realiza a conexão com o Mongo
            mongo.connect()

            """<inclua aqui suas declarações>"""

            # Fecha a conexão com o Mong
            mongo.close()
      ```
      - Exemplo de criação de um documento no Mongo:
      ```python
            from conexion.mongo_queries import MongoQueries
            import pandas as pd
            
            # Cria o objeto MongoQueries
            mongo = MongoQueries()

            # Realiza a conexão com o Mongo
            mongo.connect()

            # Solicita ao usuario o novo CPF
            cpf = input("CPF (Novo): ")
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            # Insere e persiste o novo paciente
            mongo.db["pacientes"].insert_one({"cpf": cpf, "nome": nome})
            # Recupera os dados do novo paciente criado transformando em um DataFrame
            df_paciente = pd.DataFrame(list(mongo.db["pacientes"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "_id": 0})))
            # Exibe os dados do paciente em formato DataFrame
            print(df_paciente)

            # Fecha a conexão com o Mong
            mongo.close()


    * [controller](src/controller/): Nesse diretório encontram-sem as classes controladoras, responsáveis por realizar inserção, alteração e exclusão dos registros das tabelas.
    * [model](src/model/): Nesse diretório encontram-ser as classes das entidades descritas no [diagrama relacional](diagrams/DIAGRAMA_RELACIONAL_AGENDAMENTOS.pdf)
    * [reports](src/reports/) Nesse diretório encontra-se a [classe](src/reports/relatorios.py) responsável por gerar todos os relatórios do sistema
    * [sql](src/sql/): Nesse diretório encontram-se os scripts utilizados para geração dos relatórios a partir da [classe relatorios](src/reports/relatorios.py)
    * [utils](src/utils/): Nesse diretório encontram-se scripts de [configuração](src/utils/config.py) e automatização da [tela de informações iniciais](src/utils/splash_screen.py)
    * [create_tables_and_records.py](src/create_tables_and_records.py): Script responsável por criar as tabelas e registros fictícios. Esse script deve ser executado antes do script [principal.py](src/principal.py) para gerar as tabelas, caso não execute os scripts diretamente no SQL Developer ou em alguma outra IDE de acesso ao Banco de Dados.
    * [principal.py](src/principal.py): Script responsável por ser a interface entre o usuário e os módulos de acesso ao Banco de Dados. Deve ser executado após a criação das tabelas.

### Bibliotecas Utilizadas
- [requirements.txt](src/requirements.txt): `pip install -r requirements.txt`
