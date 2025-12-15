import json
import requests
from datetime import datetime
from collections import defaultdict

# =========================
# CONFIG
# =========================
URL_HISTORIAL = "https://raw.githubusercontent.com/yeifer125/iadatos/main/historial.json"

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
# 1️⃣ DESCARGAR HISTORIAL
# =========================
print("⬇️ Descargando historial.json desde GitHub...")
resp = requests.get(URL_HISTORIAL)
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

with open("historial_limpio.json", "w", encoding="utf-8") as f:
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

# ordenar por fecha
for producto in series:
    series[producto].sort(key=lambda x: x["fecha"])

with open("series_productos.json", "w", encoding="utf-8") as f:
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

with open("tendencias.json", "w", encoding="utf-8") as f:
    json.dump(tendencias, f, ensure_ascii=False, indent=2)

# =========================
# 5️⃣ PREDICCIONES (simple)
# =========================
predicciones = {}

for producto, datos in series.items():
    if len(datos) < 3:
        continue

    diffs = []
    for i in range(1, len(datos)):
        diffs.append(datos[i]["promedio"] - datos[i-1]["promedio"])

    promedio_cambio = sum(diffs) / len(diffs)
    predicciones[producto] = {
        "prediccion_proxima": round(datos[-1]["promedio"] + promedio_cambio, 2)
    }

with open("predicciones.json", "w", encoding="utf-8") as f:
    json.dump(predicciones, f, ensure_ascii=False, indent=2)

# =========================
# 6️⃣ ALERTAS
# =========================
alertas = {}

for producto, datos in series.items():
    precios = [d["promedio"] for d in datos]

    if not precios:
        continue

    max_p = max(precios)
    min_p = min(precios)
    actual = precios[-1]

    if actual == max_p:
        alertas[producto] = "📈 Precio en máximo histórico"
    elif actual == min_p:
        alertas[producto] = "📉 Precio en mínimo histórico"

with open("alertas.json", "w", encoding="utf-8") as f:
    json.dump(alertas, f, ensure_ascii=False, indent=2)

print("✅ Pipeline completo generado correctamente")
