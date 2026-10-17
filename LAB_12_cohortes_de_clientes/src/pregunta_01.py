import gzip
import os

import matplotlib

matplotlib.use("Agg")  
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    base = os.path.join(os.path.dirname(__file__), '..')
    ruta = os.path.join(base, 'data', 'sales.csv.gz')

    # Detectar el separador mirando el encabezado
    with gzip.open(ruta, "rt", encoding="utf-8-sig") as f:
        encabezado = f.readline()
    sep = ";" if encabezado.count(";") > encabezado.count(",") else ","

    df = pd.read_csv(ruta, sep=sep, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]

    df = df[["CustomerID", "OrderDate"]].copy()
    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
    df = df.dropna(subset=["CustomerID", "OrderDate"])

    # Mes de cada orden y mes de la primera compra de cada cliente
    df["order_month"] = df["OrderDate"].dt.to_period("M")
    df["cohort"] = df.groupby("CustomerID")["order_month"].transform("min")

    # Meses transcurridos desde la cohorte
    df["period_index"] = (
        (df["order_month"].dt.year - df["cohort"].dt.year) * 12
        + (df["order_month"].dt.month - df["cohort"].dt.month)
    ).astype(int)

    # Clientes distintos por cohorte y período
    retention = (
        df.groupby(["cohort", "period_index"])["CustomerID"]
        .nunique()
        .rename("active_customers")
        .reset_index()
    )

    # Tamaño de la cohorte = clientes activos en el período 0
    tamanos = (
        retention[retention["period_index"] == 0]
        .set_index("cohort")["active_customers"]
        .rename("cohort_size")
    )
    retention = retention.merge(tamanos, left_on="cohort", right_index=True)
    retention["retention_rate"] = (
        retention["active_customers"] / retention["cohort_size"]
    )

    retention["cohort_month"] = retention["cohort"].astype(str)
    retention = (
        retention.sort_values(["cohort_month", "period_index"])
        .reset_index(drop=True)[
            ["cohort_month", "period_index", "active_customers",
             "cohort_size", "retention_rate"]
        ]
    )

    # ---------------- Guardar CSV ----------------
    salida = os.path.join(base, 'submission')
    os.makedirs(salida, exist_ok=True)
    retention.to_csv(
        os.path.join(salida, 'cohort_retention.csv'), index=False
    )

    # ---------------- Mapa de calor ----------------
    matriz = retention.pivot(
        index="cohort_month", columns="period_index",
        values="retention_rate",
    )  # los períodos no observados quedan como NaN
    valores = np.ma.masked_invalid(matriz.to_numpy())

    fig, ax = plt.subplots(
        figsize=(
            max(8, 0.7 * matriz.shape[1] + 3),
            max(5, 0.45 * matriz.shape[0] + 2),
        )
    )
    imagen = ax.imshow(valores, cmap="Blues", vmin=0, vmax=1, aspect="auto")

    ax.set_xticks(range(matriz.shape[1]))
    ax.set_xticklabels(matriz.columns)
    ax.set_yticks(range(matriz.shape[0]))
    ax.set_yticklabels(matriz.index)
    ax.set_xlabel("Período (meses desde la primera compra)")
    ax.set_ylabel("Cohorte (mes de la primera compra)")
    ax.set_title("Retención de clientes por cohorte")

    # Porcentajes dentro de las celdas observadas
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            v = matriz.iat[i, j]
            if pd.notna(v):
                ax.text(
                    j, i, f"{v:.0%}", ha="center", va="center",
                    fontsize=8,
                    color="white" if v > 0.6 else "black",
                )

    barra = fig.colorbar(imagen, ax=ax)
    barra.set_label("Tasa de retención")
    barra.ax.yaxis.set_major_formatter(
        matplotlib.ticker.PercentFormatter(xmax=1)
    )

    fig.tight_layout()
    fig.savefig(
        os.path.join(salida, 'cohort_retention_heatmap.png'), dpi=150
    )
    plt.close(fig)

    return retention
