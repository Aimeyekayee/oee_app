from pydantic import BaseModel


class FruitBase(BaseModel):
    name: str
    amount: int
    price:int

