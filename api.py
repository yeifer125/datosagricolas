from fastapi import FastAPI
import json

app = FastAPI(title="IA Datos Agrícolas")

def cargar(nombre):
    with open(nombre, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/series")
def series():
    return cargar("series_productos.json")

@app.get("/tendencias")
def tendencias():
    return cargar("tendencias.json")

@app.get("/predicciones")
def predicciones():
    return cargar("predicciones.json")

@app.get("/alertas")
def alertas():
    return cargar("alertas.json")
