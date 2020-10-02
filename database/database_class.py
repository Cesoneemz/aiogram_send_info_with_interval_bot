import asyncpg
import asyncio

from config.config import POSTGRES_CONFIG

class DatabaseAPI(object):

    @classmethod
    async def connect_to_database(cls):
        """
        Создаем подключение к базе данных
        """
        self = DatabaseAPI()
        self.pool = await asyncpg.create_pool(**POSTGRES_CONFIG)

        return self

    def connect(func):
        """
        Декоратор для осуществления запросов в базу данных
        """
        async def decorator(self, *args, **kwargs):
            async with self.pool.acquire() as connect:
                async with connect.transaction():
                    return await func(self, connect=connect, *args, **kwargs)

        return decorator


    @connect 
    async def load_info_from_csv_to_database(self, connect, param1, param2, param3, param4, param5, param6, param7, param8):
        """
        Загрузить данные из csv-файла в базу данных
        """
        return await connect.execute('INSERT INTO info(param1, param2, param3, param4, param5, param6, param7, param8) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)', param1, param2, param3, param4, param5, param6, param7, param8)


    @connect 
    async def clear_all_database(self, connect):
        """
        Полностью очистить базу данных
        """
        return await connect.execute('DELETE FROM info')


    @connect
    async def get_all_messages_with_id(self, connect):
        """
        Получить все сообщения с их id
        """
        return await connect.fetch('SELECT * FROM messages')

    @connect
    async def set_new_message(self, connect, id: int, message: str):
        """
        Изменить сообщение в базе данных
        """
        return await connect.execute('UPDATE messages SET message = $1 WHERE id = $2', message, id)

    @connect
    async def get_message_by_id(self, connect, message_id: int):
        """
        Получить сообщение по его ID в базе данных
        """
        return await connect.fetchval('''SELECT message FROM messages WHERE id = $1''', message_id)

    @connect 
    async def get_all_params(self, connect, limit: int):
        """
        Получить всю информацию из базы данных
        """
        return await connect.fetch('SELECT (param1, param2, param3, param4, param5, param6, param7, param8) FROM info ORDER BY random() LIMIT $1', limit)
    
    @connect
    async def get_all_members(self, connect):
        """
        Получить всех пользователей бота
        """
        return await connect.fetch('SELECT (member_id) FROM members')

    @connect 
    async def add_new_member(self, connect, member_id: int):
        """
        Добавить нового пользователя бота
        """
        return await connect.execute('INSERT INTO members (member_id) VALUES ($1)', member_id)

    @connect 
    async def get_member_by_member_id(self, connect, member_id: int):
        """
        Проверка существования пользователя
        """
        return await connect.fetchval('SELECT * FROM members WHERE member_id = $1', member_id)

    @connect
    async def get_all_params_names(self, connect):
        """
        Получить все имена параметров
        """
        return await connect.fetch('SELECT (message) FROM messages ORDER BY id LIMIT 8 OFFSET 3')

    @connect 
    async def add_to_database_message_info(self, connect, message_id: int, title: str, chat_id: int, message: str):
        """
        Добавить в базу данных информацию о сообщении для последюущего удаления
        """
        return await connect.execute('INSERT INTO mailing_messages (message_id, title, chat_id, message) VALUES ($1, $2, $3, $4)', message_id, title, chat_id, message)

    @connect 
    async def get_all_mailing_messages(self, connect):
        """
        Получить все отправленные сообщения
        """
        return await connect.fetch('SELECT * FROM mailing_messages')


    @connect 
    async def get_messages_id_by_database_id(self, connect, id: int):
        """
        Получить конкретный id сообщения по его id в базе данных
        """
        return await connect.fetchval('SELECT (message_id, chat_id) FROM mailing_messages WHERE id = $1', id)

    @connect 
    async def delete_message_info_from_database(self, connect, id: int):
        """
        Удалить сообщение из базы данных
        """
        return await connect.execute('DELETE FROM mailing_messages WHERE id = $1', id)

loop = asyncio.get_event_loop() 
db = loop.run_until_complete(DatabaseAPI.connect_to_database())
