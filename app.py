import asyncio
import aioredis

from aiogram import executor
from load_all import bot 

from config.config import ADMIN_ID, REDIS_CONFIG 
from database.database_class import db

loop = asyncio.get_event_loop()


if __name__ == '__main__':
    from handlers.admin_panel import dp 

    executor.start_polling(dp, loop=loop)
