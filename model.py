from typing import Optional

from pydantic import BaseModel
from mongoengine import Document, StringField, IntField, EmailField, FloatField


class newBook(BaseModel):
    title: str
    author: str
    year: int
    book_id: int
    price: str
    quantity: int

class Books(Document):
    title = StringField()
    author = StringField()
    year = IntField()
    book_id = IntField()
    price = FloatField()
    quantity = IntField()

class User(Document):
    username = StringField()
    password = StringField()
    email = EmailField()

class newUser(BaseModel):
    username: str
    password: str
    email: str

"""class UpdateBook(Document):
    title = Optional[str] = None
    author = Optional[str] = None
    year = Optional[int] = None
    book_id = Optional[int] = None"""