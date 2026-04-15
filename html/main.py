from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/str", response_class=HTMLResponse)
async def pagina_inicio():
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head><title>Página de Inicio</title></head>
    <body>
        <h1>¡Bienvenido a la Página de Inicio!</h1>
        <p>Esta es la página principal de nuestro sitio web.</p>
    </body>
    </html>
    """
    return html_content

@app.get("/fileResponse", response_class=HTMLResponse)
async def pagina_estatica():
    return FileResponse("templates/index.html")

@app.get("/openfile", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/", response_class=HTMLResponse)
async def pagina_con_estilo():
    return FileResponse("templates/index.html")