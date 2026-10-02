import pandas as pd
import os

def pregunta_12():
    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv.gz'),
        compression='gzip',
        sep='\t',
        header=None,
        names=['letter', 'value', 'date', 'codes', 'metrics'],
    )
    df = data[['letter', 'metrics']].copy()
    df['metrics'] = df['metrics'].str.split(',')
    df = df.explode('metrics')
    df['num'] = df['metrics'].str.split(':').str[1].astype(int)
    suma = df.groupby('letter')['num'].sum()
    return {letra: int(total) for letra, total in suma.items()}
