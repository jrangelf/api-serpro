import asyncio
from concurrent.futures import ThreadPoolExecutor

from zeep import Client
import copy

from constantes import *
from serprotools import *
from serpro_utils import SerproUtils

""" 
Aqui são feitas requisições ao servidor web do SERPRO via SOAP.
As bibliotecas que fazem chamadas SOAP (zeep) não suportam operações assíncronas nativamente.
Assim, executa-se as funções bloqueantes em um thread separado usando run_in_executor(), tornando a API responsiva.
"""

client = Client(wsdl=WSDL)

class SerproSiape:
    
	    
    executor = ThreadPoolExecutor()

    @staticmethod
    def _identificao_unica_sync(cpf):
        """Versão síncrona da consulta de identificação única"""
        try:
            str_saida = client.service.pesquisarServidorCpf(cpf, TOKEN)
            return formatar_identificacao_unica(str_saida)
        except:
            return "", ""

    @classmethod
    async def identificao_unica(cls, cpf):
        """Versão assíncrona da consulta de identificação única"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(cls.executor, cls._identificao_unica_sync, cpf)



    @staticmethod
    def _consulta_obito_sync(iu, cpf, nome):
        """Versão síncrona da consulta de óbito"""
        try:
            str_saida = client.service.getDataObitoServidor(iu, TOKEN)
            data_obito = formatar_data_obito(str_saida)
            return cpf, nome, data_obito
        except:
            return cpf, "", ""

    @classmethod
    async def consulta_obito(cls, cpf):
        loop = asyncio.get_running_loop()
        iu, nome = await cls.identificao_unica(cpf)
        if iu:
            return await loop.run_in_executor(cls.executor, cls._consulta_obito_sync, iu, cpf, nome)
        return cpf, "", ""


    @staticmethod
    def _extrair_ficha_financeira_sync(iu, ano_inicial, ano_final):
        """Versão síncrona da extração da ficha financeira"""
        try:
            return client.service.montarFichaFinanceiraServidor(iu, ano_inicial, ano_final, TOKEN)
        except:
            return ""

    @classmethod
    async def extrair_ficha_financeira(cls, cpf, ano_inicial, ano_final):
        loop = asyncio.get_running_loop()
        iu, _ = await cls.identificao_unica(cpf)
        if iu:
            return await loop.run_in_executor(cls.executor, cls._extrair_ficha_financeira_sync, iu, ano_inicial, ano_final)
        return ""


    @staticmethod
    def _buscar_ocorrencias_servidor_sync(iu, anomes):
        """Versão síncrona da busca de ocorrências"""
        try:
            return client.service.getOcorrenciasServidor(iu, anomes, TOKEN)
        except:
            return ""

    @classmethod
    async def buscar_ocorrencias_servidor(cls, cpf, ano_final, mes_final):
        loop = asyncio.get_running_loop()
        iu, _ = await cls.identificao_unica(cpf)
        anomes = formatar_ano_mes(ano_final, mes_final)
        if iu:
            return await loop.run_in_executor(cls.executor, cls._buscar_ocorrencias_servidor_sync, iu, anomes)
        return ""


    @staticmethod
    def _consultar_beneficiario_sync(cpf):
        """Versão síncrona da consulta de beneficiário"""
        try:
            return client.service.pesquisarBeneficiarioCpf(cpf, TOKEN)
        except:
            return ""

    @classmethod
    async def consultar_beneficiario(cls, cpf):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(cls.executor, cls._consultar_beneficiario_sync, cpf)



    @staticmethod
    def _pesquisar_beneficiario_pelo_nome_sync(nome):
        """Versão síncrona da pesquisa de beneficiário pelo nome"""
        try:
            str_saida = client.service.findBeneficiadoByNome(nome, TOKEN)
            return [{"nome": item["nome"], "cpf": item["cpf"], "matricula": item["matricula"]} for item in str_saida]
        except:
            return ""

    @classmethod
    async def pesquisar_beneficiario_pelo_nome(cls, nome):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(cls.executor, cls._pesquisar_beneficiario_pelo_nome_sync, nome)



    @staticmethod
    def _consultar_beneficiario_instituidores_sync(matricula):
        """Versão síncrona da consulta de beneficiário e seus instituidores"""
        try:
            return client.service.retornarBeneficiarioInstituidores(matricula, TOKEN)
        except:
            return ""

    @classmethod
    async def consultar_beneficiario_instituidores(cls, cpf):
        loop = asyncio.get_running_loop()
        beneficiario_info = await cls.consultar_beneficiario(cpf)
        
        if beneficiario_info and 'matricula' in beneficiario_info:
            return await loop.run_in_executor(cls.executor, cls._consultar_beneficiario_instituidores_sync, beneficiario_info['matricula'])

        return ""



# class SerproSiape:

# 	@staticmethod
# 	def identificao_unica(cpf):
# 		try:
# 			str_saida = client.service.pesquisarServidorCpf(cpf,TOKEN)
# 			iu, nome = formatar_identificacao_unica(str_saida)			
# 			return iu, nome					
# 		except:			
# 			return "", "" 

# 	@classmethod
# 	def consulta_obito(self, cpf):
# 		iu, nome = SerproSiape.identificao_unica(cpf)
# 		if iu:
# 			try:
# 				str_saida=client.service.getDataObitoServidor(iu,TOKEN)		
# 				data_obito = formatar_data_obito(str_saida)
# 				return cpf, nome, data_obito
# 			except:
# 				return cpf,"",""

# 	@classmethod
# 	def extrair_ficha_financeira(self, cpf, ano_inicial, ano_final):		
# 		iu, nome = SerproSiape.identificao_unica(cpf)		
# 		if iu:
# 			try:
# 				str_saida = client.service.montarFichaFinanceiraServidor(iu, ano_inicial, ano_final,TOKEN)				
# 				return str_saida
# 			except:
# 				return ""
			
	
# 	@classmethod
# 	def buscar_ocorrencias_servidor(self, cpf, ano_final, mes_final):
# 		anomes = formatar_ano_mes(ano_final, mes_final)		
# 		iu, _ = SerproSiape.identificao_unica(cpf)		
# 		if iu:
# 			try:
# 				str_saida = client.service.getOcorrenciasServidor(iu, anomes,TOKEN)				
# 				return str_saida
# 			except:
# 				return ""
			
# 	@classmethod
# 	def consultar_beneficiario(self, cpf): #cpf beneficiario		
# 		try:
# 			str_saida = client.service.pesquisarBeneficiarioCpf(cpf,TOKEN)				
# 			return str_saida #matricula beneficiario e nome beneficiario
# 		except:
# 			return ""

# 	@classmethod
# 	def pesquisar_beneficiario_pelo_nome(self, nome):
# 		try:
# 			str_saida = client.service.findBeneficiadoByNome(nome,TOKEN)			
# 			dados = [{"nome": item["nome"], "cpf": item["cpf"], "matricula": item["matricula"]} for item in str_saida]			
# 			return dados
# 		except:
# 			return ""	
	
# 	@classmethod
# 	def consultar_beneficiario_instituidores(self, cpf): #cpf do beneficiario
# 		matricula = SerproSiape.consultar_beneficiario(cpf)['matricula']	# mat beneficiario	
# 		try:
# 			str_saida = client.service.retornarBeneficiarioInstituidores(matricula,TOKEN)				
# 			info(f'str_saida:\n{str_saida}')
# 			return str_saida 
# 			# nome,cpf,matricula beneficiario e nome,iu,matricula instituidor
# 			# cpf = '36030007068'		
# 		except:
# 			return ""
		





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