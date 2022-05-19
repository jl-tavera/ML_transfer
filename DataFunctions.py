'''
LIBRARIES
'''
from stringprep import in_table_a1
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
                    'Round', 'Venue', 'Day',
                    'CrdY', 'CrdR', 'Opponent' ], axis = 1)

    df = df.fillna(0)   
    df['min_href'] = 0
    df_ML = []

   
    for name in signings_names:
        print(name)
        player_info = {}
        found_player = False
        for i, col in enumerate(df.columns.tolist()):
            player_info[col] = []

        for i, row in df.iterrows():
            if row['Name'] == name:
                found_player = True
                if row['Team'] in row['Squad']:
                    min_href = row['Team_Href']
                else:
                    for i, col in enumerate(df.columns.tolist()):
                        stat = player_info[col]
                        stat.append(row[col])
                        player_info[col] = stat

            if row['Name'] != name and found_player == True:
                break

        if len(player_info['Team']) > 1:
            player_info['min_href'] = min_href 
            df_ML.append(player_info)

    df_ML = pd.DataFrame(df_ML)
    return df_ML

