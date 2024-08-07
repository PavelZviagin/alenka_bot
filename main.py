import logging
import re
import uuid
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, ContentType
from aiogram.utils import executor
import asyncpg
import asyncio

API_TOKEN = '7419786460:AAGfm9c6UTMq7UIllikhbUQxg0vfGjD-5dU'
ADMIN_ID = 700796749
DB_HOST = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'postgres'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Регулярное выражение для поиска ссылок
URL_REGEX = re.compile(
    r"(https?://[^\s]+)|(www\.[^\s]+)"
)

SPAM_KW = [
    'Эксклюзивное предложение',
    'Без опыта ',
    'дополнительный доход',
    'Зарабатывайте',
    'Доход',
    'дополнительный доход',
    'мгновенный доход',
    'Легкий заработок',
    'Бизнес на дому',
    'работа на дому',
    'Без затрат',
    'Криптовалюта',
    'Пассивный доход',
    'Срочное предложение ',
    'Ставки',
    'Без затрат',
    'Казино',
    'Распродажа',
    'Супер акция',
    'Розыгрыш',
    'Не упусти шанс',
]


# Функция для подключения к базе данных
async def create_db_pool():
    return await asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST
    )


# Подключение к базе данных
async def on_startup(dispatcher):
    dispatcher['db'] = await create_db_pool()
    print('Bot Started')


@dp.message_handler(content_types=ContentType.NEW_CHAT_MEMBERS)
async def on_user_join(message: types.Message):
    try:
        logging.warning(f'User {message.from_user.id} joined chat {message.chat.id}')
        await message.delete()
    except Exception as e:
        logging.error(f"Failed to delete message: {e}")


@dp.message_handler(content_types=ContentType.LEFT_CHAT_MEMBER)
async def on_user_join(message: types.Message):
    try:
        logging.warning(f'User {message.from_user.id} joined chat {message.chat.id}')
        await message.delete()
    except Exception as e:
        logging.error(f"Failed to delete message: {e}")


# Функция для сохранения сообщения в базу данных
async def save_message(db_pool, user_id):
    async with db_pool.acquire() as connection:
        try:
            await connection.execute(
                'INSERT INTO users_chatmessage (id, created_at, user_id) VALUES ($1, $2, $3)',
                uuid.uuid4(),
                datetime.datetime.now(),
                user_id
            )
        except Exception as e:
            logging.error(e)


async def get_user(db_pool, user_id):
    async with db_pool.acquire() as connection:
        try:
            user = await connection.fetchrow('SELECT * FROM users_chatuser WHERE user_id = $1', user_id)

            if not user:
                return None

            return user
        except Exception as e:
            logging.error(e)
            return None


async def create_user(db_pool, username, user_id, fn, ln):
    async with db_pool.acquire() as connection:
        try:
            await connection.execute(
                'INSERT INTO users_chatuser (id, username, first_name, last_name, user_id, created_at) VALUES ($1, $2, $3, $4, $5, $6)',
                uuid.uuid4(),
                username,
                fn,
                ln,
                user_id,
                datetime.datetime.now()
            )
        except Exception as e:
            logging.error(e)


def check_is_admin(message: types.Message):
    return message.from_user.id == ADMIN_ID


async def check_for_spam_keywords(message: types.Message):
    # Проверка наличия ключевых слов в сообщении
    if any(keyword.lower() in message.text.lower() for keyword in SPAM_KW):
        await message.delete()

# Обработчик всех текстовых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text_message(message: types.Message):
    db_pool = dp['db']
    user = await get_user(db_pool, message.from_user.id)
    if not user:
        await create_user(db_pool, message.from_user.username, message.from_user.id, message.from_user.first_name,
                          message.from_user.last_name)
    user = await get_user(db_pool, message.from_user.id)

    if not user:
        logging.warning(f"User not found: {message.from_user.id}")
        return

    await save_message(db_pool, user['id'])

    if not check_is_admin(message):
        await check_for_spam_keywords(message)
        if URL_REGEX.search(message.text) and not check_is_admin(message):
            await message.delete()


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, on_startup=on_startup)
