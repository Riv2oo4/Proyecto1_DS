import pandas as pd
import re

# Ruta del archivo
ruta = "./establecimiento.csv"
salida_txt = "./reporte_datos_desalineados.txt"

# Leer las líneas
with open(ruta, "r", encoding="latin1") as f:
    lineas = [line.strip().strip('"') for line in f if line.strip()]

# Buscar encabezados reales
linea_encabezado = None
for i, linea in enumerate(lineas):
    if "CODIGO" in linea and "ESTABLECIMIENTO" in linea:
        linea_encabezado = i
        break

if linea_encabezado is None:
    raise ValueError("No se encontró la línea de encabezados.")

# Separar encabezados por espacios múltiples
columnas = re.split(r"\s{2,}", lineas[linea_encabezado])

# Preparar archivo de salida
with open(salida_txt, "w", encoding="utf-8") as f_out:
    # f_out.write("==== FILAS DESALINEADAS ====\n\n")

    datos = []
    for linea in lineas[linea_encabezado + 1:]:
        fila = re.split(r"\s{2,}", linea)
        if len(fila) == len(columnas):
            datos.append(fila)

    # Crear DataFrame
    df = pd.DataFrame(datos, columns=columnas)
    f_out.write("\n==== PRIMERAS FILAS DEL DATAFRAME ====\n\n")
    # Ver las primeras filas
    f_out.write(df.head().to_string())

