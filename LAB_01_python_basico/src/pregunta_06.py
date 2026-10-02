import pandas as pd
import os

def pregunta_06():
    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv.gz'),
        compression='gzip',
        sep='\t',
        header=None,
        names=['letter', 'value', 'date', 'letters', 'metrics'],
    )
    pares = data['metrics'].str.split(',').explode().str.split(':', expand=True)
    pares.columns = ['clave', 'valor']
    pares['valor'] = pares['valor'].astype(int)
    res = pares.groupby('clave')['valor'].agg(['min', 'max'])
    return [(clave, int(fila['min']), int(fila['max'])) for clave, fila in res.iterrows()]
