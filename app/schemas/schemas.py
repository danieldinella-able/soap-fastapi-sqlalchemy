from pydantic import BaseModel, Field

class BookOut(BaseModel):
    isbn: str
    title: str
    price: float

class OrderIn(BaseModel):
    isbn: str = Field(min_length=5)
    qty: int = Field(ge=1)

class OrderOut(BaseModel):
    id: int
    isbn: str
    qty: int