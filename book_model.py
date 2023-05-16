#This is code for defining the book model. 

from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


class ObjectIdStr(str):
    # Custom validator for ObjectIdStr
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    # Validator function for validating ObjectIdStr
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


class Book(BaseModel):
    # Fields for Book model
    title: str = Field(..., example="My Life My Way")  # Title of the book
    author: str = Field(..., example="John Doe")  # Author of the book
    description: str = Field(..., example="A captivating story of self-discovery.")  # Description of the book
    price: float = Field(..., example=19.99)  # Price of the book
    stock: int = Field(..., example=10)  # Stock quantity of the book
    sales: Optional[int] = Field(..., example=10)  # Optional field for sales count

    class Config:
        # Custom JSON encoders
        json_encoders = {
            ObjectId: ObjectIdStr,  # Encode ObjectId using ObjectIdStr class
        }
