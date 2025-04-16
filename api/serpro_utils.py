import unicodedata
from configura_debug import *
from collections import defaultdict

class SerproUtils:

	@classmethod
	def ajustar_dados(self, dados):
		info(f'dados:\n{dados}')
		dict_dados = defaultdict(list)
		info(f'dictdados:\n{dict_dados}')
		# Lista original com os dicionários contendo "__values__"
		# dados = [
    	# {"__values__": {...}},  # Exemplo do primeiro dicionário
    	# {"__values__": {...}},  # Exemplo do segundo dicionário
    	# # ... (outros dicionários)
		# ]
		# Removendo o campo "__values__" e criando uma nova lista
		dados_limpos = [item["__values__"] for item in dados]
		return dados_limpos
	
	@classmethod
	def ajustar_lista_nome_servidor(cls, dados):
		dados_transformados = [
			{
			 'nome': pessoa['nome'],
			 'CPF': pessoa['CPF'],
			 'identificacaoUnica': pessoa['identificacaoUnica']
			}
			for pessoa in dados  # Itera sobre cada dicionário na lista
		]	
		return dados_transformados
	

	@classmethod
	def remover_acentos(cls, texto):		
		texto_normalizado = unicodedata.normalize('NFKD', texto)
		# Filtra apenas caracteres que não são diacríticos (acentos, cedilhas, etc.)
		texto_sem_acentos = ''.join(
			caractere for caractere in texto_normalizado
			if not unicodedata.combining(caractere)
		)
		return texto_sem_acentos




def formatar_ano_mes(anofinal, mesfinal):
	return str(anofinal) + str(mesfinal)

def formatar_identificacao_unica(id_unica):
	iu = id_unica['identificacaoUnica']
	nome = id_unica['nome']
	return iu, nome
	
def formatar_data_obito(data):
	print(f"tipo (data): {type(data)}")		
	
	if data is not None: 
		str_data = str(data)
		if len(str_data) > 10:
			ano = str_data[0:4]
			mes = str_data[5:7]
			dia = str_data[8:10]
			data_obito = dia + '/' + mes + "/" + ano
			return data_obito		
	return "" 
