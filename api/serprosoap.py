from zeep import Client
import copy

from constantes import *
from serprotools import *
from serpro_utils import SerproUtils

# API-SERPRO
# esse módulo faz requisições ao servidor web do serpro

client = Client(wsdl=WSDL)

class SerproSiape:

	@staticmethod
	def identificao_unica(cpf):
		try:
			str_saida = client.service.pesquisarServidorCpf(cpf,TOKEN)
			iu, nome = formatar_identificacao_unica(str_saida)			
			return iu, nome					
		except:			
			return "", "" 

	@classmethod
	def consulta_obito(self, cpf):
		iu, nome = SerproSiape.identificao_unica(cpf)
		if iu:
			try:
				str_saida=client.service.getDataObitoServidor(iu,TOKEN)		
				data_obito = formatar_data_obito(str_saida)
				return cpf, nome, data_obito
			except:
				return cpf,"",""

	@classmethod
	def extrair_ficha_financeira(self, cpf, ano_inicial, ano_final):		
		iu, nome = SerproSiape.identificao_unica(cpf)		
		if iu:
			try:
				str_saida = client.service.montarFichaFinanceiraServidor(iu, ano_inicial, ano_final,TOKEN)				
				return str_saida
			except:
				return ""
			
	
	@classmethod
	def buscar_ocorrencias_servidor(self, cpf, ano_final, mes_final):
		anomes = formatar_ano_mes(ano_final, mes_final)		
		iu, _ = SerproSiape.identificao_unica(cpf)		
		if iu:
			try:
				str_saida = client.service.getOcorrenciasServidor(iu, anomes,TOKEN)				
				return str_saida
			except:
				return ""
			
	@classmethod
	def consultar_beneficiario(self, cpf): #cpf beneficiario		
		try:
			str_saida = client.service.pesquisarBeneficiarioCpf(cpf,TOKEN)				
			return str_saida #matricula beneficiario e nome beneficiario
		except:
			return ""

	@classmethod
	def pesquisar_beneficiario_pelo_nome(self, nome):
		try:
			str_saida = client.service.findBeneficiadoByNome(nome,TOKEN)			
			dados = [{"nome": item["nome"], "cpf": item["cpf"], "matricula": item["matricula"]} for item in str_saida]			
			return dados
		except:
			return ""	
	
	@classmethod
	def consultar_beneficiario_instituidores(self, cpf): #cpf do beneficiario
		matricula = SerproSiape.consultar_beneficiario(cpf)['matricula']	# mat beneficiario	
		try:
			str_saida = client.service.retornarBeneficiarioInstituidores(matricula,TOKEN)				
			info(f'str_saida:\n{str_saida}')
			return str_saida 
			# nome,cpf,matricula beneficiario e nome,iu,matricula instituidor
			# cpf = '36030007068'		
		except:
			return ""
		





"""
	deve retornar um dicionário da seguinte forma:
			
	fichas={	IU1 : {'cadastro:{ dados_cadastro }, 'registros':{ lancamentos}},
				IU2 : {'cadastro:{ dados_cadastro }, 'registros':{ lancamentos}},
	 			...
	 			IUn : {'cadastro:{ dados_cadastro }, 'registros':{ lancamentos}
	 		}
	dados_cadastro={ {'iu':1234, 'nome':"joaquim", 
					   registros[{ 'ano':1992,
					   				'orgao':123,
					   				'matricula':123,
					   				'codgcargo':12,
					   				'codcargo':22, 
					   				'classe':'C', 
					   				'padrao': 'VI', 
					   				sigla: 'EST'}, {...},{...}
					   			]
	lancamentos=[
					[1992, 25000, 1, 1, 0, [0, 0, 0, 0, 0, 938364.73, 938364.73, 938364.73, 1126037.67, 2506028.98, 2506028.98, 2506028.98]], 
					[1992, 25000, 13, 1, 0, [0, 0, 0, 0, 0, 9383.64, 9383.64, 9383.64, 11260.37, 25060.28, 25060.28, 50120.57]], 
					[1992, 25000, 53, 1, 1, [0, 0, 0, 0, 0, 93836.47, 9383.64, 9383.64, 11260.37, 25060.28, 25060.28, 25060.28]], 
					[1992, 25000, 92, 1, 0, [0, 0, 0, 0, 0, 4044.39, 4044.36, 4044.36, 4853.52, 4853.22, 4853.22, 4853.22]], 
					[1992, 25000, 224, 1, 1, [0, 0, 0, 0, 0, 637866.04, 637866.04, 637866.04, 637866.04, 0, 0, 0]], 
					[1992, 25000, 591, 1, 0, [0, 0, 0, 0, 0, 0, 0, 0, 337811.3, 751808.69, 2004823.18, 2004823.18]],
				]	

"""

"""
Case 1: tmp = "https://app.sicap.agu.gov.br/SiapeSicapService/ServicoSiape/"



Case 5: tmp = "https://app.sicap.agu.gov.br/SiapeSicapService/ServicoSiape/findBeneficioAndBeneficiadoAndServidorAndInstituidorAndOrgaoByCodigoOrgaoAndMatriculaBeneficiadoAndMesAnoBeneficio"
Case 6: tmp = "https://app.sicap.agu.gov.br/SiapeSicapService/ServicoSiape/findBeneficiadoByNome"
Case 7: tmp = "https://app.sicap.agu.gov.br/SiapeSicapService/ServicoSiape/findOrgaoByCodigoAndSituacao"
Case 8: tmp = "https://app.sicap.agu.gov.br/SiapeSicapService/ServicoSiape/findDadosFuncionaisByIdentificacaoUnicaAndOrgaoAndPeriodoAndAgrupamento"
Case 9: tmp = "https://app.sicap.agu.gov.br/SiapeSicapService/ServicoSiape/listarServidorNome"
Case 12: tmp = "https://app.sicap.agu.gov.br/SiapeSicapService/ServicoSiape/getHistoricoBeneficio"
Case 13: tmp = "https://app.sicap.agu.gov.br/SiapeSicapService/ServicoSiape/pesquisarServidorMatricula"
Case 14: tmp = "https://app.sicap.agu.gov.br/SiapeSicapService/ServicoSiape/getFichaFinanceira"
        






"""