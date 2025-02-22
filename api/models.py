# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, Numeric, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CargoEmprego(Base):
    __tablename__ = 'cargoemprego'

    #id = Column(BigInteger, primary_key=True)    
    codigo = Column(String(10))
    grupo = Column(String(10))
    nome = Column(String(200),primary_key=True)
    nivel = Column(String(10))


class Rubricas(Base):
    __tablename__ = 'rubricas'

    #id = Column(BigInteger, primary_key=True)
    codigo = Column(String(10), primary_key=True)
    descricao = Column(String(200))


class OrgaoSiape(Base):
    __tablename__ = 'orgaosiape'

    #id = Column(BigInteger, primary_key=True)
    codigo = Column(String(10), primary_key=True)
    nome = Column(String(200)) 