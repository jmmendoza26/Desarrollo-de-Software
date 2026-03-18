from fastapi import FastAPI

app = FastAPI()

# --------------------
# Parámetros por ruta
# --------------------

@app.get('/')
def mensaje():
    return "Bienvenido a FastAPi Ingeniero de sistemas y computación"

@app.get('/{nombre}/{codigo}')
def mensaje2(nombre:str, codigo:int):
    return f"Bienvenido {nombre} - {codigo}"

# -------------------
# Parámetros por función \ Se ingresan en la URL
# <URL>/dir/?<var> = dato & <var2> = dato2. <- Se escribe todo pegado
# -------------------


@app.get('/uno/')
def mensaje3(edad:int = 18, nombre:str ='',semestre:int = 1):
    return f"Bienvenido {nombre}, Su edad es {edad}, Semestre: {semestre}"