from decouple import config, Csv

SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DB_URL')
TOKEN = config('TOKEN')
WSDL = config('WSDL')

NOREGS='Não há registro'