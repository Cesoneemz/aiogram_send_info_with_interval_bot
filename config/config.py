from os import getenv


API_TOKEN = getenv('API_KEY')

POSTGRES_CONFIG = {
    'host': getenv('POSTGRES_HOST'),
    'user': getenv('POSTGRES_USER'),
    'password': getenv('POSTGRES_PASSWORD'),
    'database': getenv('POSTGRES_DATABASE_FOUR'),
    'port': getenv('POSTGRES_PORT')
        }

ADMIN_ID = getenv('ADMIN_IDS').split(' ') 

REDIS_CONFIG = {
        'address': getenv('REDIS_ADDRESS'),
        }
