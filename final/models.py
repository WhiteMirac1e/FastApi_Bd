from datetime import datetime

from pydantic import BaseModel, Field


class ProductsIn(BaseModel):
    name: str = Field(max_length=32)
    descriptions: str = Field(max_length=128)
    cost: float = Field(default=0)


class Products(BaseModel):
    id: int
    name: str = Field(max_length=32)
    descriptions: str = Field(max_length=128)
    cost: float = Field(default=0)


class OrdersIn(BaseModel):
    user_id: int
    product_id: int
    date: datetime = Field(default=datetime.now())
    status: str = Field(default="created")


class Orders(BaseModel):
    id: int
    user_id: int
    product_id: int
    date: datetime = Field(default=datetime.now())
    status: str = Field(default="created")


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=3)


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=3)
