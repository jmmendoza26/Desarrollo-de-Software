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
def leer_hotel():
    with Session(engine) as session:
        hoteles = session.exec(select(hotel)).all()
        return {"hoteles":hoteles}

@app.get("/")
async def leer_hotel(request: Request):
    with Session(engine) as session:
        hoteles = session.exec(select(hotel)).all()
        return templates.TemplateResponse(
            "index.html",{"request":request,"hoteles":hoteles}
            )

@app.get("/buscar")
async def hotel_cod(request: Request):
    with Session(engine) as session:
        hoteles = session.exec(select(hotel))
    pass   