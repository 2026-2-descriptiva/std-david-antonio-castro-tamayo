import pandas as pd
import os


def pregunta_02():
    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv.gz'),
        compression='gzip',
        sep='\t',
        header=None,
        names=['letter', 'value', 'date', 'letters', 'pairs'],
    )
    conteo = data['letter'].value_counts().sort_index()
    return list(conteo.items())