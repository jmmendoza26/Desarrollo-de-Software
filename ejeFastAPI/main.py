import csv
import os
from fastapi import Body, FastAPI, HTTPException

app = FastAPI()

ARCHIVO_CSV = "productos.csv"

PRODUCTOS_INICIALES = [
    {"codigo": 1, "nombre": "Esfero", "valor": 3500, "existencias": 10},
    {"codigo": 2, "nombre": "Cuaderno", "valor": 5000, "existencias": 25},
    {"codigo": 3, "nombre": "Lápiz", "valor": 200, "existencias": 12},
]

def cargar_productos() -> list[dict]:
    if not os.path.exists(ARCHIVO_CSV):
        guardar_productos(PRODUCTOS_INICIALES)
        return [dict(p) for p in PRODUCTOS_INICIALES]
    with open(ARCHIVO_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [
            {"codigo": int(row["codigo"]), "nombre": row["nombre"],
             "valor": float(row["valor"]), "existencias": int(row["existencias"])}
            for row in reader
        ]

def guardar_productos(lista: list[dict]):
    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["codigo", "nombre", "valor", "existencias"])
        writer.writeheader()
        writer.writerows(lista)

productos = cargar_productos()

# --------------------
# Parámetros por ruta
# --------------------

@app.get('/')
def mensaje():
    return "Bienvenido a FastAPi Ingeniero de sistemas y computación"

# @app.get('/{nombre}/{codigo}')
# def mensaje2(nombre:str, codigo:int):
#     return f"Bienvenido {nombre} - {codigo}"

# -------------------
# Parámetros por función \ Se ingresan en la URL
# <URL>/dir/?<var> = dato & <var2> = dato2. <- Se escribe todo pegado
# -------------------

@app.get('/uno/')
def mensaje3(edad:int = 18, nombre:str ='',semestre:int = 1):
    return f"Bienvenido {nombre}, Su edad es {edad}, Semestre: {semestre}"

@app.get('/productos')
def listProductos():
    return productos

# Validación 1: código mayor a cero
# Validación 2: mensaje si no existe
@app.get('/productos/{cod}')
def findProduct(cod:int):
    if cod <= 0:
        raise HTTPException(status_code=400, detail="El código debe ser mayor a cero")
    for p in productos:
        if p["codigo"] == cod:
            return p
    raise HTTPException(status_code=404, detail=f"Producto con código {cod} no encontrado")

@app.get('/productos/')
def findProduct2(nom:str=""):
    for p in productos:
        if p["nombre"] == nom:
            return p
    raise HTTPException(status_code=404, detail=f"Producto '{nom}' no encontrado")

# Validación 3: código consecutivo automático
# Validación 4: valor y existencias mayores a cero
@app.post('/productos')
def createProduct(nombre:str, valor:float, existencias:int):
    if valor <= 0:
        raise HTTPException(status_code=400, detail="El valor debe ser mayor a cero")
    if existencias <= 0:
        raise HTTPException(status_code=400, detail="Las existencias deben ser mayores a cero")
    nuevo_codigo = max(p["codigo"] for p in productos) + 1 if productos else 1
    nuevo_producto = {
        "codigo": nuevo_codigo,
        "nombre": nombre,
        "valor": valor,
        "existencias": existencias
    }
    productos.append(nuevo_producto)
    guardar_productos(productos)
    return nuevo_producto

@app.post('/productos2')
def createProduct2(
    nombre:str=Body(),
    valor:float=Body(),
    existencias:int=Body()):
    if valor <= 0:
        raise HTTPException(status_code=400, detail="El valor debe ser mayor a cero")
    if existencias <= 0:
        raise HTTPException(status_code=400, detail="Las existencias deben ser mayores a cero")
    nuevo_codigo = max(p["codigo"] for p in productos) + 1 if productos else 1
    nuevo_producto = {
        "codigo": nuevo_codigo,
        "nombre": nombre,
        "valor": valor,
        "existencias": existencias
    }
    productos.append(nuevo_producto)
    guardar_productos(productos)
    return nuevo_producto

# Validación 5: error si no existe
# Validación 6: valor y existencias mayores a cero
# Validación 7: mostrar producto antes y después
@app.put('/producto')
def updateProduct(
    cod:int,
    nom:str=Body(),
    val:float=Body(),
    exis:int=Body()
    ):
    if val <= 0:
        raise HTTPException(status_code=400, detail="El valor debe ser mayor a cero")
    if exis <= 0:
        raise HTTPException(status_code=400, detail="Las existencias deben ser mayores a cero")
    for prod in productos:
        if prod["codigo"] == cod:
            antes = dict(prod)
            prod["nombre"] = nom
            prod["valor"] = val
            prod["existencias"] = exis
            guardar_productos(productos)
            return {"antes": antes, "después": dict(prod)}
    raise HTTPException(status_code=404, detail=f"Producto con código {cod} no encontrado")

# Validación 8: error si no existe, mostrar producto eliminado
@app.delete('/productos/{cod}')
def deleteProduct(cod:int):
    for prod in productos:
        if prod["codigo"] == cod:
            productos.remove(prod)
            guardar_productos(productos)
            return {"mensaje": "Producto eliminado", "producto": prod}
    raise HTTPException(status_code=404, detail=f"Producto con código {cod} no encontrado")