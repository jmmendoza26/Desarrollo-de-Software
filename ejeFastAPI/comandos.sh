python3 -m venv venv #Crear entorno virtual
source venv/bin/activate #Activar entorno virtual
pip install fastapi uvicorn

touch main.py

uvicorn main:app --reload #Abrir API y recarga automática