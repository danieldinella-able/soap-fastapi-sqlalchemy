from app.core.base.base_model import BaseModel


class Book(BaseModel):
    isbn: str
    title: str
    price: float
