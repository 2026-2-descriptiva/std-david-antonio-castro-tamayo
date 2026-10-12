def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    import os
    import re
    import pandas as pd

    ruta = os.path.join(
        os.path.dirname(__file__), '..', 'data', 'clusters_report.txt'
    )

    patron = re.compile(r"^(\d+)\s+(\d+)\s+(\d+(?:[.,]\d+)?)\s*%\s*(.*)$")

    registros = []
    actual = None

    with open(ruta, encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            coincidencia = patron.match(linea)

            if coincidencia:
                actual = {
                    "cluster": int(coincidencia.group(1)),
                    "cantidad_de_palabras_clave": int(coincidencia.group(2)),
                    "porcentaje_de_palabras_clave": float(
                        coincidencia.group(3).replace(",", ".")
                    ),
                    "texto": [coincidencia.group(4)],
                }
                registros.append(actual)
            elif actual is not None and linea and not set(linea) <= set("-= "):
                actual["texto"].append(linea)

    for registro in registros:
        texto = " ".join(registro.pop("texto"))
        texto = re.sub(r"\s+", " ", texto).strip().rstrip(".")
        palabras = [p.strip() for p in texto.split(",") if p.strip()]
        registro["principales_palabras_clave"] = ", ".join(palabras)

    return pd.DataFrame(registros)
