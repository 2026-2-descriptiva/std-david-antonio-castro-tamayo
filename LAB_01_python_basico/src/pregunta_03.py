import pandas as pd
import os

def pregunta_03():
    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv.gz'),
        compression='gzip',
        sep='\t',
        header=None,
        names=['letter', 'value', 'date', 'letters', 'pairs'],
    )
    suma = data.groupby('letter')['value'].sum()
    return [(letra, int(total)) for letra, total in suma.items()]
