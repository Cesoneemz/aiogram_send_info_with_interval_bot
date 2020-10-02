import aioredis
import asyncio

from database.database_class import db 
from config.config import REDIS_CONFIG, ADMIN_ID  
import exceptions
from load_all import bot

def _unpack_rows(*row) -> list:
    """
    Функция распаковывает словари в список, удобный для работы
    """
    params_names = []
    for param in row:
        params_names.append(param.get('message'))
      
    return params_names
          
async def send_info_callback():
    """
    Рассылка информации из базы данных с заданным интервалом и лимитом строк
    """
    msg = ""
    all_params_names = await db.get_all_params_names()
    values = [dict(record) for record in all_params_names]
          
    redis = await aioredis.create_redis_pool(**REDIS_CONFIG)
    interval = int(await redis.get('interval_to_send_info'))
    limit = int(await redis.get('limit_query'))
    redis.close()
    await redis.wait_closed()             
    param1, param2, param3, param4, param5, param6, param7, param8 = _unpack_rows(*values)
          
    all_params = [dict(record) for record in await db.get_all_params(limit=limit)]
    for info in all_params:
        msg = f"{param1}: {info.get('row')[0]}\n{param2}: {info.get('row')[1]}\n{param3}: {info.get('row')[2]}\n{param4}: {info.get('row'    )[3]}\n{param5}: {info.get('row')[4]}\n{param6}: {info.get('row')[5]}\n{param7}: {info.get('row')[6]}\n{param8}: {info.get('row')[7]}\n\n"       
        await asyncio.sleep(interval)
      
        for member in await db.get_all_members():
            try:
                message = await bot.send_message(member.get('member_id'), text=msg)
                title = message.chat.title if not message.chat.title is None else ''
                await db.add_to_database_message_info(message_id=message.message_id, title=title, chat_id=message.chat.id, message=message.text)
                await asyncio.sleep(0.3)
            except exceptions.exceptions.NotValidMemberId:
                pass

