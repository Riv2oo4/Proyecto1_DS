import pandas as pd
import os

# Carpeta con los archivos CSV
carpeta_datos = "./Datos"
archivos = [f for f in os.listdir(carpeta_datos) if f.endswith(".csv")]

# Carpeta de salida para los archivos Excel
os.makedirs("ReportesExcel", exist_ok=True)

for nombre_archivo in archivos:
    ruta = os.path.join(carpeta_datos, nombre_archivo)
    salida_excel = f"./ReportesExcel/resumen_{nombre_archivo.replace('.csv', '')}.xlsx"

    try:
        # Leer archivo como texto para buscar línea con encabezados
        with open(ruta, "r", encoding="latin1") as f:
            lineas = f.readlines()

        linea_encabezado = None
        for i, linea in enumerate(lineas):
            if "CODIGO" in linea and "ESTABLECIMIENTO" in linea:
                linea_encabezado = i
                break

        if linea_encabezado is None:
            print(f"Encabezado no encontrado en {nombre_archivo}")
            continue

        # Leer CSV desde la línea de encabezado encontrada
        df = pd.read_csv(ruta, sep=";", encoding="latin1", skiprows=linea_encabezado)

        # Exportar todo el DataFrame a Excel
        df.to_excel(salida_excel, index=False, sheet_name="DatosCompletos")

        print(f"Exportado completo: {nombre_archivo} → {salida_excel}")

    except Exception as e:
        print(f"Error procesando {nombre_archivo}: {e}")
