import os
from spyne import Application, rpc, ServiceBase, Unicode, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from app.db import SessionLocal
from app.models import BookORM
from app.soap_types import BookType, BookNotFoundFault
from app.data_seed import init_db

TNS = 'urn:bookshop'

class BookCatalogService(ServiceBase):

    @rpc(_returns=Iterable(BookType))
    def ListBooks(ctx):
        with SessionLocal() as s:
            for row in s.query(BookORM).order_by(BookORM.isbn).all():
                yield BookType(isbn=row.isbn, title=row.title, price=str(row.price))

    @rpc(Unicode, _returns=BookType)
    def GetBook(ctx, isbn):
        with SessionLocal() as s:
            row = s.get(BookORM, isbn)
            if not row:
                raise BookNotFoundFault(isbn)
            return BookType(isbn=row.isbn, title=row.title, price=str(row.price))

application = Application(
    [BookCatalogService],
    tns=TNS,
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

# Ensure DB schema exists (creates SQLite file and tables if missing)
try:
    init_db()
except Exception as e:
    # Don't crash boot if init fails; print and continue (container logs)
    print(f"[soap_server] DB init error: {e}")

# Avvio di comodo senza gunicorn
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    port = int(os.getenv("PORT", "8001"))
    print(f"SOAP up → http://localhost:{port}/?wsdl")
    server = make_server("0.0.0.0", port, wsgi_app)
    server.serve_forever()
