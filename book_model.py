from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


class Book(BaseModel):
    title: str = Field(..., example="My Life My Way")
    author: str = Field(..., example="John Doe")
    description: str = Field(..., example="A captivating story of self-discovery.")
    price: float = Field(..., example=19.99)
    stock: int = Field(..., example=10)
    sales: Optional[int] = Field(..., example=10)

    class Config:
        json_encoders = {
            ObjectId: ObjectIdStr,
        }
