from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
# Montar archivos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home():
    return RedirectResponse(url="/usuario/Invitado")

@app.get("/usuario/{nombre}")
async def usuario(request: Request, nombre: str, edad: int = 25, casado: bool = False):
    datos = {
        "request": request,
        "nombre": nombre,
        "edad": edad,
        "casado": casado,
        "hobbies": ["programar", "jugar", "leer"]
    }
    return templates.TemplateResponse("saludo.html", datos)