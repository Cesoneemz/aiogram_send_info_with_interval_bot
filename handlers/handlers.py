from aiogram import types
from aiogram.dispatcher import FSMContext

import aioredis 
import asyncio

from config.config import REDIS_CONFIG 
from load_all import dp, bot 
from database.database_class import db 

@dp.channel_post_handler(lambda message: message.text == 'Активировать бота')
async def send_welcome(message: types.Message):
    if await db.get_member_by_member_id(member_id=message.chat.id) is None:
        await db.add_new_member(member_id=message.chat.id)
        await message.answer(await db.get_message_by_id(message_id=1))
        await message.answer(await db.get_message_by_id(message_id=2))
    else:
        await message.answer(await db.get_message_by_id(message_id=3))


@dp.message_handler(lambda message: message.text == 'Активировать бота' and not message.chat.title is None and message.chat.type == "supergroup")
async def activate_bot_in_chat(message: types.Message):
    if await db.get_member_by_member_id(member_id=message.chat.id) is None:
        await db.add_new_member(member_id=message.chat.id)
        await message.answer(await db.get_message_by_id(message_id=1))
        await message.answer(await db.get_message_by_id(message_id=2))
    else:
        await message.answer(await db.get_message_by_id(message_id=3))
