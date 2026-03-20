#Crear entorno virtual
python3 -m venv venv

#Activar entorno virtual
source venv/bin/activate #Activar entorno virtual

pip install fastapi uvicorn

touch main.py

#Abrir API y recarga automática
uvicorn main:app --reload 