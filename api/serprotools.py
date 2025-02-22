from copy import deepcopy
from collections import defaultdict
from configura_debug import *


class ExtracaoRubricas():
	
	def __init__(self,ficha):
		self.ficha = ficha

	
	def ajustar_dados(self, dados):
		# Lista original com os dicionários contendo "__values__"
		# dados = [
    	# {"__values__": {...}},  # Exemplo do primeiro dicionário
    	# {"__values__": {...}},  # Exemplo do segundo dicionário
    	# # ... (outros dicionários)
		# ]
		# Removendo o campo "__values__" e criando uma nova lista
		dados_limpos = [item["__values__"] for item in dados]
		return dados_limpos
	


	'''
dados_limpos = ExtracaoRubricas.ajustar_dados(str_saida)
			info(f'dados limpos: {dados_limpos}')
			 
			dados_filtrados = [{"nome": item["nome"], "cpf": item["cpf"]} for item in dados_limpos]
			info(f'filtrados: {dados_filtrados}')
			
	'''
	
	def retirar_nome_cpf_beneficiario(self):
		...


	def percorrer_periodo_extracao(self):
		for i in range(len(self.ficha)):
			periodo = self.ficha[i]
			self.processar_periodo_extracao(periodo)

	def percorrer_vinculos(self):
		for i in range(len(self.ficha)):
			vinculo = self.ficha[i]['vinculos']['vinculo']
			for j in range(len(vinculo)):
				self.processar_vinculos(vinculo[j])
	
	def percorrer_ficha_financeira(self):
		lista = []
		for i in range(len(self.ficha)):
			vinculo = self.ficha[i]['vinculos']['vinculo']
			for j in range(len(vinculo)):
				codorgao = vinculo[j]['codOrgao']
				elementos = vinculo[j]['fichaFinanceira']['itemFichaFinanceira']			
				for k in range(len(elementos)):
					dicionario = self.processar_elementos_ficha(elementos[k],codorgao)
					lista.append(dicionario)
		
		dict1 = {'rubricas': lista}
		dict_ordenado = sorted(dict1["rubricas"], key=lambda x: x["datapagto"])	
		return dict_ordenado


	
	def processar_elementos_ficha(self,itemficha, codorgao):
		dicionario={}
		codigo_rubrica = itemficha['codigo']
		data_pagamento = itemficha['dataPagamento']
		valor = itemficha['valor']
		rendimento = itemficha['rendimento']
		sequencia = itemficha['sequencia']
		sinalfolha = itemficha['sinalFolha']		
		dicionario['codorgao'] = codorgao
		dicionario['codrubrica'] = codigo_rubrica
		dicionario['datapagto'] = data_pagamento
		dicionario['valor'] = valor
		dicionario['rendimento'] = rendimento
		dicionario['sequencia'] = sequencia
		dicionario['sinalfolha'] = sinalfolha
		
		"""print (f"Órgão: {codorgao}")
		print (f"Código rubrica: {codigo_rubrica}")
		print (f"Data pagamento: {data_pagamento}")
		print (f"Valor: {valor}")
		print (f"Rendimento: {rendimento}")
		print (f"Sequencia: {sequencia}")
		print (f"sinalfolha: {sinalfolha}")
		print ("-----------------------------")
		"""
		return dicionario

	def processar_vinculos(self,itemficha):
		codorgao = itemficha['codOrgao']
		matricula = itemficha['matricula']

		# print (f"Código órgao: {codorgao}")
		# print (f"Matrícula: {matricula}")
		# print ("-----------------------------")	

	def processar_periodo_extracao(self,itemficha):
		ano = itemficha['ano']
		nome = itemficha['nome']
		iu = itemficha['identificacaoUnica']

		# print (f"Ano: {ano}")
		# print (f"Nome: {nome}")
		# print (f"IU: {iu}")
		# print ("-----------------------------")


	def separar_rubricas_por_orgao(self, codigo_orgao):

		dados_por_codOrgao = defaultdict(list)
		dados = []
		codigo_orgao = str(codigo_orgao)		

		# Percorre a ficha para extrair os dados financeiros agrupados por codOrgao
		for pessoa in self.ficha:
			#info(f'pessoa:\n{pessoa}')
			for vinculo in pessoa['vinculos']['vinculo']:
				codOrgao = vinculo['codOrgao']
				
				#info(f'codOrgao:{codOrgao}')
				#info(f'codigo_orgao: {codigo_orgao}')

				if codigo_orgao == '' or codigo_orgao == str(codOrgao):
					
					if 'fichaFinanceira' in vinculo and 'itemFichaFinanceira' in vinculo['fichaFinanceira']:
						for item in vinculo['fichaFinanceira']['itemFichaFinanceira']:
							
							dados_por_codOrgao[codOrgao].append({
								'codorgao': codOrgao,
								'codrubrica': item['codigo'],
								'rendimento': item['rendimento'],
								'sequencia': item['sequencia'],
								'datapagto': item['dataPagamento'],
								'valor': item['valor'],
								'sinalfolha': item['sinalFolha']
							})
	
		# Exibir os resultados organizados por codOrgao
		for codOrgao, items in dados_por_codOrgao.items():		
			for item in items:
				dados.append(item)	
				 
		return dados

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


def obter_orgaos_por_periodo(ficha):
	lista_orgaos = []
	lista = []
	dicionario = {}	
	for i in range(len(ficha)):
		ano = ficha[i]['ano']
		nivel1 = ficha[i]['vinculos']['vinculo']
    
		for j in range(len(nivel1)):
			orgao = nivel1[j]['codOrgao']               
			lista_orgaos.append(orgao)
    		
		dicionario['ano']= ano
		dicionario['orgaos']= lista_orgaos   
		lista_orgaos= []
		lista.append(dicionario)
		dicionario= {}    
	
	return lista #"Em teste ainda"
     

def formatar_ficha_financeira():
	pass


def formatar_rubricas():
	pass


def filtrar_ficha_pelo_orgao(str_saida, orgao):
	pass

def filtrar_rubricas_selecionadas():	
		
	pass

#_____________________________________________________________________



def formataDadosServidor (envelope):
	
	dict_dados_servidor = {}
	
	iu = envelope['identificacaoUnica']
	nome = envelope['nome']
	cpf = envelope['CPF']
	
	dict_dados_servidor['iu'] = iu
	dict_dados_servidor['cpf']= cpf
	dict_dados_servidor['nome'] = nome
	
	return dict_dados_servidor

  
def formataDataDeObito (envelope):
	
	str_envelope = str(envelope)

	if len(str_envelope) > 10:
		ano = str_envelope[0:4]
		mes = str_envelope[5:7]
		dia = str_envelope[8:10]
		datadeobito = dia + '/' + mes + "/" + ano

	return datadeobito


def formataFichaFinanceira(envelope):

	def remove_repetidos(l0):
		l = []
		for i in l0:
			if i not in l:
				l.append(i)
				l.sort()
		return l

	def posicao_sufixo_meses(anomes):
		pos = int(str(anomes)[4:6]) - 1
		return pos

	def insere_pagamentos(lista1, lista2):
		l1 = deepcopy(lista1)
		l2 = deepcopy(lista2)

		for n in range(len(l1)):

			ano1 = l1[n][0]
			org1 = l1[n][1]
			rub1 = l1[n][2]
			nom1 = l1[n][3]
			ren1 = l1[n][4]
			seq1 = l1[n][5]

			for m in range(len(l2)):

				ano2 = l2[m][0]
				org2 = l2[m][1]
				rub2 = l2[m][2]
				nom2 = l2[m][3]
				ren2 = l2[m][4]
				seq2 = l2[m][5]
				dat2 = l2[m][6]
				vlr2 = l2[m][7]

				if ano1 == ano2 and org1 == org2 and rub1 == rub2 and ren1 == ren2 and seq1 == seq2:
					pos = posicao_sufixo_meses(dat2)
					l1[n][6][pos] = vlr2

		return l1

	def consolidar_registros(registros):

		reg_aux = deepcopy(registros)

		# cria uma lista sem a data e o valor pago
		lista_aux = []
		for i in range(len(reg_aux)):
			aux = reg_aux[i]
			del aux[7]
			del aux[6]
			lista_aux.append(aux)

		# ordena a lista criada
		lista_ord = []
		lista_ord = remove_repetidos(lista_aux)

		# insere na lista ordenada e sem repetições
		# o sufixo com os meses
		for i in range(len(lista_ord)):
			lista_ord[i].append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

		x1 = [] + lista_ord
		x2 = deepcopy(registros)

		lista_final = []
		lista_final = insere_pagamentos(x1, x2)

		return lista_final
	

	ficha = envelope	
	quantidade_fichas = len(ficha)		
	#print ("Quantidade de fichas:", quantidade_fichas)

	registros, cadastros = [], []
		
	#rubricas_db = Rubricas.objects.all()
	#for j in rubricas_db:
	#	print(j)
		
	#rub = Rubricas.objects.get(codigorubrica='13')
	#print ("Rubrica:", rub.nomerubrica)
	#print("quantidade_fichas:" + str(quantidade_fichas))
	
	if quantidade_fichas > 0:
			
		for i in range(quantidade_fichas):
				
			servidor = ficha[i]['nome']
			cpf = ficha[i]['CPF']
			ano = ficha[i]['ano']
			iu = ficha[i]['identificacaoUnica']
			
			#print ("Ficha Financeira de: ", ano, '\n')
			#print ("Servidor: ",iu, ' - ', servidor, '\n', )

			quantidade_vinculos = len(ficha[i]['vinculos']['vinculo'])
			#print ("Quantidade de vínculos na ficha:", i, " :", quantidade_vinculos)		
			
			#print('(1) ========================')
			#print(ficha[i])

			for j in range(quantidade_vinculos):			
				
				codigo_orgao = ficha[i]['vinculos']['vinculo'][j]['codOrgao']
				matricula = ficha[i]['vinculos']['vinculo'][j]['matricula']
				codigo_grupo_cargo = ficha[i]['vinculos']['vinculo'][j]['codGrupoCargo']
				codigo_cargo = ficha[i]['vinculos']['vinculo'][j]['codCargo']
				classe = ficha[i]['vinculos']['vinculo'][j]['classe']
				padrao = ficha[i]['vinculos']['vinculo'][j]['padrao']
				sigla_regime = ficha[i]['vinculos']['vinculo'][j]['siglaRegimeJuridico']
				
				quantidade_itens=len(ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'])
				
				#print("CodCargo:",codigo_cargo,"    CodGrupoCargo:",codigo_grupo_cargo)
				#print("(2) =============================")
				#print(ficha[i]['vinculos']['vinculo'][j])
				nomecargo = ''
				#try:
				#	nomeorgao = OrgaoSiape.objects.get(codigo=str(codigo_orgao))
				#except:
				#	nomeorgao = 'Não informado'

				
				#if codigo_cargo != 0 and codigo_grupo_cargo != 0:
				#	try:
						#nomecargo = CargoEmprego.objects.get(codcargo=codigo_cargo, codgrupocargo=codigo_grupo_cargo)
					#except:
				#		nomecargo = 'Não informado'
				
				cad = {'ano':ano,'orgao':codigo_orgao,'matricula':matricula,'codgcargo':codigo_grupo_cargo,'codcargo':codigo_cargo,'classe':classe,'padrao':padrao,'sigla':sigla_regime,'nomeorgao':nomeorgao,'nomecargo':nomecargo}
				cadastros.append(cad)

				for k in range(quantidade_itens):
					
					rubrica = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['codigo']
					rendimento = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['rendimento']
					sequencia = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['sequencia']
					datapgto = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['dataPagamento']
					valor = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['valor']
					
					try:
						nomerubrica = Rubricas.objects.get(codigorubrica=str(rubrica))
					except:
						nomerubrica = 'N/I'
										
					reg = [ano,codigo_orgao, rubrica, str(nomerubrica), rendimento,sequencia,datapgto,float(valor)]
					registros.append(reg)
					
		print ("Servidor: ",iu, ' - ', servidor, '\n', )
		dados_cadastro = {'iu':iu,'nome':servidor,'registros':cadastros}
	else:
		dados_cadastro = {'iu':'','nome':'','registros':''}
		
	#print ("Cadastros:----------------------------------")
	#for i in cadastros:
	#	print (i)
	#print("Dados cadastro:--------------------------------")
	#for i in dados_cadastro.items():
	#	print (i)
	
	#print("=============================================")
	#print ()
	#print("=============================================")

	registros_meses_consolidados =[]
	registros_meses_consolidados = consolidar_registros(registros)

	dicionario = {'cadastro':dados_cadastro,'lancamentos':registros_meses_consolidados}
	
	return dicionario
	


	
			


