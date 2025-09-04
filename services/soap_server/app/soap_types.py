from spyne import ComplexModel, Unicode, Integer, Fault

class BookType(ComplexModel):
    isbn  = Unicode
    title = Unicode
    price = Unicode  # teniamolo string per semplicità (altrimenti Decimal)

class OrderReceiptType(ComplexModel):
    id         = Integer
    isbn       = Unicode
    qty        = Integer
    created_at = Unicode

class BookNotFoundFault(Fault):
    def __init__(self, isbn: str):
        super().__init__(
            faultcode="Client.BookNotFound",
            faultstring=f"Book {isbn} not found",
        )
