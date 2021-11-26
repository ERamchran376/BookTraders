# BookTraders
This is my groups API from my BSc (Hons) IT - Software Engineering course in 2021

/Get_all_books
Endpoint: This end point allows to get all the books from the API.
There are no attributes associated with this endpoint.
/get_book_id
Endpoint: This allow us to get book details via the book id from the database.
Attributes:
book_id - integer
/search_book
Endpoint: This will allow us to search for the books in the database by Title or year.
Attributes:
title - string
year - query
/delete_book/{book_id}
Endpoint: This will allow us to delete books in the database via the Delete Book option.
Attributes:
book_id - integer
/search_author
Endpoint: This allows us to search for the authors in the database via the Search Author
option.
Attributes:
author - string
/add_new_book
Endpoint: This allows us to add books to the database via Title, Author, Year, Book ID, Price,
Quantity.
Attributes:
title – string
author – string
year – Int
book id – Int
price – string
quantity – Int
/sign_up
Endpoint: This will allow us to sign up to access the database containing all the books.
Attributes:
username – string
password – string
email - string
/token
Endpoint: is a unique identifier of an application requesting access to your service.
There are no attributes associated with this endpoint.
