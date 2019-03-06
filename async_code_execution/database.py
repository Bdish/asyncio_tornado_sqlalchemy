from config import config, logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from concurrent.futures import ThreadPoolExecutor
import asyncio


class DataBase:



    Base = declarative_base()

    def __init__(self):

        SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8mb4'.format(
            host=config.get('books_db', 'host'),
            port=config.get('books_db', 'port'),
            user=config.get('books_db', 'user'),
            passwd=config.get('books_db', 'password'),
            db=config.get('books_db', 'database'))

        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        DataBase.Base.metadata.create_all(self.engine)

    """def setup_session(self, session):
        self.session = session()
        

    async def exec(self, function, args):
        self.loop = asyncio.get_event_loop()
        return await self.loop.run_in_executor(DataBase.executor, lambda: function(**args))"""
