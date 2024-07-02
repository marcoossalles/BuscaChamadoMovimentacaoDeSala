from Controller.BuscaChamados import BuscaChamadosSd
from Controller.BdChamados import BancoChamados
import os
import logging

pagina_atual = 1

start_index = 1

row_count = 100 

classe_busca_chamados = BuscaChamadosSd(start_index=1, row_count=100)

classe_bd_chamados = BancoChamados(host='172.16.0.50', port='5432', user='rpa', password='Jump@@jet@', dbname='rpa')

conexao_bd_chamados = classe_bd_chamados.RealizaConexaoBdChamados()
if conexao_bd_chamados == None:
  logging.info("Ocorreu um erro ao conectar no Banco de dados.")
  exit()


while True:

  lista_ids_chamados = classe_busca_chamados.BuscaListaIdsChamados()

  if lista_ids_chamados is None or len(lista_ids_chamados) == 0:
    logging.info('Não encontramos novos chamados!')
    exit()

  start_index = start_index + len(lista_ids_chamados)
  pagina_atual += 1

  classe_busca_chamados =BuscaChamadosSd(start_index, row_count)

  lista_dados_chamados = classe_busca_chamados.BuscaDadosChamados(lista_ids_chamados)

  if lista_dados_chamados is None:
    logging.info('Não encontramos novos chamados!')
    exit

  classe_bd_chamados.RealizaInsertDadosChamados(lista_dados_chamados)


