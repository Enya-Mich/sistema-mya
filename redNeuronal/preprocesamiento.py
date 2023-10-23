import pandas as pd
import numpy as np

def load_data(filepath):
    return pd.read_csv(filepath,delimiter=';')

def preprocess_data(df):
    
    print(df.columns)
    for column in ['u_ubicacion', 'clima', 'estacion', 'riesgo', 't_tramo']:
        df[column] = df[column].astype(float)
    
    df['h_inicio'] = df['h_inicio'].apply(lambda x: x.split(':')[:2])
    df['h_ultimo'] = df['h_ultimo'].apply(lambda x: x.split(':')[:2])
    df['h_inicio'] = df['h_inicio'].apply(lambda x: int(''.join(x)))
    df['h_ultimo'] = df['h_ultimo'].apply(lambda x: int(''.join(x)))
    df = df.astype(np.float32)
    
    return df
