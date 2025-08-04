import pandas as pd

def limpiar_csv_con_encabezado_dinamico(ruta_archivo):
    with open(ruta_archivo, encoding='utf-8', errors='ignore') as f:
        lineas = f.readlines()

    # Buscar línea de encabezado real
    inicio_datos = None
    for i, linea in enumerate(lineas):
        if "CODIGO;;DISTRITO;DEPARTAMENTO;MUNICIPIO;ESTABLECIMIENTO" in linea:
            inicio_datos = i
            break

    if inicio_datos is None:
        raise ValueError("No se encontró la línea de encabezado real.")

    #  Buscar final del archivo
    fin_datos = None
    for j in range(len(lineas) - 1, 0, -1):
        if "Ministerio de Educaci" in lineas[j]:
            fin_datos = j
            break

    if fin_datos is None:
        raise ValueError("No se encontró la línea final con 'Ministerio de Educación'.")

    # Extraer solo las líneas válidas
    lineas_validas = lineas[inicio_datos:fin_datos]

    from io import StringIO
    contenido_limpio = StringIO("".join(lineas_validas))
    df = pd.read_csv(contenido_limpio, sep=";", engine="python")

    df = df.dropna(axis=1, how='all')

    return df

ruta = "./Datos/AltaVerapaz.csv"  
df_limpio = limpiar_csv_con_encabezado_dinamico(ruta)


import pandas as pd
import os

carpeta_datos = "./Datos"
archivos = [f for f in os.listdir(carpeta_datos) if f.endswith(".csv")]
dataframes = []

os.makedirs("ReportesExcel", exist_ok=True)

for nombre_archivo in archivos:
    ruta = os.path.join(carpeta_datos, nombre_archivo)
    try:
        df = limpiar_csv_con_encabezado_dinamico(ruta)
        df["ARCHIVO_ORIGEN"] = nombre_archivo 
        dataframes.append(df)
        print(f"Procesado: {nombre_archivo}")
    except Exception as e:
        print(f"Error en {nombre_archivo}: {e}")

# Unificar todos en uno solo
df_unificado = pd.concat(dataframes, ignore_index=True)

# Guardar en un solo archivo Excel
os.makedirs("ReportesExcel", exist_ok=True)
df_unificado.to_excel("./ReportesExcel/TodosUnificados.xlsx", index=False)

print("\nArchivo final generado: ReportesExcel/TodosUnificados.xlsx")
