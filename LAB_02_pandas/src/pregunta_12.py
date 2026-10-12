def pregunta_12():
    """
    En `data/tbl2.tsv`, cada valor de la columna `c0` aparece en varias
    filas. Construya un DataFrame con una fila por cada valor de `c0`, en
    orden ascendente, y las columnas `c0` y `c5`. En `c5`, forme un texto
    `c5a:c5b` para cada fila de ese `c0`, ordene esos textos alfabéticamente y
    únalos separados por comas.
    """

    import pandas as pd
    import os

    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'tbl2.tsv'),
        sep="\t",
    )

    data["c5"] = data["c5a"] + ":" + data["c5b"].astype(str)

    return (
        data.groupby("c0")["c5"]
        .apply(lambda x: ",".join(sorted(x)))
        .reset_index()
    )
