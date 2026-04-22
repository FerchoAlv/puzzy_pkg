from pathlib import Path
import csv




dir_salida = Path.home() / "ros2_ws" / "src" / "puzzy_pkg" / "data_2"
dir_salida.mkdir(parents=True, exist_ok=True)

ruta_salida = dir_salida / "datos_1.csv"

W = [[0,1]]
with open(ruta_salida, "w", newline="", encoding="utf-8") as f: 
    writer = csv.writer(f)
    writer.writerows(W)