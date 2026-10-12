def pregunta_03():
    """
    Usando `data/tbl0.tsv`, cuente cuántos registros hay para cada categoría
    de la columna `c1`. Retorne una Serie de Pandas cuyo índice son las
    categorías, en orden alfabético, y cuyos valores son las cantidades.
    """

    import pandas as pd
    import os

    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'tbl0.tsv'),
        sep="\t",
    )

    return data["c1"].value_counts().sort_index()