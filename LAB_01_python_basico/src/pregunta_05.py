import pandas as pd
import os

def pregunta_05():
    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv.gz'),
        compression='gzip',
        sep='\t',
        header=None,
        names=['letter', 'value', 'date', 'letters', 'pairs'],
    )
    res = data.groupby('letter')['value'].agg(['max', 'min'])
    return [(letra, int(fila['max']), int(fila['min'])) for letra, fila in res.iterrows()]
