from fastapi import FastAPI, Request, Path
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import json

app = FastAPI()

# Montar la carpeta static para servir archivos CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar la carpeta de plantillas
templates = Jinja2Templates(directory="templates")

class hotel(BaseModel):
    codigo: int
    nombre: str
    ciudad: str
    valorNoche: float
# Lista de hoteles 
hoteles = [
    {
        "codigo": 101, 
        "nombre": "Hotel Bogotá Plaza",
        "ciudad": "Bogotá", 
        "valorNoche": 280000
        },
    {
        "codigo": 102,
        "nombre": "Casa Medina",
        "ciudad": "Bogotá",
        "valorNoche": 350000
        },
    {
        "codigo": 103,
        "nombre": "Hotel de la Ópera",
        "ciudad": "Bogotá",
        "valorNoche": 420000
        },
    ]

@app.get("/", response_class=HTMLResponse)

async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",{"request": request, "hoteles": hoteles})

@app.get("/listaciudad", response_class=HTMLResponse)
async def listaC(request: Request, ciudad:str):
    hoteles_ciudad= [x for x in hoteles if x["ciudad"] == ciudad]
    return templates.TemplateResponse(
        "index.html",{"request": request, "hoteles": hoteles_ciudad}
    )

@app.post("/crearhotel")
def crearhoteles(ht: hotel):
    for hotel in hoteles:
        if hotel["codigo"] == ht.codigo:
            return "El código ya está registrado"

    hoteles.append(ht.model_dump())

    archivo = open("hoteles.json", "w")
    json.dump(hoteles, archivo, indent=4,ensure_ascii=False)
    archivo.close()

    return hoteles
