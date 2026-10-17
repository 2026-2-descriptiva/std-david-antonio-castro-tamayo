import gzip
import os

import numpy as np
import pandas as pd

def _leer(ruta):
    with gzip.open(ruta, "rt", encoding="utf-8-sig") as f:
        encabezado = f.readline()
    sep = ";" if encabezado.count(";") > encabezado.count(",") else ","
    df = pd.read_csv(ruta, sep=sep, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    return df

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """

    base = os.path.join(os.path.dirname(__file__), '..')
    data = os.path.join(base, 'data')

    partes = []
    for canal, archivo in [
        ("letter", "historical_requests_letter.csv.gz"),
        ("web", "historical_requests_web.csv.gz"),
    ]:
        d = _leer(os.path.join(data, archivo)).drop_duplicates()
        d["channel"] = canal
        partes.append(d)
    df = pd.concat(partes, ignore_index=True)

    df["in_date"] = pd.to_datetime(df["in_date"], errors="coerce").dt.normalize()
    df["out_date"] = pd.to_datetime(df["out_date"], errors="coerce").dt.normalize()

    df["year"] = df["in_date"].dt.year
    df["answered"] = df["out_date"].notna()

    df["calendar_days"] = (df["out_date"] - df["in_date"]).dt.days

    df["business_days"] = np.nan
    r = df["answered"] & df["in_date"].notna()
    uno = np.timedelta64(1, "D")
    inicio = df.loc[r, "in_date"].values.astype("datetime64[D]") + uno
    fin = df.loc[r, "out_date"].values.astype("datetime64[D]") + uno
    df.loc[r, "business_days"] = np.busday_count(inicio, fin)

    df["on_time"] = df["answered"] & (df["business_days"] <= 15)

    channel = (
        df.groupby("channel")
        .agg(
            requests=("channel", "size"),
            answered=("answered", "sum"),
            median_business_days=("business_days", "median"),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
    )
    channel["pending"] = channel["requests"] - channel["answered"]
    channel = channel[
        ["channel", "requests", "answered", "pending",
         "median_business_days", "on_time_rate"]
    ]

    yearly = (
        df.groupby(["year", "channel"])
        .agg(
            requests=("channel", "size"),
            answered=("answered", "sum"),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
    )
    yearly["pending"] = yearly["requests"] - yearly["answered"]
    yearly["year"] = yearly["year"].astype(int)
    yearly = yearly.sort_values(["year", "channel"]).reset_index(drop=True)[
        ["year", "channel", "requests", "pending", "on_time_rate"]
    ]

    df["_dow"] = df["in_date"].dt.dayofweek
    dias = (
        df.groupby("day_name")
        .agg(
            requests=("day_name", "size"),
            median_calendar_days=("calendar_days", "median"),
            median_business_days=("business_days", "median"),
            _dow=("_dow", "min"),
        )
        .reset_index()
        .sort_values("_dow")
        .reset_index(drop=True)[
            ["day_name", "requests", "median_calendar_days",
             "median_business_days"]
        ]
    )

    salida = os.path.join(base, 'submission')
    os.makedirs(salida, exist_ok=True)
    channel.to_csv(os.path.join(salida, 'channel_summary.csv'), index=False)
    yearly.to_csv(os.path.join(salida, 'yearly_summary.csv'), index=False)
    dias.to_csv(os.path.join(salida, 'entry_day_summary.csv'), index=False)

    return channel, yearly, dias
