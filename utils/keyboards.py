from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
load_csv_in_database = KeyboardButton(text="Загрузить csv-файл")
delete_all_database = KeyboardButton(text="Удалить всю базу данных")
appoint_a_new_administrator = KeyboardButton(text="Назначить нового администратора")
delete_administrator = KeyboardButton(text="Удалить администратора")
edit_system_messages = KeyboardButton(text="Редактировать текстовые сообщения")
set_new_interval = KeyboardButton(text="Разослать информацию из базы данных")
delete_message = KeyboardButton(text="Удалить сообщение")
admin_keyboard.add(load_csv_in_database, delete_all_database, appoint_a_new_administrator, delete_administrator, edit_system_messages, set_new_interval, delete_message)
