from pydantic import BaseModel

class ProductBase(BaseModel):
    descricao: str
    preco: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    codigo: int