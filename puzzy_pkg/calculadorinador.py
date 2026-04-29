import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
from pathlib import Path

carpeta = "/home/rucardo/ros2_ws/src/puzzy_pkg/data/data_piso_0.1"

ruta_salida_datos = "/home/rucardo/ros2_ws/src/puzzy_pkg/data_procesado/data_piso_cova.csv"



covis = []

cov11 = []
cov12 = []
cov21 = []
cov22 = []



def promi(carpeta):
    suma_cov = None
    contador = 0

    for archivo in sorted(os.listdir(carpeta)):
        if archivo.endswith(".csv"):
            ruta = os.path.join(carpeta, archivo)
            
            df = pd.read_csv(ruta, header=None)
            df.columns = ['x', 'y']
            datos = df[['x', 'y']].dropna()

            datos = datos.iloc[25:]
            
            cov = np.cov(datos.to_numpy(), rowvar=False)
            
            # Inicializar o acumular
            if suma_cov is None:
                suma_cov = cov
            else:
                suma_cov += cov
            
            contador += 1

    # Promedio final
    if contador > 0:
        promedio_cov = suma_cov / contador
        print("\nMatriz de covarianza promedio:")
        print(promedio_cov)
    else:
        print("No se pudieron procesar archivos válidos")
    return promedio_cov

for i in range(5):
    carpeta  = carpeta[:-1]+ str(i+1)
    covis.append(promi(carpeta))

print("----------------------------------------------------")

for covi in covis:
    cov11.append(covi[0][0])
    cov12.append(covi[0][1])
    cov21.append(covi[1][0])
    cov22.append(covi[1][1])

x = [0.1/0.0505, 0.2/0.0505, 0.3/0.0505, 0.4/0.0505, 0.5/0.0505]

covaricovari = np.column_stack((x, cov11, cov12,cov21, cov22))
with open(ruta_salida_datos, "w", newline="", encoding="utf=8") as f:
    writer = csv.writer(f)
    writer.writerows(covaricovari)

fig = go.Figure()

fig.add_trace(go.Scatter(x=x, y=cov11, mode='lines+markers', name='cov11'))
fig.add_trace(go.Scatter(x=x, y=cov12, mode='lines+markers', name='cov12'))
fig.add_trace(go.Scatter(x=x, y=cov21, mode='lines+markers', name='cov21'))
fig.add_trace(go.Scatter(x=x, y=cov22, mode='lines+markers', name='cov22'))

fig.update_layout(
    title="w vs cov",
    xaxis_title="w",
    yaxis_title="covs"
)

fig.show()
    



