import asyncio 

from config.config import ADMIN_ID 

def validation_is_admin(admin_id: int):
    """
    Функция проверяет является ли пользователь админом
    """

    return True if str(admin_id) in ADMIN_ID else False


