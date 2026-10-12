def pregunta_09():
    """
    Retorne la tabla `data/tbl0.tsv` completa con una columna adicional
    llamada `year`, al final, que contenga el año de la fecha de la columna
    `c3` como un texto de cuatro caracteres.
    """

    import pandas as pd
    import os

    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'tbl0.tsv'),
        sep="\t",
    )

    data["year"] = data["c3"].str[:4]

    return data
