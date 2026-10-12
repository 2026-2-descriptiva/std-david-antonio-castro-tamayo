def pregunta_10():
    """
    Usando `data/tbl0.tsv`, construya para cada categoría de la columna `c1`
    un texto con todos sus valores de la columna `c2`, ordenados de menor a
    mayor y separados por `:`. Retorne un DataFrame cuyo índice son las
    categorías, en orden alfabético, con una única columna llamada `c2`.
    """

    import pandas as pd
    import os

    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'tbl0.tsv'),
        sep="\t",
    )

    return (
        data.groupby("c1")["c2"]
        .apply(lambda x: ":".join(str(v) for v in sorted(x)))
        .to_frame()
    )
