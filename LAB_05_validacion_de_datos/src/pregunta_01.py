def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

    import json
    import math
    import os
    import re
    import pandas as pd

    base = os.path.join(os.path.dirname(__file__), '..')
    ruta = os.path.join(base, 'data', 'ventas.csv.gz')

    requeridas = [
        "supplier_id", "supplier", "country", "city", "purchase_date",
        "amount", "discount", "weight", "units", "unit_price",
        "contact_email",
    ]

    df = pd.read_csv(
        ruta,
        dtype=str,
        keep_default_na=False,
        na_filter=False,
        encoding="utf-8-sig",
    )

    df.columns = [
        re.sub(r"\s+", "_", c.replace("\ufeff", "").strip().lower())
        for c in df.columns
    ]

    columnas = list(df.columns)

    def es_faltante(valor):
        v = valor.strip()
        return v == "" or v == "N/A"

    faltantes = {
        c: int(sum(es_faltante(v) for v in df[c])) for c in columnas
    }

    filas_duplicadas = int(df.duplicated().sum())

    filas_id_repetido = 0
    if "supplier_id" in df.columns:
        ids = df.loc[~df["supplier_id"].map(es_faltante), "supplier_id"]
        filas_id_repetido = int(ids.duplicated(keep=False).sum())

    patron_email = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    emails_invalidos = 0
    if "contact_email" in df.columns:
        emails_invalidos = int(
            sum(not patron_email.match(v) for v in df["contact_email"])
        )

    unidades_invalidas = 0
    if "units" in df.columns:
        for v in df["units"]:
            if es_faltante(v):
                continue
            try:
                numero = float(v)
            except ValueError:
                continue 
            if not math.isfinite(numero):
                continue
            if numero <= 0 or numero != int(numero):
                unidades_invalidas += 1

    paises = []
    if "country" in df.columns:
        paises = sorted(df["country"].unique().tolist())

    reporte = {
        "row_count": int(len(df)),
        "column_count": int(len(columnas)),
        "missing_required_columns": sorted(
            c for c in requeridas if c not in columnas
        ),
        "unexpected_columns": sorted(
            c for c in columnas if c not in requeridas
        ),
        "duplicate_row_count": filas_duplicadas,
        "duplicate_supplier_id_row_count": filas_id_repetido,
        "missing_value_count_by_column": faltantes,
        "invalid_email_count": emails_invalidos,
        "invalid_unit_count": int(unidades_invalidas),
        "country_values": paises,
    }

    salida = os.path.join(base, 'submission')
    os.makedirs(salida, exist_ok=True)
    with open(
        os.path.join(salida, 'data_quality_report.json'),
        "w",
        encoding="utf-8",
    ) as archivo:
        json.dump(reporte, archivo, ensure_ascii=False, indent=2)

    return reporte
