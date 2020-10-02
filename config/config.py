from dotenv import load_dotenv
from pathlib import PurePath
from os import getenv

env_path = PurePath('env', '.env')
load_dotenv(dotenv_path=env_path)

API_TOKEN = getenv('API_KEY')

POSTGRES_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'Cesoneemz19',
    'database': 'aiogram_info_send',
    'port': getenv('POSTGRES_PORT')
        }

ADMIN_ID = ['434903526'] 

REDIS_CONFIG = {
        'address': 'redis://localhost',
        }
