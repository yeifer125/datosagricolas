import json
import requests
import subprocess
from datetime import datetime
from collections import defaultdict
import os

# =========================
# CONFIG
# =========================
URL_HISTORIAL = "https://raw.githubusercontent.com/yeifer125/iadatos/main/historial.json"
DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)

# =========================
# UTILIDADES
# =========================

def convertir_fecha(fecha):
    try:
        return datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        return None

def limpiar_numero(valor):
    if valor is None:
        return None

    if isinstance(valor, (int, float)):
        return float(valor)

    valor = str(valor).strip()

    if "," in valor and "." in valor:
        valor = valor.replace(".", "").replace(",", ".")
    elif "," in valor:
        valor = valor.replace(",", ".")

    try:
        return float(valor)
    except:
        return None

# =========================
# REGRESIÓN LINEAL SIMPLE
# =========================
def regresion_lineal(precios):
    n = len(precios)
    if n < 2:
        return precios[-1]

    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(precios) / n

    num = sum((x[i] - x_mean) * (precios[i] - y_mean) for i in range(n))
    den = sum((x[i] - x_mean) ** 2 for i in range(n))

    if den == 0:
        return precios[-1]

    a = num / den
    b = y_mean - a * x_mean

    return a * n + b  # siguiente punto

# =========================
# 1️⃣ DESCARGAR HISTORIAL
# =========================
print("⬇️ Descargando historial.json...")
resp = requests.get(URL_HISTORIAL)
resp.raise_for_status()
data = resp.json()

# =========================
# 2️⃣ LIMPIAR HISTORIAL
# =========================
print("🧹 Limpiando datos...")
historial_limpio = []

for d in data:
    moda = limpiar_numero(d.get("moda"))
    fecha = convertir_fecha(d.get("fecha"))

    if moda is None or fecha is None:
        continue

    historial_limpio.append({
        "producto": d.get("producto"),
        "fecha": fecha,
        "precio": moda
    })

with open(f"{DATA_DIR}/historial_limpio.json", "w", encoding="utf-8") as f:
    json.dump(historial_limpio, f, ensure_ascii=False, indent=2)

# =========================
# 3️⃣ SERIES POR PRODUCTO
# =========================
series = defaultdict(list)

for d in historial_limpio:
    series[d["producto"]].append({
        "fecha": d["fecha"],
        "promedio": d["precio"]  # el dashboard espera "promedio"
    })

for producto in series:
    series[producto].sort(key=lambda x: x["fecha"])

with open(f"{DATA_DIR}/series_productos.json", "w", encoding="utf-8") as f:
    json.dump(series, f, ensure_ascii=False, indent=2)

# =========================
# 4️⃣ TENDENCIAS
# =========================
tendencias = {}

for producto, datos in series.items():
    if len(datos) < 2:
        tendencias[producto] = {"tendencia": "insuficiente"}
        continue

    primero = datos[0]["promedio"]
    ultimo = datos[-1]["promedio"]

    if ultimo > primero:
        t = "sube"
    elif ultimo < primero:
        t = "baja"
    else:
        t = "estable"

    tendencias[producto] = {"tendencia": t}

with open(f"{DATA_DIR}/tendencias.json", "w", encoding="utf-8") as f:
    json.dump(tendencias, f, ensure_ascii=False, indent=2)

# =========================
# 5️⃣ PREDICCIONES
# =========================
predicciones = {}

for producto, datos in series.items():
    if len(datos) < 3:
        continue

    precios = [d["promedio"] for d in datos]
    pred = regresion_lineal(precios)

    predicciones[producto] = {
        "prediccion_proxima": round(pred, 2)
    }

with open(f"{DATA_DIR}/predicciones.json", "w", encoding="utf-8") as f:
    json.dump(predicciones, f, ensure_ascii=False, indent=2)

# =========================
# 6️⃣ ALERTAS
# =========================
alertas = {}

for producto, datos in series.items():
    precios = [d["promedio"] for d in datos]
    if not precios:
        continue

    actual = precios[-1]

    if actual == max(precios):
        alertas[producto] = "📈 Precio en máximo histórico"
    elif actual == min(precios):
        alertas[producto] = "📉 Precio en mínimo histórico"

with open(f"{DATA_DIR}/alertas.json", "w", encoding="utf-8") as f:
    json.dump(alertas, f, ensure_ascii=False, indent=2)

# =========================
# 7️⃣ CONSOLIDAR HISTÓRICOS
# =========================
print("🧩 Consolidando históricos...")
subprocess.run(["python", "consolidar_json.py"], check=True)

print("✅ Pipeline completo generado correctamente")
