from linear_code_execution.database import DataBase
from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime


class Book(DataBase.Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    author = Column(String(20), nullable=True)
    customer = Column(String(20), nullable=True)
    title_of_book = Column(String(200), nullable=True)
    add_date = Column(DateTime, default=datetime.now)
    price = Column(Integer, nullable=True)
