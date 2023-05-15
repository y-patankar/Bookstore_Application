from fastapi import FastAPI, Query
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from book_model import Book
from pymongo.collection import Collection
from typing import List
import motor.motor_asyncio
from typing import Union, Dict

app = FastAPI()

# Connect to MongoDB using Motor
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["bookstore"]
collection = db["books"]


@app.post("/books")
async def create_book(book: Book):
    try:
        # Insert the book data into MongoDB asynchronously
        book_data = jsonable_encoder(book)
        await collection.insert_one(book_data)

        return {"message": "Book created successfully"}
    except Exception as e:
        # Log the error and return an appropriate error message
        print(f"Error creating book: {e}")
        return {"message": "Failed to create book"}


@app.get("/books/count")
async def get_total_books():
    try:
        # Aggregation pipeline to get the total number of books
        pipeline = [
            {"$group": {"_id": None, "total_books": {"$sum": 1}}}
        ]

        result = await collection.aggregate(pipeline).to_list(None)

        if result:
            total_books = result[0]["total_books"]
            return {"total_books": total_books}
        else:
            return {"total_books": 0}
    except Exception as e:
        # Log the error and return an appropriate error message
        print(f"Error getting total books count: {e}")
        return {"message": "Failed to retrieve total books count"}


@app.get("/books")
async def search_books(title: str = None, author: str = None, min_price: float = None, max_price: float = None):
    try:
        query_filter = {}

        if title:
            query_filter["title"] = {"$regex": title, "$options": "i"}

        if author:
            query_filter["author"] = {"$regex": author, "$options": "i"}

        if min_price is not None and max_price is not None:
            query_filter["price"] = {"$gte": min_price, "$lte": max_price}
        elif min_price is not None:
            query_filter["price"] = {"$gte": min_price}
        elif max_price is not None:
            query_filter["price"] = {"$lte": max_price}

        books = await collection.find(query_filter).to_list(None)

        results = [str(Book(**book)) for book in books]
        return {"results": results}
    except Exception as e:
        # Log the error and return an appropriate error message
        print(f"Error searching books: {e}")
        return {"message": "Failed to search books"}


@app.get("/books/top-selling", response_model=List[Book])
async def get_top_selling_books():
    try:
        # Aggregation pipeline to get the top 5 best-selling books based on sales
        pipeline = [
            {"$sort": {"sales": -1}},
            {"$limit": 5}
        ]

        result = await collection.aggregate(pipeline).to_list(None)
        top_books = list(result)

        return top_books
    except Exception as e:
        # Log the error and return an appropriate error message
        print(f"Error getting top selling books: {e}")
        return {"message": "Failed to retrieve top selling books"}


@app.get("/books/top-books", response_model=List[str])
async def get_top_authors_with_most_books():
    try:
        # Aggregation pipeline to get the top 5 authors with the most books
        pipeline = [
            {"$group": {"_id": "$author", "bookCount": {"$sum": 1}}},
            {"$sort": {"bookCount": -1}},
            {"$limit": 5},
            {"$project": {"_id": 0, "author": "$_id"}}
        ]

        result = await collection.aggregate(pipeline).to_list(None)
        top_authors = [doc["author"] for doc in result]

        return top_authors
    except Exception as e:
        # Log the error and return an appropriate error message
        print(f"Error getting top authors: {e}")
        return {"message": "Failed to retrieve top authors"}
    
@app.get("/books/{book_id}", response_model=Union[Book, Dict[str, str]])
async def get_book_by_id(book_id: str):
    try:
        book = await collection.find_one({"_id": ObjectId(book_id)})
        if book:
            return Book(**book)
        else:
            return {"message": "No book found with the given ID"}
    except Exception as e:
        # Log the error and return an appropriate error message
        print(f"Error getting book by ID: {e}")
        return {"message": "Failed to retrieve book"}


@app.put("/books/{book_id}")
async def update_book(book_id: str, book: Book):
    try:
        updated_book_data = jsonable_encoder(book)
        await collection.update_one({"_id": ObjectId(book_id)}, {"$set": updated_book_data})
        return {"message": "Book updated successfully"}
    except Exception as e:
        # Log the error and return an appropriate error message
        print(f"Error updating book: {e}")
        return {"message": "Failed to update book"}


@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    try:
        await collection.delete_one({"_id": ObjectId(book_id)})
        return {"message": "Book deleted successfully"}
    except Exception as e:
        # Log the error and return an appropriate error message
        print(f"Error deleting book: {e}")
        return {"message": "Failed to delete book"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
