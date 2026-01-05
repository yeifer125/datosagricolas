import json
import glob
from collections import defaultdict
import os

DATA_DIR = "data"

def consolidar(prefijo, salida):
    total = defaultdict(list)

    patron = os.path.join(DATA_DIR, f"{prefijo}_*.json")
    archivos = sorted(glob.glob(patron))

    for archivo in archivos:
        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)

            for clave, valores in data.items():
                # series_productos -> lista
                if isinstance(valores, list):
                    total[clave].extend(valores)
                # alertas / tendencias / predicciones -> dict simple
                else:
                    total[clave] = valores

    # 🔒 Ordenar por fecha si existe
    for clave, valores in total.items():
        if isinstance(valores, list) and "fecha" in valores[0]:
            total[clave] = sorted(valores, key=lambda x: x["fecha"])

    salida_path = os.path.join(DATA_DIR, salida)

    with open(salida_path, "w", encoding="utf-8") as f:
        json.dump(total, f, ensure_ascii=False, indent=2)

    print(f"✅ Generado {salida_path} ({len(archivos)} archivos)")


if __name__ == "__main__":
    consolidar("series_productos", "series_productos.json")
    consolidar("tendencias", "tendencias.json")
    consolidar("predicciones", "predicciones.json")
    consolidar("alertas", "alertas.json")
