# tmp_check.py (fuori dal servizio)
if __name__ == "__main__":
    from zeep import Client
    c = Client("http://localhost:8001/?wsdl")
    print(c.service.ListBooks())
    print(c.service.GetBook("9780001"))