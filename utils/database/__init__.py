import aiosqlite

from utils.database.schemas import Schema


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBConnection(metaclass=Singleton):

    _con: aiosqlite.Connection

    def __init__(self):
        pass

    async def create_db(self):
        self._con = await aiosqlite.connect(Schema.DB_PATH)
        print('Database connection established')

    async def close_db(self):
        await self._con.close()
        print('Database disconnected')

    def get_db(self):
        return self._con
