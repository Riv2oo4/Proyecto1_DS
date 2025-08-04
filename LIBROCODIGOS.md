# Libro de Códigos

## 1. Descripción general del conjunto de datos

**Fuente de los datos:** MINEDUC–Guatemala

**Contexto y propósito de la recolección:**
Reunir los registros de todos los establecimientos educativos de Guatemala, distribuidos en 23 archivos CSV departamentales, para aplicar una limpieza estandarizada y generar un único archivo unificado (`TodosUnificados.xlsx`) que facilite análisis posteriores y garantice trazabilidad.

---

## 2. Listado de variables

| Nombre de la variable | Etiqueta / Descripción                                                 | Tipo de dato   | Valores posibles                                                                         | Códigos de valores faltantes |
| --------------------- | ---------------------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------- | ---------------------------- |
| `CODIGO`              | Código oficial del establecimiento educativo (formato `NN-NN-NNNN-NN`) | Texto (string) | Cadenas de 14 caracteres con dígitos y guiones, e.g. `03-01-0052-46`                     | `NaN`                        |
| `DISTRITO`            | Código del distrito educativo                                          | Texto (string) | Códigos de 6 caracteres (`NN-NNN`), e.g. `03-001`, `03-002`                              | `NaN`                        |
| `DEPARTAMENTO`        | Nombre del departamento                                                | Texto (string) | 22 departamentos oficiales: `Alta Verapaz`, `Guatemala`, …                               | `NaN`                        |
| `MUNICIPIO`           | Nombre del municipio dentro del departamento                           | Texto (string) | Todos los municipios oficiales por departamento, e.g. `Antigua Guatemala`, `Totonicapán` | `NaN`                        |
| `ESTABLECIMIENTO`     | Nombre oficial del centro educativo                                    | Texto (string) | Texto libre (puede incluir siglas, comillas, apóstrofes)                                 | `NaN`                        |
| `DIRECCION`           | Dirección física (calle, avenida, km, finca, colonia…)                 | Texto (string) | Texto libre, e.g. `5A. CALLE ORIENTE NO.17`, `KM. 2 Salida a Sta. María de Jesús`        | `NaN`                        |
| `TELEFONO`            | Teléfono de contacto                                                   | Texto (string) | Solo dígitos (7–8 dígitos), e.g. `78328708`, `58437849`                                  | `NaN`                        |
| `SUPERVISOR`          | Nombre completo del supervisor a cargo                                 | Texto (string) | Texto libre; en algunos casos `"---"` indica dato faltante                               | `NaN`, `"---"`               |
| `DIRECTOR`            | Nombre completo del director del centro                                | Texto (string) | Texto libre; `"---"` para faltantes                                                      | `NaN`, `"---"`               |
| `NIVEL`               | Nivel educativo que imparte                                            | Texto (string) | `DIVERSIFICADO`                                                                          | `NaN`                        |
| `SECTOR`              | Tipo de gestión del centro                                             | Texto (string) | `OFICIAL`, `PRIVADO`                                                                     | `NaN`                        |
| `AREA`                | Clasificación urbano/rural                                             | Texto (string) | `URBANA`, `RURAL`                                                                        | `NaN`                        |
| `STATUS`              | Estado operativo                                                       | Texto (string) | `ABIERTA`, `CERRADA TEMPORALMENTE`, `CERRADA DEFINITIVAMENTE`                            | `NaN`                        |
| `MODALIDAD`           | Modalidad de enseñanza                                                 | Texto (string) | `MONOLINGUE`, `BILINGUE`                                                                 | `NaN`                        |
| `JORNADA`             | Jornada o turno de clases                                              | Texto (string) | `MATUTINA`, `VESPERTINA`, `NOCTURNA`, `DOBLE`, `FIN DE SEMANA`                           | `NaN`                        |
| `PLAN`                | Régimen o plan de estudios                                             | Texto (string) | `DIARIO(REGULAR)`, `SABATINO`, `SEMIPRESENCIAL`, `FIN DE SEMANA`                         | `NaN`                        |
| `DEPARTAMENTAL`       | Departamento que originó el archivo CSV                                | Texto (string) | Mismos valores que `DEPARTAMENTO`                                                        | `NaN`                        |
| `ARCHIVO_ORIGEN`      | Nombre del archivo CSV de procedencia                                  | Texto (string) | `sacatepequez.csv`, `guatemala.csv`, …                                                   | `NaN`                        |

---

## 3. Transformaciones y limpieza aplicada

```python
import pandas as pd
import os
from io import StringIO

def limpiar_csv_con_encabezado_dinamico(ruta):
    # 1) Leer todas las líneas, ignorar errores de encoding
    with open(ruta, encoding='utf-8', errors='ignore') as f:
        lineas = f.readlines()
    # 2) Detectar inicio real del encabezado
    for i, ln in enumerate(lineas):
        if "CODIGO;;DISTRITO;DEPARTAMENTO;MUNICIPIO;ESTABLECIMIENTO" in ln:
            inicio = i
            break
    # 3) Detectar fin del bloque de datos
    for j in range(len(lineas)-1, -1, -1):
        if "Ministerio de Educaci" in lineas[j]:
            fin = j
            break
    # 4) Extraer líneas válidas y parsear con pandas
    bloque = "".join(lineas[inicio:fin])
    df = pd.read_csv(StringIO(bloque), sep=";", engine="python")
    # 5) Eliminar columnas completamente vacías
    df.dropna(axis=1, how='all', inplace=True)
    return df

# 6) Procesar todos los CSV de la carpeta Datos
dataframes = []
for archivo in os.listdir("./Datos"):
    if archivo.endswith(".csv"):
        df = limpiar_csv_con_encabezado_dinamico(f"./Datos/{archivo}")
        df["ARCHIVO_ORIGEN"] = archivo
        dataframes.append(df)

# 7) Concatenar y exportar
df_unificado = pd.concat(dataframes, ignore_index=True)
df_unificado.to_excel("ReportesExcel/TodosUnificados.xlsx", index=False)
```

**Operaciones registradas y justificación:**

1. **Filtrado de metadatos:** se remueven líneas previas al encabezado falso y posteriores al pie de página (“Ministerio de Educación”) para garantizar solo datos útiles.
2. **Lectura dinámica:** `StringIO` permite pasar el bloque extraído directamente a `pd.read_csv()`, evitando guardar archivos intermedios.
3. **Eliminación de columnas vacías:** `dropna(axis=1, how='all')` optimiza memoria y estructura.
4. **Trazabilidad:** se añade `ARCHIVO_ORIGEN` para auditar el origen de cada registro.
5. **Unificación:** se concatenan los 23 DataFrames en uno solo, facilitando análisis global.

---

## 4. Variables derivadas o creadas

| Variable         | Definición                                            | Regla / Fórmula                         |
| ---------------- | ----------------------------------------------------- | --------------------------------------- |
| `ARCHIVO_ORIGEN` | Indica el archivo CSV del cual proviene cada registro | `df["ARCHIVO_ORIGEN"] = nombre_archivo` |

---

## 5. Referencias y anexos

* **Script de limpieza:** `filtro.py`
* **Fuente de datos original:** Plataforma de establecimientos de MINEDUC–Guatemala (
* **Archivo unificado resultante:** `ReportesExcel/TodosUnificados.xlsx`
