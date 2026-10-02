import pandas as pd
import os

def pregunta_01():
    """
    
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """
    
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv.gz'), compression='gzip', sep='\t', header=None)
    suma = data[1].sum()   # la segunda columna es el índice 1
    
    return suma
