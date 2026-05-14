from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager


class hotel(SQLModel, table=True):
    codigo: int = Field(primary_key=True)
    nombre: str
    ciudad: str
    valornoche: float

postgres_url = "postgresql://" \
"postgres:postgres123@localhost/ventas"
engine = create_engine(postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Montar la carpeta static para servir archivos CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar la carpeta de plantillas
templates = Jinja2Templates(directory="templates")

@app.get("/lista")
def leer_hoteles():
    with Session(engine) as session:
        hoteles = session.exec(select(hotel)).all()
        return {"hoteles":hoteles}

@app.get("/hotel/{codigo}")
def buscar_hotel_por_codigo(codigo: int):
    with Session(engine) as session:
        h = session.get(hotel, codigo)
        if not h:
            raise HTTPException(status_code=404, detail="Hotel no encontrado")
        return h

@app.get("/ciudad/{ciudad}")
def buscar_hoteles_por_ciudad(ciudad: str):
    with Session(engine) as session:
        hoteles = session.exec(select(hotel).where(hotel.ciudad == ciudad)).all()
        return {"hoteles":hoteles}

@app.post("/hotel", status_code=201)
def adicionar_hotel(nuevo_hotel: hotel):
    with Session(engine) as session:
        session.add(nuevo_hotel)
        session.commit()
        session.refresh(nuevo_hotel)
        return nuevo_hotel

@app.get("/")
async def pagina_principal(request: Request):
    with Session(engine) as session:
        hoteles = session.exec(select(hotel)).all()
        return templates.TemplateResponse(
            "index.html",{"request":request,"hoteles":hoteles}
            )

   