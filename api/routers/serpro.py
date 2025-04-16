#from starlette import status
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status, Query, Body
from typing import List
from database import SessionLocal

from serprosoap import SerproSiape
from configura_debug import *
from serprotools import *
from models import *


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.get("/pesquisarcpf/{cpf}")
# async def pesquisar_cpf(cpf):
#     iu, nome = SerproSiape.identificao_unica(cpf)    
#     return {'cpf':cpf, 'nome':nome, 'iu': iu}

@router.get("/pesquisarcpf/{cpf}")
async def pesquisar_cpf(cpf):
    iu, nome = await SerproSiape.identificao_unica(cpf)
    return {'cpf': cpf, 'nome': nome, 'iu': iu}

# @router.get("/datadeobito/{cpf}")
# async def pesquisar_data_obito(cpf):
#     cpf, nome, data_de_obito = SerproSiape.consulta_obito(cpf)    
#     return {'cpf':cpf, 'nome':nome, 'data_de_obito': data_de_obito}


@router.get("/datadeobito/{cpf}")
async def pesquisar_data_obito(cpf):
    cpf, nome, data_de_obito = await SerproSiape.consulta_obito(cpf)
    return {'cpf': cpf, 'nome': nome, 'data_de_obito': data_de_obito}


@router.get("/vinculos/{cpf}")
async def pesquisar_orgaos_pelo_cpf(
    cpf, 
    anoinicial: int = Query(..., title="Ano inicial", gt=1980, lt=2100),
    anofinal: int = Query(..., title="Ano inicial", gt=1980, lt=2100)):    
    ficha = await SerproSiape.extrair_ficha_financeira(cpf, anoinicial, anofinal)
    orgaos = obter_orgaos_por_periodo(ficha)
    return orgaos


@router.get("/fichafinanceira/{cpf}")
async def pesquisar_ficha_financeira(
    cpf: str,
    anoinicial: int = Query(..., title="Ano inicial", gt=1980, lt=2100),
    anofinal: int = Query(..., title="Ano inicial", gt=1980, lt=2100)):       
    ficha = await SerproSiape.extrair_ficha_financeira(cpf, anoinicial, anofinal)
    return ficha


@router.get("/rubricas/{cpf}")
async def extrair_todas_rubricas_ficha_financeira(cpf: str,
                            anoinicial: int,
                            anofinal: int):    
    ficha = await SerproSiape.extrair_ficha_financeira(cpf, anoinicial, anofinal)
    if ficha:
        rubrica = ExtracaoRubricas(ficha)
        dicionario = rubrica.percorrer_ficha_financeira()
        return dicionario    
    return ''

@router.get("/rubricas/{cpf}/{orgao}")
async def extrair_todas_rubricas_ficha_financeira_por_orgao(cpf: str,
                            anoinicial: int,
                            anofinal: int,
                            orgao: int):    
    ficha = await SerproSiape.extrair_ficha_financeira(cpf, anoinicial, anofinal)    
    if ficha:
        rubrica = ExtracaoRubricas(ficha)
        dicionario = rubrica.separar_rubricas_por_orgao(orgao)        
        return dicionario    
    return ''


@router.get("/ocorreciasservidor/{cpf}")
async def obter_ocorrencias_servidor(cpf: str, anofinal: int, mesfinal: int):
    ficha = await SerproSiape.buscar_ocorrencias_servidor(cpf, anofinal, mesfinal)
    return ficha


@router.get("/pesquisarservidor/{nome}")
async def pesquisar_servidor_pelo_nome(nome: str):
    nome = await SerproSiape.pesquisar_servidor_pelo_nome(nome)
    if nome:
        return nome    
    return ''


@router.get("/pesquisarbeneficiario/{nome}")
async def pesquisar_beneficiario_pelo_nome(nome: str):
    nome = await SerproSiape.pesquisar_beneficiario_pelo_nome(nome)
    if nome:
        return nome    
    return ''


@router.get("/consultarinstituidores/{cpf}")
async def pesquisar_instituidores_pelo_cpf_beneficiario(cpf: str):
    nome = await SerproSiape.consultar_beneficiario_instituidores(cpf)
    if nome:
        return nome    
    return ''

@router.get("/consultarbeneficiario/{cpf}")
async def consultar_beneficiario_pelo_cpf(cpf: str):
    nome = await SerproSiape.consultar_beneficiario(cpf)
    if nome:
        return nome    
    return ''

# -------------------------------------------------------------
# a partir daqui a API busca os dados no próprio banco postgres
# -------------------------------------------------------------

@router.get("/descricaorubrica")
async def listar_todas_descricoes_rubricas(db: Session = Depends(get_db)):
    data_tabela = db.query(Rubricas).all()
    if data_tabela is not None:
        return data_tabela
    raise HTTPException(status_code=404, detail='N/I')


@router.get("/descricaorubrica/")
async def obter_descricao_rubrica_pelo_codigo(codigo,
                                              db: Session = Depends(get_db)):
    data_tabela = db.query(Rubricas).filter(Rubricas.codigo == codigo).first()    
    if data_tabela is not None:
        return data_tabela
    else:
        return {'descricao':'', 'codigo':codigo}


@router.get("/itens/")
async def get_itens(rubricas: List[int] = Query(...)):    
    return rubricas


@router.get("/nomeorgao/")
async def obter_nome_orgao_pelo_codigo(codigo,
                                       db: Session = Depends(get_db)):
    data_tabela = db.query(OrgaoSiape).filter(OrgaoSiape.codigo == codigo).first()
    if data_tabela is not None:
        return data_tabela
    else:
        return {'nome':'', 'codigo':codigo}
    #raise HTTPException(status_code=404, detail='nome não encontrado')


@router.get("/cargoemprego/")
async def obter_nome_cargo(codcargo,
                           codgrupo,
                           db: Session = Depends(get_db)):
    data_tabela = db.query(CargoEmprego).filter(CargoEmprego.codigo == codcargo, CargoEmprego.grupo == codgrupo).first()
    if data_tabela is not None:
        return data_tabela
    raise HTTPException(status_code=404, detail='sem dados')