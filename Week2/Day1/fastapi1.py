#--------------------------------------------CREATE FIRST API ENDPOINT ----------------------

from fastapi import FastAPI,Body    # importing the FASTAPI
app = FastAPI()                  # It create an API Application

@app.get("/user")                    #It define an End-Point (url)
async def get_user():
    return {"Message": "Hello ALL!"}

#when we run this application it goes to the url --> "http//:127.0.0:8000/user" and it will display he return message..

#--------------------------------------GET REQUEST METHOD-----------------------------------------
#it used to retrieve/fetch the data from the server
#it is read only 
#it does not modify the data

BOOKS = [
    {'title': 'Title One', 'author' : 'Author One', 'category': 'science'},
{'title': 'Title Two', 'author' : 'Author Two', 'category' : 'science'},
{'title': 'Title Three', 'author': 'Author Three', 'category' : 'history'},
{'title': 'Title Four', 'author' : 'Author Four', 'category': 'math'},
{'title': 'Title Five', 'author' : 'Author Five', 'category': 'math'}
]

@app.get("/books")

async def get_books():
    return BOOKS

#------------------------------------PATH PARAMETER---------------------------------
#it is a value that pass inside the URL path
#it helps you identify a specific resource
#EG--> we have created a endpoint to return a 100 books .but for returing a specific book from 100 books we can not create a endpoint for every book.
#so, here the path parameter is used..
#It is used to get One Item

@app.get("/books/{book_title}")     #---> {book_title} --> dynamic param (PP)..

async def get_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():  #casefold() ---> converts text into lowercase..
            return book
        
@app.get("/books/category/{category}")
async def get_books_bycategory(category: str):
    book_list = []
    for book in BOOKS:
        if book.get("category") and book.get("category").casefold() == category.casefold():
            book_list.append(book)

    return book_list
        


#---------------------------------------QUERY PARAMETER------------------------------
#It is a value passed in the URL after "?" to filter or modify data
#They are requests parameters that have been attached after a "?"
#It is used for FILTER/SEARCH

@app.get("/books/")
async def get_book_by_query(category: str):
    books_list = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_list.append(book)
    return books_list


#----------------------------------------PATH and QUERY PARAM TOGETHER ---------------------------------
#we can use both QP and PP together

@app.get("/books/{book_author}/")
async def get_book_by_query_and_author(book_author: str, category: str):
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            return book


#---------------------------------------POST REQUEST METHOD-------------------------------------
#-It is ued to send data to the server and usually create something new.
#it is to send and create data
#it can have a Body() that has additional information that GET does not have.

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

#another way of adding book

@app.post("/books/create_another-book")
def create_book(book: dict):
    BOOKS.append(book)
    return {"message": "Book added"}

#---------------------------------------PUT REQUEST METHOD-------------------------------------
# It is used to update an existing resource completely (full replacement)
#replace old data with new data

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold(): #here we take "title" as an identifier
            BOOKS[i] = updated_book
            return {"message": "Book updated successfully"}
        
#-------------------------------DELETE REQUEST METHOD------------------------------
#it is used to remove data from the server
#it uses path parameters as an identifier

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
