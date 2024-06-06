from fastapi import FastAPI, HTTPException

from domain.models import execute_query
from domain.dto import ProductCreate,Product
from domain.schemas import CepResponse, XMLCep

import httpx
import xmltodict

app = FastAPI()

@app.post("/products/", response_model=Product)
def create_product(product: ProductCreate):
    query = "INSERT INTO products (descricao, preco) VALUES (%s, %s)"
    params = (product.descricao, product.preco)
    execute_query(query, params)
    
    query = "SELECT * FROM products ORDER BY codigo DESC LIMIT 1"
    created_product = execute_query(query)
    if not created_product:
        raise HTTPException(status_code=500, detail="Failed to retrieve the created product")
    return created_product[0]

@app.get("/products/", response_model=list[Product])
def read_products(skip: int = 0, limit: int = 10):
    query = "SELECT * FROM products where deleted is null LIMIT %s OFFSET %s"
    params = (limit, skip)
    products = execute_query(query, params)
    return products

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int):
    query = "SELECT * FROM products WHERE codigo = %s and deleted is null"
    params = (product_id,)
    products = execute_query(query, params)
    if len(products) == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[0]

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate):
    query = "UPDATE products SET descricao = %s, preco = %s WHERE codigo = %s"
    params = (product.descricao, product.preco, product_id)
    execute_query(query, params)
    
    query = "SELECT * FROM products WHERE codigo = %s"
    updated_product = execute_query(query, (product_id,))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product[0]

@app.delete("/products/{product_id}", response_model=bool)
def delete_product(product_id: int):
    query = "UPDATE products SET deleted= 1 where codigo = %s"
    params = (product_id,)
    execute_query(query, params)
    return True

@app.get("/cep/{cep}", response_model=dict)
async def get_cep_info(cep: str):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching CEP information")

@app.get("/cep-xml/{cep}", response_model=CepResponse)
async def get_cep_info_xml(cep: str):
    url = f"https://viacep.com.br/ws/{cep}/xml/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = xmltodict.parse(response.content)
            # Transform the parsed XML data into the CepResponse model
            cep_data = XMLCep(
                cep=data['xmlcep']['cep'],
                logradouro=data['xmlcep']['logradouro'],
                complemento=data['xmlcep']['complemento'],
                bairro=data['xmlcep']['bairro'],
                localidade=data['xmlcep']['localidade'],
                uf=data['xmlcep']['uf'],
                ibge=data['xmlcep']['ibge'],
                gia=data['xmlcep']['gia'],
                ddd=data['xmlcep']['ddd'],
                siafi=data['xmlcep']['siafi']
            )
            return CepResponse(xmlcep=cep_data)
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching CEP information")
        
if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)