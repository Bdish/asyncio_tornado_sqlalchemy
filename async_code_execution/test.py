import json
from tornado.web import Application
from ddt import ddt, data, unpack
from linear_code_execution.app import AddBook
from unittest.mock import MagicMock
from linear_code_execution.book import Book
from datetime import datetime
from tornado.testing import AsyncHTTPTestCase


class TestAddBook(AsyncHTTPTestCase):
    def get_app(self):
        urls = [
            (r'/', AddBook)
        ]
        return Application(urls, http_client=self.http_client)

    def tearDown(self):
        pass

    def test_add_book(self):
        """LogOut._identification_update = MagicMock()
        LogOut._identification_update.return_value = result_update"""

        headers = None
        body = {
            "author": "Tom",
            "title": "New book"
        }
        json_body = json.dumps(body)
        book = Book()
        book.id = 1
        book.author = "sdfsdf"
        book.title_of_book = "sdfgdfg"
        book.customer = "gdfgffddf"
        book.price = 100
        book.add_date = datetime.now()

        AddBook._add_book_to_db = MagicMock()
        AddBook._add_book_to_db.return_value = book

        res = self.fetch('/', method='POST', body=json_body, headers=headers)

        self.assertEqual(res.code, 200)
        self.assertEqual(res.body.decode('utf-8'), "sdfgdfg")