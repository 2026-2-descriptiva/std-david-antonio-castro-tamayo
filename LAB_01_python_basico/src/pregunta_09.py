import pandas as pd
import os

def pregunta_09():
    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv.gz'),
        compression='gzip',
        sep='\t',
        header=None,
        names=['letter', 'value', 'date', 'codes', 'metrics'],
    )
    claves = data['metrics'].str.split(',').explode().str.split(':').str[0]
    conteo = claves.value_counts().sort_index()
    return {clave: int(n) for clave, n in conteo.items()}