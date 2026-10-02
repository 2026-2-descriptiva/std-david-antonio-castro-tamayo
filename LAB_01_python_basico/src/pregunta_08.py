import pandas as pd
import os

def pregunta_08():
    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv.gz'),
        compression='gzip',
        sep='\t',
        header=None,
        names=['letter', 'value', 'date', 'codes', 'metrics'],
    )
    res = data.groupby('value')['letter'].apply(lambda s: sorted(set(s)))
    return [(int(valor), letras) for valor, letras in res.items()]
