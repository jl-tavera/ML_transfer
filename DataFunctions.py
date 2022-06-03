'''
LIBRARIES
'''
from stringprep import in_table_a1
import FBrefScraper as FBref
import pandas as pd
import numpy as np
from collections import Counter


'''
FORMAT FUNCTIONS
'''

def rawDuplicates(string):
    string = string[1:-1]
    string = string.split(',')
    string = list(dict.fromkeys(string))
    value = string[0]
    value = value[1:-1]

    return value

def rawListDuplicates(string):
    lst = string[1:-1]
    lst = lst.split(',')
    lst = list(dict.fromkeys(lst))
    for element in lst:
        if len(element) < 3:
            lst.remove(element)
    no_space = lst[0]
    space = lst[1]

    if no_space in space: 
        lst.remove(space)

    return lst

def formatHREF(lst, min_href):
    format_lst = []
    for href in lst:
        if ' ' in href:
            href = href.replace(' ', '')
        href = href[1:-1]
        format_lst.append(href)

    if min_href in format_lst:
        format_lst.remove(min_href)

    return format_lst

def formatComp(lst):
    col = 0
    if 'Primera A' in lst:
        col = 1

    return col


def formatResult(lst):
    lst = lst[1:-1]
    lst = lst.split(', ')
    total = len(lst)
    avg_goal = 0
    w = 0
    l = 0
    for result in lst:
        result = result[1:-1]
        result = result.split(' ')
        if len(result) == 2:
            if result[0] == 'W':
                goals = result[1].split('–')
                avg_goal += abs(int(goals[0]) - int(goals[1]))
                w +=  1
            
            if result[0] == 'L':
                goals = result[1]
                goals = goals.split('–')
                avg_goal += abs(int(goals[0]) - int(goals[1]))*(-1)
                l += 1
        else: 
            print(result)

    
    avg_goal = round(avg_goal/total, 3) 
    w_percentage = round(w/total , 3)
    l_percentage = round(l/total , 3)

    return (avg_goal, w_percentage, l_percentage)

def formatSquads(lst):
    lst = lst[1:-1]
    lst = lst.split(', ')
    lst = Counter(lst)

    return lst

def formatStart(lst):
    lst = lst[1:-1]
    lst = lst.split(', ')
    total = len(lst)
    i = 0 
    for start in lst: 
        if start[1] == 'Y':
            i += 1
    
    return round(i/total, 3)


def signingsCount(df): 
    cols = df.columns.tolist()

    for col in cols:
        if col != 'Year':

            for i, row in df.iterrows(): 
                count = int(len(row[col]))
                df.at[i, col] = count
        

    df.loc['Total', :] = df.sum().values

    return df

def stdev(lst):
    lst_stat = []
    lst = lst[1:-1]
    lst = lst.split(', ')
    for element in lst:
        if len(element) == 1:
            element = int(element)
            lst_stat.append(element)
        elif len(element) > 2:
            element = int(element[1:-1])
            lst_stat.append(element)
       

    array = np.asarray(lst_stat)
    std = round(np.std(array),3)

    return std

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
                    'Opponent' ], axis = 1)

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

def createRFDF(filename):
    signings = FBref.loadCSV(filename)
    signings = signings.drop(['0'],axis = 1 )
    stat_names = ['Min', 'Gls','Ast','PK','PKatt',
                'Sh','SoT','CrdY','CrdR','Fls',
                'Fld','Off','Crs','TklW','Int',
                'OG','PKwon','PKcon']
    j = 0
    for i, row in signings.iterrows():

        list_name = row['Name']
        list_name = rawDuplicates(list_name)
        signings.at[i, 'Name'] = list_name

        list_team = row['Team']
        list_team = rawDuplicates(list_team)
        signings.at[i, 'Team'] = list_name

        min_href = str(row['min_href'])

        list_teamhref = row['Team_Href']
        list_teamhref = rawListDuplicates(list_teamhref)
        list_teamhref = formatHREF(list_teamhref, min_href)

        list_comp = row['Comp']
        list_comp = formatComp(list_comp)
        signings.at[i, 'Comp'] = list_name

        list_result = row['Result']
        list_result = formatResult(list_result)

        list_squad = row['Squad']
        list_squad = formatSquads(list_squad)

        for stat in stat_names:
            list_stat = row[stat]
            std = stdev(list_stat)
            signings.at[i, stat] = std
            



        
        if len(list_teamhref) > 0:
            
            url = list_teamhref[0]
            pos = FBref.getNormalizedStats(url, list_name, stat_names)
            print(pos)
            j += 1
            print(j)
            print(list_teamhref)
            print(list_name)
            print(row['min_href'])
            
   
            

    return None