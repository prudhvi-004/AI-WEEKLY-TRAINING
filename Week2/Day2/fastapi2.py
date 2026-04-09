from typing import Optional   # Optional → field can be missing / None
from fastapi import FastAPI, Path, Query  # FastAPI → framework to build APIs
from pydantic import BaseModel, Field   # BaseModel → validation model, Field → add rules/constraints

app = FastAPI()   # FastAPI() → creates API app instance

class Book:
    def __init__(self, id, title, author, description, rating, published_date):
        # Normal Python class → used for internal storage (no validation)
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

#------------------------------------PYDANTIC-------------------------
#it is a python lib used for data modeling , data parsing, and has a effiecient error handling
#validate data
#enforce types
#convert data automatically


class BookRequest(BaseModel):   # BaseModel → enables validation + type checking

    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    # Optional[int] → not required
    # Field(default=None) → sets default value

    title: str = Field(min_length=3)  
    # Field(min_length=3) → validation rule (min characters)

    author: str = Field(min_length=1)  
    # Field() → adds constraints to input

    description: str = Field(min_length=1, max_length=100)  
    # max_length → restricts max characters

    rating: int = Field(gt=0, lt=6)  
    # gt → greater than, lt → less than

    published_date: int = Field(gt=1999, lt=2031)  
    # validates year range

    model_config = {  
        # model_config → Pydantic v2 config settings
        "json_schema_extra": {  
            # json_schema_extra → adds example to Swagger docs
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2029
            }
        }
    }


BOOKS = [   # List → acts like in-memory database
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'An awesome book!', 5, 2029),
    Book(4, 'Python Mastery', 'John Doe', 'Complete guide to Python', 5, 2028),
    Book(5, 'Deep Learning Essentials', 'Andrew Ng', 'Learn deep learning basics', 5, 2027),
    Book(6, 'Clean Code Concepts', 'Robert Martin', 'Writing clean code', 5, 2026),
    Book(7, 'Machine Learning Basics', 'Alice Smith', 'Intro to ML concepts', 4, 2025)
]


@app.get("/books")   # @app.get → API endpoint (GET request)
async def read_all_books():   # async → allows async handling (non-blocking)
    return BOOKS


#to get book by ID..  Path Param
@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        

 #to get book by rating.. Query Param
@app.get("/books/")
async def get_book_by_rating(rating: int = Query(gt=-1,ls=6)):
    books = []
    for book in BOOKS:
        if book.rating == rating:
            books.append(book)
    return books


@app.post("/books/create_book")   # @app.post → API endpoint (POST request)
async def add_book(book_request: BookRequest):   #here we added the data validation(BookRequest) for add_book..
    # we no need to add Body() like before.
    # pydantic will initilaize automatically.
    # BookRequest → request body is validated automatically

    new_book = Book(**book_request.model_dump())  
    # model_dump() → converts Pydantic model → dictionary
    #in above the book_request is pydantic model bcs we assigned the book_request as BookRequest. so, it is. 
    # ** → unpacks dictionary into arguments
    #Arguments = values you pass into a function or class

    new_book = assign_book_id(new_book)

    BOOKS.append(new_book)   # append() → adds item to list

    return new_book


#Update book using ID 
@app.put("/books/updatebook/")
async def update_book(upd_book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == upd_book.id:
            BOOKS[i] = upd_book
            upd_book.id = i+1


#Delete a book using ID..
@app.delete("/books/deletebook/{id}")
async def delete_book(id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            break
        
#function for assigning ID for book..
def assign_book_id(book: Book):   # function → custom logic

    if len(BOOKS) == 0:   # len() → number of items in list
        book.id = 1
    else:
        book.id = BOOKS[-1].id + 1   # BOOKS[-1] → last element

    return book
