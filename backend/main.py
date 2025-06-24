from fastapi import FastAPI
from .database import init_db

app = FastAPI(title="EnlaceRB API")

# Inicializa la base de datos al iniciar
init_db()

@app.get("/")
def home():
    return {"mensaje": "EnlaceRB backend está funcionando"}
