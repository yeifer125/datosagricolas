from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import json
import glob
import os

app = FastAPI(title="Dashboard Datos Agrícolas")

DATA_DIR = "data"

def cargar_ultimo(nombre):
    archivos = sorted(glob.glob(f"{DATA_DIR}/{nombre}_*.json"))
    if not archivos:
        return {}
    with open(archivos[-1], "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/series")
def series():
    return cargar_ultimo("series_productos")

@app.get("/tendencias")
def tendencias():
    return cargar_ultimo("tendencias")

@app.get("/predicciones")
def predicciones():
    return cargar_ultimo("predicciones")

@app.get("/alertas")
def alertas():
    return cargar_ultimo("alertas")

# SERVIR DASHBOARD
app.mount("/", StaticFiles(directory="dashboard", html=True), name="dashboard")
