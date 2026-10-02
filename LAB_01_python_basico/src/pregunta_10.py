import pandas as pd
import os

def pregunta_10():
    data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv.gz'),
        compression='gzip',
        sep='\t',
        header=None,
        names=['letter', 'value', 'date', 'codes', 'metrics'],
    )
    return [
        (letra, len(codes.split(',')), len(metrics.split(',')))
        for letra, codes, metrics in zip(data['letter'], data['codes'], data['metrics'])
    ]