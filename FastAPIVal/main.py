import csv
import json
import os
from fastapi import Body, FastAPI, HTTPException, Path
from typing import List, Dict, Any, Union, Optional, TypedDict
from pydantic import BaseModel, Field

class Producto(BaseModel):
    codigo: int
    nombre: str
    valor: float
    existencias: int

class ProductoRespuesta(TypedDict):
    Mensaje: str
    Producto: Optional[Producto]

class productoCreate(BaseModel):
    codigo: int
    nombre: str=Field(min_length=5,max_length=15)
    valor: float=Field(gt=0)
    existencias: int=Field(gt=0, le=10, default=10)

app = FastAPI()

productos = [
    {"codigo": 1, "nombre": "Esfero", "valor": 3500, "existencias": 10},
    {"codigo": 2, "nombre": "Cuaderno", "valor": 5000, "existencias": 25},
    {"codigo": 3, "nombre": "Lápiz", "valor": 200, "existencias": 12},
]

@app.get('/lista', response_model=List[Producto])
def mensaje():
    return productos

@app.get('/productorespuestaAny/{cod}', response_model=Dict[str, Any])
def buscaproducto(cod:int=Path(gt=0)):
    for producto in productos:
        if producto["codigo"]==cod:
            return {
                "Mensaje" : "Producto Encontrado",
                "Producto" : producto
            }
    return {
        "Mensaje": "Producto NO encontrado"
    }

@app.get('/productorespuesta/{cod}', response_model=Dict[str, Union[str, Optional[Dict]]])
def buscaproductoUnion(cod:int=Path(gt=0)):
    for producto in productos:
        if producto["codigo"]==cod:
            return {
                "Mensaje" : "Producto Encontrado",
                "Producto" : producto
            }
    return {
        "Mensaje": "Producto NO encontrado"
    }

@app.get('/productorespuestaEsquema/{cod}', response_model=ProductoRespuesta)
def buscaproductoEsquema(cod:int=Path(gt=0)):
    for producto in productos:
        if producto["codigo"]==cod:
            return ProductoRespuesta(
                Mensaje="Producto Encontrado",
                Producto=producto
            )
    return ProductoRespuesta(
        Mensaje="Producto NO enconrado",
        Producto=None
    )

@app.post('/crearProdEsquema')
def crearproducto(prod:Producto):
    productos.append(prod.model_dump())
    return productos

@app.post('/crearProdEsquema')
def crearproductoval(prod:productoCreate):
    productos.append(prod.model_dump())
    return productos