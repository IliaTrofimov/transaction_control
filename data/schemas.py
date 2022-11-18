import decimal

from pydantic import BaseModel


class Transaction(BaseModel):
    value: int

