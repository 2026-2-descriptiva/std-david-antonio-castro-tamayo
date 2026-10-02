import pandas as pd
import os
def pregunta_04():
    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv.gz'),
        compression='gzip',
        sep='\t',
        header=None,
        names=['letter', 'value', 'date', 'letters', 'pairs'],
    )
    meses = data['date'].str[5:7]
    conteo = meses.value_counts().sort_index()
    return [(mes, int(n)) for mes, n in conteo.items()]
