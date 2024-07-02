import requests
import logging

class BuscaChamadosSd:
    def __init__(self, start_index, row_count):
        self.start_index = start_index
        self.row_count = row_count

    def BuscaListaIdsChamados(self):
        lista_ids = []   
        url = "https://suporte.gavresorts.com.br/api/v3/requests"
        headers = {"authtoken": "40605592-93B7-4820-B4E4-E352FA8A3754"}
        idStatusAberto = "1"
        input_data = {
            "list_info": {
                "row_count": self.row_count,
                "start_index": self.start_index,
                "sort_order": "asc",
                "search_fields": {
                    "status.id": idStatusAberto,
                    "template.id": "2102",
                    "template.name": "Atualização de Cadastro",
                    "service_category.id": "602",
                    "service_category.ciid": "4203"
                }
            }
        }
        params = {'input_data': str(input_data)}    
        try:
            response = requests.get(url, headers=headers, params=params, verify=False)
            if response.status_code == 200:
                data = response.json()
                if "requests" in data:
                    lista_chamados = data["requests"]
                    for item in lista_chamados:
                        lista_ids.append((item['id']))
            return lista_ids
        except Exception as e:
            logging.error(f'Ocorreu um erro ao realizar a requisição: {e}')
            return None
        
    def BuscaDadosChamados(self, lista_ids_chamados):
        info_chamado = []
        lista_info_chamado = []
        lista_chamados_filter = []
        
        for id in lista_ids_chamados:
            url = f"https://suporte.gavresorts.com.br/api/v3/requests/{id}"
            headers = {"authtoken": "40605592-93B7-4820-B4E4-E352FA8A3754"}
            
            try:
                response = requests.get(url, headers=headers, verify=False)
                if response.status_code == 200:
                    info_chamado.append(response.json())
            except Exception as e:
                logging.error(f'Falha ao buscar chamado por ID {e}')
                return None
            
        for item_chamados in info_chamado:
            lista_info_chamado.append((item_chamados['request']['id'], item_chamados['request']['udf_fields']))

        for item in lista_info_chamado:
            id_chamado = item[0]
            origem = item[1].get('udf_pick_4804', {})
            destino = item[1].get('udf_pick_4803', {})
            movimentacao = item[1].get('udf_pick_4801', {})
            cpf = item[1].get('udf_sline_620', {})
            cnpj = item[1].get('udf_sline_606', {})
            if movimentacao == 'Sim':
                lista_chamados_filter.append([id_chamado, origem, destino, cpf, cnpj, False])
        return lista_chamados_filter