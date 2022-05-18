'''
LIBRARIES
'''

import pandas as pd
import numpy as np

def signingsCount(df): 
    cols = df.columns.tolist()
    for col in cols:
        if col != 'Year':
            for i, row in df.iterrows(): 
                df.at[i, col] = len(row[col])
    df.append(df.sum(numeric_only=True), ignore_index=True)
    
    return df