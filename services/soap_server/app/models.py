from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, func

Base = declarative_base()

class BookORM(Base):
    __tablename__ = "books"
    isbn  = Column(String, primary_key=True)            # es: "9780001"
    title = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

class OrderORM(Base):
    __tablename__ = "orders"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    isbn       = Column(String, ForeignKey("books.isbn"), nullable=False)
    qty        = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    book       = relationship("BookORM")
