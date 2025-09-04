from app.core.base.base_model import BaseModel


class Book(BaseModel):
    isbn: str
    title: str
    author: str
    price: float