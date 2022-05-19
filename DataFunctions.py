'''
LIBRARIES
'''
import FBrefScraper as FBref
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

def completeRawData(filename):
    signings = FBref.loadCSV(filename)
    colnames = signings.columns.tolist()
    colnames = colnames[1:]
    for i,col in enumerate(colnames):
        if 'La ' in col: 
            col = col.replace('La ', '')
        if ' ' in col:
            col = col.replace(' ', '')
        if 'á' in col: 
            col = col.replace('á', 'a')

        df_name = '/teams/' + str(col) + '.csv'
        df_team = FBref.loadCSV(df_name)

        if i == 0:
            df = df_team

        df_team.columns = df_team.iloc[0]
        df_team = df_team.reset_index(drop=True)

        df = df.append(df_team, ignore_index=True)
        df = df.reset_index(drop=True)
    
    
    teams_href = df['Team_Href'].unique()
    signings_names = df['Name'].unique()

    df = df.drop(['Match Report','Date',
                    'Round', 'Venue' ], axis = 1)

    df_ML = pd.DataFrame
    df_ML.columns = df.columns 
   
    for name in signings_names:
        for i, row in df.iterrows:
            if row['Name'] == name:
                min = 0
                if row['Team'] == row['Squad']:
                    min += row['Min']



    return len(teams_href)