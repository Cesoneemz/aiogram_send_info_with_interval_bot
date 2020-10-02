import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
import aioredis

from config.config import POSTGRES_CONFIG, REDIS_CONFIG
from database.database_class import db
import exceptions
from load_all import dp, bot
from utils.keyboards import admin_keyboard as ak 
from utils.validators import validation_is_admin
from utils.utils import send_info_callback
from states.states import WaitForCsvWithInfo, AddAdmin, DeleteAdmin, EditSystemMessages, SetIntervalToSendInfo, DeleteMessageFromAnyway 


@dp.message_handler(lambda message: validation_is_admin(message.from_user.id), commands=['admin']) 
async def send_admin_keyboard(message: types.Message):
    await message.answer('Присылаю админскую клавиатуру', parse_mode='HTML', reply_markup=ak)


@dp.message_handler(lambda message: validation_is_admin(message.from_user.id) and message.text == "Загрузить csv-файл")
async def load_csv_to_database_part1(message: types.Message):
   await message.answer('Пожалуйста, пришлите csv-файл, размером не более 20МБ', parse_mode='HTML') 
   await WaitForCsvWithInfo.wait_for_csv_file.set()


@dp.message_handler(lambda message: validation_is_admin(message.from_user.id), content_types=types.ContentType.DOCUMENT, state=WaitForCsvWithInfo.wait_for_csv_file)
async def load_csv_to_database_part2(message: types.Message, state: FSMContext):
    import os, csv, psycopg2

    file_id = message.document.file_id
    filename = message.document.file_name
    file = await bot.get_file(file_id=file_id)
    file_path = file.file_path

    destination = os.path.join(os.getcwd(), 'csv', filename)

    await bot.download_file(file_path=file_path, destination=destination)

    await message.answer("Файл был успешно загружен, начинаю парсинг...")

    connect = psycopg2.connect(**POSTGRES_CONFIG)
    connect.autocommit = True
    cursor = connect.cursor()

    error_numbers = {}

    with open(destination, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        await db.clear_all_database()
        for row in reader:
            print(row)
            if len(row) == 1:
                split_row = row[0].split(';')
            else:
                split_row = row 

            await db.load_info_from_csv_to_database(param1=row[0], param2=row[1], param3=row[2], param4=row[3], param5=row[4], param6=row[5], param7=row[6], param8=row[7])

    connect.commit()

    os.remove(destination)

    await state.finish()

    await message.answer("Файл был успешно загружен", parse_mode='HTML')


@dp.message_handler(lambda message: validation_is_admin(message.from_user.id) and message.text == 'Назначить нового администратора')
async def add_admin_part_1(message: types.Message):
    await message.answer("Пожалуйста, введите ID нового админа")

    await AddAdmin.wait_for_admin_id.set()


@dp.message_handler(lambda message: validation_is_admin(message.from_user.id), state=AddAdmin.wait_for_admin_id)
async def add_admin_part2(message: types.Message, state: FSMContext):
    if message.text not in ADMIN_ID:
        ADMIN_ID.append(message.text)
    await message.answer(f"ID {message.text} был добавлен к списку админов")

    await state.finish()


@dp.message_handler(
    lambda message: validation_is_admin(message.from_user.id) and message.text == 'Удалить администратора')
async def add_admin_part_1(message: types.Message):
    await message.answer("Пожалуйста, введите ID админа, которого нужно удалить")

    await DeleteAdmin.wait_for_admin_id_delete.set()


@dp.message_handler(lambda message: validation_is_admin(message.from_user.id),
                    state=DeleteAdmin.wait_for_admin_id_delete)
async def add_admin_part2(message: types.Message, state: FSMContext):
    if message.text in ADMIN_ID:
        ADMIN_ID.remove(message.text)
        await message.answer(f"Админ с ID {message.text} был удалён")
    else:
        await message.answer('Такого админа нет')

    await state.finish()


@dp.message_handler(
    lambda message: validation_is_admin(message.from_user.id) and message.text == 'Редактировать текстовые сообщения')
async def edit_system_messages_id(message: types.Message):
    messages = await db.get_all_messages_with_id()
    msg = ''
    for i in messages:
        msg += f'ID: {i[0]}   Сообщение: {i[1]}\n\n'
    await message.answer(msg)
    await message.answer("Выберите сообщение, которое вы хотите редактировать.")
    await EditSystemMessages.wait_for_id.set()


@dp.message_handler(lambda message: validation_is_admin(message.from_user.id), state=EditSystemMessages.wait_for_id)
async def edit_system_message(message: types.Message, state: FSMContext):
    await state.update_data(id=int(message.text))
    await message.answer("Введите новое сообщение")

    await EditSystemMessages.wait_for_new_message.set()


@dp.message_handler(lambda message: validation_is_admin(message.from_user.id),
                    state=EditSystemMessages.wait_for_new_message)
async def set_new_system_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id = data.get('id')

    try:
        await db.set_new_message(id=id, message=message.text)

        await message.answer("Сообщение успешно изменено!")

        await state.finish()

    except exceptions.exceptions.NotValidIdForEditMessage:

        await message.answer("Ошибка")
        await state.finish()

@dp.message_handler(lambda message: validation_is_admin(message.from_user.id) and message.text == "Разослать информацию из базы данных")
async def send_info_from_database(message: types.Message):
    await message.answer("Пожалуйста, введите время, в секундах, через которое нужно отправить информацию")

    await SetIntervalToSendInfo.wait_for_interval_in_seconds.set()

@dp.message_handler(lambda message: validation_is_admin(message.from_user.id), state=SetIntervalToSendInfo.wait_for_interval_in_seconds)
async def set_row_limit(message: types.Message, state: FSMContext):
    redis = await aioredis.create_redis_pool(**REDIS_CONFIG)
    await redis.set('interval_to_send_info', str(message.text)) 
    redis.close()
    await redis.wait_closed()

    await message.answer('Пожалуйста, введите лимит строк.')
 
    await SetIntervalToSendInfo.wait_for_limit_query.set()

@dp.message_handler(lambda message: validation_is_admin(message.from_user.id), state=SetIntervalToSendInfo.wait_for_limit_query)
async def send_info_from_database_with_interval(message: types.Message, state: FSMContext):
    from app import loop 
    try:
        redis = await aioredis.create_redis_pool(**REDIS_CONFIG)
        await redis.set('limit_query', str(message.text))
        loop.call_later(int(await redis.get('interval_to_send_info')), asyncio.create_task, await send_info_callback())
        redis.close()
        await redis.wait_closed()
        await state.finish()
    except exceptions.exceptions.NotValidInterval:
        await message.answer('Неверный интервал')
        await state.finish()


@dp.message_handler(lambda message: validation_is_admin(message.from_user.id) and message.text == 'Удалить сообщение')
async def send_messages_info(message: types.Message):
    msg = 'ID     MESSAGE_ID   CHANNEL/CHAT TITLE   MESSAGE\n\n'
    for m in await db.get_all_mailing_messages():
        msg += f"{m.get('id')}     {m.get('message_id')}    {m.get('title')}     {m.get('message').replace('chr(10)', '')}\n\n"

    if not await db.get_all_mailing_messages() is None:
        await message.answer(msg)
        await message.answer('Пожалуйста, введите ID сообщения, которое нужно удалить')
        await DeleteMessageFromAnyway.wait_for_id.set()
    else:
        await message.answer('На данный момент сообщений для удаления нет')

@dp.message_handler(lambda message: validation_is_admin(message.from_user.id), state=DeleteMessageFromAnyway.wait_for_id)
async def delete_message(message: types.Message, state: FSMContext):
    try:
        message_id, chat_id = await db.get_messages_id_by_database_id(id=int(message.text))
        await bot.delete_message(chat_id, message_id)
        await db.delete_message_info_from_database(id=int(message.text))
        await message.answer('Сообщение было удалено')
        await state.finish()
    except exceptions.exceptions.NotValidIdForMessage:
        await message.answer('Неверный ID')
        await state.finish()

