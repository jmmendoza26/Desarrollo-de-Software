from fastapi import Body, FastAPI

app = FastAPI()

productos = [{
    "codigo" : 1,
    "nombre" : "Esfero",
    "valor": 3500,
    "existencias": 10
},{
    "codigo" : 2,
    "nombre" : "Cuaderno",
    "valor": 5000,
    "existencias": 25
},{
    "codigo" : 3,
    "nombre" : "Lápiz",
    "valor": 200,
    "existencias": 12
},]

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

@app.get('/productos/{cod}')
def findProduct(cod:int):
    for p in productos:
        if p["codigo"] == cod:
            return p
    return f"Producto {cod} no encontrado"

@app.get('/productos/')
def findProduct2(nom:str=""):
    for p in productos:
        if p["nombre"] == nom:
            return p
    return f"Producto {nom} no encontrado"

@app.post('/productos')
def createProduct(nombre:str,codigo:int,valor:float,existencias:int):
    productos.append(
        {"codigo":codigo,
         "nombre":nombre,
         "valor":valor,
         "existencias":existencias}
    )
    return productos

@app.post('/productos2')
def createProduct2(
    nombre:str=Body(),
    codigo:int=Body(),
    valor:float=Body(),
    existencias:int=Body()):
    productos.append(
        {"codigo":codigo,
         "nombre":nombre,
         "valor":valor,
         "existencias":existencias}
    )
    return productos

@app.put('/producto')
def updateProduct(
    cod:int,
    nom:str=Body(),
    val:float=Body(),
    exis:int=Body()
    ):
    for prod in productos:
        if prod["codigo"] == cod:
            prod["nombre"] = nom
            prod["valor"] = val
            prod["existenvias"] = exis
    return productos

@app.delete('/productos/{cod}')
def deleteProduct(cod:int):
    for prod in productos:
        if prod["codigo"] == cod:
            productos.remove(prod)
    return productos