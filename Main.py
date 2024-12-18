from typing import Optional
from fastapi import FastAPI, HTTPException, Path, Query, Depends
from mongoengine import connect
from mongoengine.queryset.visitor import Q
from model import newBook, Books, newUser, User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from jose import jwt
from mailjet_rest import Client
import json, os

connect(db="bms", host="localhost", port=27017)

api_key = 'XXXXXX'
api_secret = 'XXXXXX'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

app = FastAPI()

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "6f17318d568fea048d3f455a899c467f"
ALGORITHM = "HS256"


@app.get("/get_all_books")
async def get_all_books():
    book = json.loads(Books.objects().to_json())
    return {"books": book}


@app.get("/get_book/{book_id}")
async def get_book(book_id: int = Path(..., gt=0)):
    book = json.loads(Books.objects.get(book_id=book_id).to_json())
    return book


@app.get("/search_book")
async def search_book(title: Optional[str] = None, year: int = Query(None,gt=0)):
    return searchBook(title, year)


@app.delete("/delete_book/{book_id}")
async def delete_book(book_id: int = Path(..., gt=0), token: str = Depends(Oauth2_scheme)):
    book = Books.objects.filter(Q(book_id=book_id))
    book.delete()

    return {"Books": "deleted"}


@app.put("/update_books")
async def update_book(bookid: int = Query(None, gt=0), title: Optional[str] = None, author: Optional[str] = None,
                      year: int = Query(None,gt=0), quantity: int = Query(None, gt=0), price: float = Query(None, gt=0),
                      token: str = Depends(Oauth2_scheme)):

    if bookid:
        if title:
            if author:
                if year:
                    if price:
                        Books.objects(book_id=bookid).update(title=title, author=author, year=year, price=price)
                        return {"Message": "Title, Author, Year and Price Updated!"}
                    if quantity:
                        if price:
                            Books.objects(book_id=bookid).update(title=title, author=author, year=year,
                                                                 quantity=quantity, price=price)
                            return {"Message": "Title, Author, Year, Quantity and Price Updated!"}
                        Books.objects(book_id=bookid).update(title=title, author=author, year=year,quantity=quantity)
                        return {"Message": "Title, Author, Year and Quantity Updated!"}
                    Books.objects(book_id=bookid).update(title=title, author=author, year=year)
                    return {"Message": "Title, Author and Year Updated!"}
                if quantity:
                    if price:
                        Books.objects(book_id=bookid).update(title=title, quantity=quantity, price=price, author=author)
                        return {"Message": "Title, Author, Quantity and Price Updated!"}
                    Books.objects(book_id=bookid).update(title=title, author=author, quantity=quantity)
                    return {"Message": "Title, Author and Quantity Updated!"}
                if price:
                    Books.objects(book_id=bookid).update(title=title, author=author, price=price)
                    return {"Message": "Title, Author and Price Updated!"}
                Books.objects(book_id=bookid).update(title=title, author=author)
                return {"Message": "Title and Author Updated!"}
            if year:
                if quantity:
                    if price:
                        Books.objects(book_id=bookid).update(title=title, year=year, quantity=quantity,price=price)
                        return {"Message": "Title, Year, Quantity and Price Updated!"}
                    Books.objects(book_id=bookid).update(title=title, year=year, quantity=quantity)
                    return {"Message": "Title, Year and Quantity Updated!"}
                if price:
                    Books.objects(book_id=bookid).update(title=title, year=year, price=price)
                    return {"Message": "Title, Year and Price Updated!"}
                Books.objects(book_id=bookid).update(title=title,year=year)
                return {"Message": "Title and Year Updated!"}
            if quantity:
                if price:
                    Books.objects(book_id=bookid).update(title=title, quantity=quantity, price=price)
                    return {"Message": "Title, Quantity and Price Updated!"}
                Books.objects(book_id=bookid).update(title=title,quantity=quantity)
                return {"Message": "Title and Quantity Updated!"}
            if price:
                Books.objects(book_id=bookid).update(title=title,price=price)
                return {"Message": "Title and Price Updated!"}
            Books.objects(book_id=bookid).update(title=title)
            return {"Message": "Title Updated!"}
        if author:
            if year:
                if quantity:
                    if price:
                        Books.objects(book_id=bookid).update(author=author, year=year, quantity=quantity, price=price)
                        return {"Message": "Author, Year, Quantity and Price Updated!"}
                    Books.objects(book_id=bookid).update(author=author, year=year, quantity=quantity)
                    return {"Message": "Author, Year and Quantity Updated!"}
                if price:
                    Books.objects(book_id=bookid).update(author=author, year=year, price=price)
                    return {"Message": "Author, Year and Price Updated!"}
                Books.objects(book_id=bookid).update(author=author,year=year)
                return {"Message": "Author and Year Updated!"}
            if quantity:
                Books.objects(book_id=bookid).update(author=author,quantity=quantity)
                return {"Message": "Author and Quantity Updated!"}
            if price:
                Books.objects(book_id=bookid).update(author=author,price=price)
                return {"Message": "Author and Price Updated!"}
            Books.objects(book_id=bookid).update(author=author)
            return {"Message": "Author Updated!"}
        if year:
            if quantity:
                if price:
                    Books.objects(book_id=bookid).update(year=year, quantity=quantity,price=price)
                    return {"Message": "Year, Quantity and Price Updated!"}
                Books.objects(book_id=bookid).update(year=year,quantity=quantity)
                return {"Message": "Year and Quantity Updated!"}
            if price:
                Books.objects(book_id=bookid).update(year=year, price=price)
                return {"Message": "Year and Price Updated!"}
            Books.objects(book_id=bookid).update(year=year)
            return {"Message": "Year Updated!"}
        if quantity:
            if price:
                Books.objects(book_id=bookid).update(quantity=quantity,price=price)
                return {"Message": "Quantity and Price Updated!"}
            Books.objects(book_id=bookid).update(quantity=quantity)
            return {"Message": "Quantity Updated!"}
        if price:
            Books.objects(book_id=bookid).update(price=price)
            return {"Message": "Price Updated!"}
        return {"Message": "Please fill in some fields"}
    else:
        raise HTTPException(status_code=400, detail="Please enter a book id")


def searchBook(title: Optional[str] = None, year: int = Query(None,gt=0)):
    if title:
        if year:
            book = json.loads(Books.objects.filter(Q(title__icontains=title) & Q(year=year)).to_json())
            return {"Books": book}

    if title:
        book = json.loads(Books.objects.filter(Q(title__icontains=title)).to_json())
        return {"Books": book}

    if year:
        book = json.loads(Books.objects.filter(Q(year=year)).to_json())
        return {"Books": book}


@app.get("/search_author")
async def search_author(author: str):
    auth = json.loads(Books.objects.filter(author__icontains=author).to_json())
    return {"author": auth}


@app.post("/add_new_book")
async def add_new_book(book: newBook, token: str = Depends(Oauth2_scheme)):
    new_book = Books(title=book.title, author=book.author, year=book.year, book_id=book.book_id, price=book.price,
                     quantity=book.quantity)
    if Books.objects(book_id=book.book_id):
        raise HTTPException(status_code=400, detail="ID already exists")
    else:
        new_book.save()

    return {"Message": "Book Added!"}


pwd_cont = CryptContext(schemes=["bcrypt"], deprecated="auto")


def passwordHash(password):
    return pwd_cont.hash(password)


@app.post("/signup")
async def signup(newuser: newUser):
    user = User(username=newuser.username, password=passwordHash(newuser.password), email=newuser.email)
    user.save()
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "email@email.com",
                    "Name": "BookTraders"
                },
                "To": [
                    {
                        # "Email": "email@email.com",
                        # "Name": "John Doe"
                        "Email": newuser.email,
                        "Name": newuser.username
                    }
                ],
                "Subject": "Greetings from BookTraders.",
                "TextPart": "Welcome to BookTraders",
                "HTMLPart": "<h3>Dear " + newuser.username + ", welcome to BookTraders!",
                # "HTMLPart": "<h3>Dear John Doe, welcome to BookTraders!",
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())

    return {"message": "Please check your email"}


def authenticateUser(username, password):
    try:
        user = json.loads(User.objects.get(username=username).to_json())
        password_check = pwd_cont.verify(password, user['password'])
        return password_check
    except User.DoesNotExist:
        return False


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if authenticateUser(username, password):
        access_token = create_access_token(
            data={"sub": username}, expires_delta=timedelta(minutes=60)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


@app.get("/")
async def read_root(token: str = Depends(Oauth2_scheme)):
    return {"token": token}
