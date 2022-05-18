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
                count = int(len(row[col]))
                df.at[i, col] = count
        

    df.loc['Total', :] = df.sum().values

    return df