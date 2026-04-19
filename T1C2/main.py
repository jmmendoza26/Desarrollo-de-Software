from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Montar la carpeta static para servir archivos CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar la carpeta de plantillas
templates = Jinja2Templates(directory="templates")

# Lista de productos definida en el taller
productos = [
    {"codigo": 1, "nombre": "Cuaderno", "valoru": 5000,  "existencias": 100},
    {"codigo": 2, "nombre": "Esfero",   "valoru": 2500,  "existencias": 250},
    {"codigo": 3, "nombre": "Lapiz",    "valoru": 1500,  "existencias": 300},
]

def calcular_estado(existencias: int) -> str:
    """Retorna el estado del inventario según la cantidad de existencias."""
    if existencias < 50:
        return "Bajo"
    elif existencias <= 100:
        return "Medio"
    else:
        return "Alto"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Construir la lista de productos con los campos calculados
    productos_calculados = []
    for p in productos:
        productos_calculados.append({
            "codigo":      p["codigo"],
            "nombre":      p["nombre"],
            "valoru":      p["valoru"],
            "existencias": p["existencias"],
            "valor_total": p["valoru"] * p["existencias"],
            "estado":      calcular_estado(p["existencias"]),
        })

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "productos": productos_calculados}
    )