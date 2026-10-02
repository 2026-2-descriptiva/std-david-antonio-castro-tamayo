import pandas as pd
import os

def pregunta_11():
    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv.gz'),
        compression='gzip',
        sep='\t',
        header=None,
        names=['letter', 'value', 'date', 'codes', 'metrics'],
    )
    df = data[['codes', 'value']].copy()
    df['codes'] = df['codes'].str.split(',')
    df = df.explode('codes')
    suma = df.groupby('codes')['value'].sum()
    return {letra: int(total) for letra, total in suma.items()}
