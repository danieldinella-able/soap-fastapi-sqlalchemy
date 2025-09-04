from zeep import Client


def main():
    c = Client("http://localhost:8001/?wsdl")
    print(c.service.ListBooks())
    print(c.service.GetBook("9780001"))


if __name__ == "__main__":
    main()

