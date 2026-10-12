def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        4
    """

    import pandas as pd
    import os
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'tbl0.tsv'), sep="\t")
    columnas = len(data.columns)
    
    return columnas
