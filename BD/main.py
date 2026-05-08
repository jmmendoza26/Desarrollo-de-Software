from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, HTTPException
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

@app.get("/")
def leer_hotel():
    with Session(engine) as session:
        hoteles = session.exec(select(hotel)).all()
        return {"Hoteles": hoteles}
    