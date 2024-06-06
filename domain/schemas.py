from pydantic import BaseModel

class XMLCep(BaseModel):
    cep: str
    logradouro: str
    complemento: str
    bairro: str
    localidade: str
    uf: str
    ibge: str
    gia: str
    ddd: str
    siafi: str

class CepResponse(BaseModel):
    xmlcep: XMLCep
