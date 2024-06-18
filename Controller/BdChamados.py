from psycopg2 import OperationalError
import psycopg2
import logging

class BancoChamados:
    def __init__(self, host, port, user, password, dbname):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.conexao_bd_chamados = None

    def RealizaConexaoBdChamados(self):
        try:
            self.conexao_bd_chamados = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname=self.dbname
            )
            print(f"Conexão bem-sucedida ao banco de dados {self.dbname}.")
            return self.conexao_bd_chamados
        except psycopg2.OperationalError as e:
            print(f"O erro '{e}' ocorreu ao tentar conectar ao banco de dados {self.dbname}.")
            return self.conexao_bd_chamados

    def RealizaInsertDadosChamados(self, lista_dados_chamados):
        try:
            cursor = self.conexao_bd_chamados.cursor()
            for registro in lista_dados_chamados:
                cursor.execute("""
                    INSERT INTO chamadosmovimentacao (idchamado, origem, destino, cpf, cnpj, statusmovimentacao)
                    VALUES (%s, %s, %s, %s, %s, %s)""", registro)
            self.conexao_bd_chamados.commit()
            logging.info("Registros inseridos com sucesso!")
        except psycopg2.OperationalError as e:
            print(f"O erro '{e}' ocorreu ao tentar conectar ao banco de dados {self.dbname}.")

    def DesconectaBdChamados(self):
        if self.conexao_bd_chamados:
            self.conexao_bd_chamados.close()
            print(f"Conexão com o banco de dados {self.dbname} fechada.")
