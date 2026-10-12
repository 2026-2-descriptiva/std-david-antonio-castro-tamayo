def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.
    """

    import pandas as pd
    import os

    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'tbl1.tsv'),
        sep="\t",
    )

    return sorted(data["c4"].str.upper().unique())
