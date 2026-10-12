def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """
    import pandas as pd
    import os
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'tbl0.tsv'), sep="\t")
    registros = len(data)
    
    return registros

    
