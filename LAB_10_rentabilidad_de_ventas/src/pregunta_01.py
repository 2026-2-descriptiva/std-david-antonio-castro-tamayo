import pandas as pd
import os

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    base = os.path.join(os.path.dirname(__file__), '..')
    df = pd.read_csv(
      os.path.join(base, 'data', 'superstore_orders.csv.gz'),
      sep=";",
      decimal=",",
      encoding="utf-8-sig",
    )
    df.columns = [c.strip() for c in df.columns]


    df["is_loss"] = df["Profit"] < 0
    df["loss"] = (-df["Profit"]).where(df["is_loss"], 0.0)

    df["discount_band"] = pd.cut(
        df["Discount"],
        bins=[float("-inf"), 0, 0.05, 0.10, float("inf")],
        labels=["0%", "1%-5%", "6%-10%", "más de 10%"],
    )

    def agregar(grupos, con_pedidos=False):
        """Calcula las métricas comunes y las redondea."""
        reglas = dict(
            lines=("Order ID", "size"),
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            loss_lines=("is_loss", "sum"),
            lost_profit=("loss", "sum"),
        )
        if con_pedidos:
            reglas["orders"] = ("Order ID", "nunique")

        r = grupos.agg(**reglas)
        r["profit_margin"] = r["profit"] / r["sales"]
        r["loss_line_rate"] = r["loss_lines"] / r["lines"]

        r["sales"] = r["sales"].round(2)
        r["profit"] = r["profit"].round(4)
        r["lost_profit"] = r["lost_profit"].round(4)
        r["profit_margin"] = r["profit_margin"].round(4)
        r["loss_line_rate"] = r["loss_line_rate"].round(4)
        return r

    resumen = agregar(df.assign(_k=1).groupby("_k"), con_pedidos=True)
    profitability = resumen.reset_index(drop=True)[
        ["lines", "orders", "sales", "profit", "profit_margin",
         "loss_lines", "loss_line_rate", "lost_profit"]
    ]

    discount = agregar(
        df.groupby("discount_band", observed=False)
    ).reset_index()[
        ["discount_band", "lines", "sales", "profit", "profit_margin",
         "loss_line_rate", "lost_profit"]
    ]
    discount["discount_band"] = discount["discount_band"].astype(str)

    por_segmento = agregar(
        df.groupby(["Customer Segment", "Product Category"])
    ).reset_index()
    priority = (
        por_segmento[por_segmento["lines"] >= 100]
        .sort_values("lost_profit", ascending=False)
        .head(5)
        .reset_index(drop=True)[
            ["Customer Segment", "Product Category", "lines", "sales",
             "profit", "profit_margin", "lost_profit"]
        ]
    )

    salida = os.path.join(base, 'submission')
    os.makedirs(salida, exist_ok=True)
    profitability.to_csv(
        os.path.join(salida, 'profitability_summary.csv'), index=False
    )
    discount.to_csv(
        os.path.join(salida, 'discount_summary.csv'), index=False
    )
    priority.to_csv(
        os.path.join(salida, 'priority_segments.csv'), index=False
    )

    return profitability, discount, priority
