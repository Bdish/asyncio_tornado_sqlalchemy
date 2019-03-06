from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient
import tornado as tornado
from tornado.escape import json_decode
from tornado.platform.asyncio import AsyncIOMainLoop
from config import logging
from linear_code_execution.database import DataBase
from linear_code_execution.book import Book
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from config import config
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import asyncio

import json


class AddBook(RequestHandler):

    async def post(self):
        logging.critical("0")
        try:
            self.set_status(200)
            # logging.critical("request.url: " + self.request.uri)
            # logging.critical("request.text: " + self.request.body.decode('utf-8'))
            data = json_decode(self.request.body)

            book = Book()
            book.author = data["author"]
            book.title_of_book = data["title"]

            book = await self._get_customer_and_price(book)
            self.loop = asyncio.get_event_loop()
            book = await self.loop.run_in_executor(self.application.executor, partial(self._add_book_to_db, book))
            await self._send_book_to_view(book)
            self.write(book.title_of_book)
        except Exception as e:
            logging.critical("AddBook: " + str(e))
            self.set_status(500)
            self.write("Error on the book server")

    async def _get_customer_and_price(self, book: Book) -> Book:
        try:
            logging.critical("1")
            url = config.get('request_info_about_customer', 'base_url')
            http_client = AsyncHTTPClient()
            res = await http_client.fetch(url)
            if res.code != 200:
                self.set_status(500)
                self.write("Customer information not received")
            # logging.critical("res.text: " + res.text)
            dict_res = json.loads(res.body)
            book.customer = dict_res['customer']
            book.price = dict_res['price']
        except Exception as e:
            logging.critical("_get_customer_and_price: " + str(e))
            self.set_status(500)
            self.write("Error processing information about the customer and price")
        return book

    async def _send_book_to_view(self, book: Book):
        logging.critical("3")
        try:
            url = config.get('request_info_about_customer', 'base_url')
            http_client = AsyncHTTPClient()
            res = await  http_client.fetch(url)
            http_client.fetch(url)
            if res.code != 200:
                self.set_status(500)
                self.write("Customer information not received")
            # logging.critical("res.text: " + res.text)
            dict_res = json.loads(res.body)
            book.customer = dict_res['customer']
            book.price = dict_res['price']
        except Exception as e:
            logging.critical("__send_book_to_view: " + str(e))
            self.set_status(500)
            self.write("Error send book to view")

    def _add_book_to_db(self, book: Book) -> Book:
        logging.critical("2")
        db = DataBase()
        session = Session(db.engine)
        try:
            session.add(book)
            session.commit()
            session.refresh(book)
        except SQLAlchemyError:
            logging.debug("Error in _add_book_to_db: {error}".format(error=str(SQLAlchemyError)))
            self.set_status(500)
        finally:
            session.close()
        return book


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": ""}),
            (r'/', AddBook),
        ]
        settings = {
        }
        super(Application, self).__init__(handlers, **settings)


async def make_app():
    app = Application()
    app.listen(config.get("controllers", "port"), config.get("controllers", "host"))
    app.executor = ThreadPoolExecutor(max_workers=1)


if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_app())
    loop.run_forever()
