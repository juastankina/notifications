from peewee_aio import Manager

from config import settings

db = Manager(settings.db_url)


async def get_db():
    try:
        await db.connect()
        yield
    finally:
        if db.is_connected:
            await db.disconnect()
