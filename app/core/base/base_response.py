"""Modello di risposta standard per i manager/API.

Contiene uno `status` (SUCCESS/ERROR), un `payload` opzionale e un messaggio.
"""

from typing import Any

from app.core.base.base_enum import BaseEnum
from app.core.base.base_model import BaseModel

class BaseResponse(BaseModel):
    class Status(str, BaseEnum):
        SUCCESS = "SUCCESS"
        ERROR = "ERROR"

    message: str | None
    payload: Any
    status: Status

    def __init__(self, status: Status, payload: Any=None, message: str=None):
        super().__init__(payload=payload, message=message, status=status)

    @classmethod
    def success(cls, payload=None):
        """Crea una risposta di successo con payload opzionale."""
        return cls(status=cls.Status.SUCCESS, payload=payload)

    @classmethod
    def error(cls, message, payload=None):
        """Crea una risposta di errore con messaggio e payload opzionale."""
        return cls(status=cls.Status.ERROR, message=message, payload=payload)

    def is_success(self) -> bool:
        """Indica se la risposta è di successo."""
        return self.status == self.Status.SUCCESS


#TODO sostituire con PyTest
if __name__ == "__main__":
    b = BaseResponse(status=BaseResponse.Status.SUCCESS, payload={"ciao": "mondo"}, message="dsdfsfsdf")
    print(b.status == BaseResponse.Status.SUCCESS)
