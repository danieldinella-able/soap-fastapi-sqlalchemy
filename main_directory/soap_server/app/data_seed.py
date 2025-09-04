from .db import engine, SessionLocal
from .models import Base, BookORM

def init_db():
    Base.metadata.create_all(bind=engine)

def seed_books():
    demo = [
        BookORM(isbn="9780001", title="FastAPI Deep Dive", price=29.90),
        BookORM(isbn="9780002", title="Python Patterns",  price=24.90),
        BookORM(isbn="9780003", title="SQLAlchemy Basics", price=19.90),
    ]
    with SessionLocal() as s:
        # evita duplicati se lo rilanci
        existing = {b.isbn for b in s.query(BookORM.isbn).all()}
        for b in demo:
            if b.isbn not in existing:
                s.add(b)
        s.commit()

if __name__ == "__main__":
    init_db()
    seed_books()
    print("DB pronto con libri demo.")
