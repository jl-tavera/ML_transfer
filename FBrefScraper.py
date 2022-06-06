'''
WEB SCRAPING FUNCTIONS FOR FBREF
'''

'''
LIBRARIES
'''

from random import randint
from time import sleep

from cgitb import html
from tabnanny import check
# from typing import final
import requests
from bs4 import BeautifulSoup
from soupsieve import match
import numpy as np
from tables import Col
import config as cf
import pandas as pd


'''
LOADING FUNCTIONS
'''
def loadCSV(name):

    route = cf.export_dir.replace('/App', '') + name
    csv = pd.read_csv(route)

    return csv

def loadCleanCSV(name):

    route = cf.clean_export_dir.replace('/App', '') + name
    csv = pd.read_csv(route)

    return csv

'''
FORMAT FUNCTIONS
'''

def formatLinks(links):
    links = links.split(',')
    links = links[:-1]

    return links

def formatHREF(href):
    href = href[0]
    href = 'https://www.fbref.com/' + str(href['href'])
    return href

def formatList(lst,n):
    lst2 = []
    j = len(lst)//n
    lst = np.array_split(lst, j)
    for chunk in lst:
        lst2.append(chunk.tolist())

    return lst2


def formatMRSTeam(squads, final_stats):
    stats_dict = {}
    squad_1 = {}
    squad_2 = {}
    
    final_stats = formatList(final_stats, 3)

    for i,stat in enumerate(final_stats):
        
        stat_type = stat[1]
        squad_1[stat_type] = stat[0]
        squad_2[stat_type] = stat[2]

    stats_dict[squads[0]] = squad_1
    stats_dict[squads[1]] = squad_2

    return stats_dict

def formatMinutes(mins):
    if ',' in mins:
        mins = mins.replace(',','')
        if len(mins) ==0:
            mins = 0

    return int(mins)

def createStatsDict(stats_names):
    dict = {}
    for stat in stats_names:
        dict[stat] = [] 

    return dict

def formatStat(stat):
    all_stats = True
    if stat != '':
        stat = int(stat)
    else:
        all_stats = False

    return stat, all_stats

def updateDict(dict, key, value):
    lst = dict[key]
    lst.append(value)
    dict[key] = lst

    return dict


def normalizedStats(player_dict, stats_dict):
    all_stats = True
    for stat in stats_dict:
        avg = 0
        if len(stats_dict[stat]) > 0:
            
            for element in stats_dict[stat]:
                if type(element) == int:
                    avg += element
                else: 
                    all_stats = False
                    break
            if avg != 0 and all_stats == True:
                avg = avg/len(stats_dict[stat])
                avg = round((player_dict[stat][0])/avg, 3) 
            elif avg == 0 and all_stats == True:
                avg = 0.00001
            
        player_dict[stat] = avg
    
    return player_dict, all_stats
        
def groupMin(player_min, max_min, total_mins):
    lst3_size = len(total_mins)//4  
    min_norm = round(player_min/max_min, 3)

    group = 4
    for  i,value in enumerate(total_mins):
        if player_min == value:
            if i <= lst3_size:
                group = 1
            elif i > lst3_size and i<= (lst3_size*2):
                group = 2
            elif i > (lst3_size*2) and i<= (lst3_size*3):
                group = 3
    
    return group, min_norm



'''
FILTER FUNCTIONS
'''
def getATeams(squads_seasons): 
    squads = []
    teams_A = []
    for year in squads_seasons: 
        teams = (squads_seasons[year]).keys()
        for team in teams: 
            teams_A.append(team)

    for team in teams_A: 
        if teams_A.count(team) == 6:
            squads.append(team)
    squads =list(dict.fromkeys(squads))


    return squads

def filterSquads(squads_seasons, ATeams):
    filter_squads = {}
    for squad in ATeams:
        squad_years = {}
        for year in squads_seasons:
            dicc = squads_seasons[year]
            href = dicc[squad]
            squad_years[year] = href
        filter_squads[squad] = squad_years

    return filter_squads

def filterSignings(players):
    signings = {}
    for squad in players: 
        squad_signings = {}
        for year in players[squad]:
            squad_year_signings = ''
            if int(year) > 2016: 
                players_year = (players[squad][year]).keys()
                players_year_p = (players[squad][str(int(year) - 1)]).keys()
                for player in players_year:
                    if player not in players_year_p: 
                        squad_year_signings += players[squad][year][player] + ','
                squad_signings[year] = squad_year_signings
        signings[squad] = squad_signings

    signings = pd.DataFrame(signings)

    return signings

'''
SCRAPING FUNCTIONS
'''

def getSeasons(url): 
    seasons = {}
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')
    table = soup.find('table', id='seasons')
    for row in table.tbody.find_all('tr'):    
        columns = row.find_all('th')
        if(columns != []):
            season = columns[0].text.strip()
            seasonHREF = columns[0].find_all('a', href=True)
            seasonHREF = formatHREF(seasonHREF)
        seasons[season] = seasonHREF

    return seasons

def getSquads(seasons, year_data, year_now):
    squads_seasons = {}
    for year in seasons: 
        if int(year) > year_data and int(year) < year_now :
            url = seasons[year]
            squads = {}
            r = requests.get(url)
            soup = BeautifulSoup(r.content, features='lxml')
            for caption in soup.find_all('caption'):
                if caption.get_text() == 'League Table Table':
                    table = caption.find_parent('table')
                    break
            for row in table.tbody.find_all('tr'):    
                columns = row.find_all('td')
                if(columns != []):
                    squad = columns[0].text.strip()
                    
                    squadHREF = columns[0].find_all('a', href=True)
                    squadHREF = formatHREF(squadHREF)

                    squads[squad] = squadHREF
            squads_seasons[year] = squads

    return squads_seasons


def getSeasonMatchReports(squads):
    matchReports = {}
    for squad in squads: 
        matchs = []
        url = squads[squad]
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features='lxml')
        table = soup.find('table', id='matchlogs_for')
        for row in table.tbody.find_all('tr'):    
            columns = row.find_all('td')
            if(columns != []):
                matchHREF = columns[14].find_all('a', href=True)
                matchHREF = formatHREF(matchHREF)
                matchs.append(matchHREF)
        
        matchReports[squad] = matchs
    return matchReports

def getMRSTeam(soup):

    titles_list = []
    squads_names = []
    extra_stats = []
    initial_stats = []
    j = 0

    team_stats = soup.find('div', {'id': 'team_stats'})

    team_stats_extra = soup.find('div', {'id': 'team_stats_extra'})
    team_stats_extra = team_stats_extra.find_all('div')

    stats_titles = team_stats.find_all('th') 
    stats = team_stats.find_all('strong') 
    squads = team_stats.find_all('span', { 'class': 'teamandlogo'})


    for squad in squads: 
        squad = squad.text.strip()
        squads_names.append(squad)

    for th in stats_titles: 
        try:
            col = int(th["colspan"])
        except (ValueError, KeyError) as e:
            col = 0
        if col == 2: 
            th = th.text.strip()
            if th != 'Cards':
                titles_list.append(th)
    
    for i, stat in enumerate(stats):
        
        if i % 2 == 0:
            initial_stats.append(stat.text.strip())
            initial_stats.append(titles_list[j])
            j += 1
        else: 
            initial_stats.append(stat.text.strip())

    for stat in team_stats_extra:
        stat = stat.text.strip()
        check = False

        if stat == None and check == False:
            check = True
        if stat == None and check == True:
            check = False
        if check == False and ('\n' not in stat) and (stat not in squads_names) and (len(stat) != 0):
            extra_stats.append(stat)
    
    final_stats = initial_stats + extra_stats
    stats_team_dict = formatMRSTeam(squads_names, final_stats)

    return stats_team_dict


def getMatchReportStats(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')
    stats_team_dict = getMRSTeam(soup)

    return stats_team_dict

def getSignings(filter_squads):
    squad_players = {}
    for squad in filter_squads:
        season_players = {}
        for year in filter_squads[squad]:
            url = filter_squads[squad][year]
            r = requests.get(url)
            soup = BeautifulSoup(r.content, features='lxml')
            players = getPlayers(soup)
            season_players[year] = players
        squad_players[squad] = season_players

    return squad_players


def getPlayers(soup):
    table_players = soup.find('table')
    players_dicc = {}
    rows = table_players.tbody.find_all('tr')    
    for i, row in enumerate(table_players.tbody.find_all('th')):
        
        columns = rows[i].find_all('td')
        name = row.text.strip()
        player_href = row.find_all('a', href=True)
        player_href = formatHREF(player_href)
        min = columns[5].text.strip()

        if ',' in min:
            min = min.replace(',', '')
        if len(min) > 0:
            min = int(min)
            if min > 270: 
                players_dicc[name] = player_href
            

    return players_dicc

def getColumnNames(soup, stats_df,col):
    col_names = ['Name', 'Team', 'Team_Href']
    table_players = soup.find('table')
    rows = table_players.thead.find_all('tr')
    row = rows[1]
    for i, col_name in enumerate(row.find_all('th')):
        col_name = col_name.text.strip()
        col_names.append(col_name)

    stats_df.append(col_names)
    return stats_df

def getColumnNamesGK(soup, stats_df_gk,col):
    col_names = ['Name', 'Team', 'Team_Href']
    table_players = soup.find('table')
    rows = table_players.thead.find_all('tr')
    row = rows[1]
    for i, col_name in enumerate(row.find_all('th')):
        col_name = col_name.text.strip()
        col_names.append(col_name)

    stats_df_gk.append(col_names)
    return stats_df_gk

def getPlayerStats(soup, squad_url, stats_df,stats_df_gk,  col):
    name = soup.find('h1')
    name = name.find('span')
    name = name.text.strip()
    meta = soup.find_all('p')
    for data in meta:
        if 'Position' in data.text.strip(): 
            pos = data.text.strip()

    team = col
    table_players = soup.find('table')
    rows = table_players.tbody.find_all('th') 
    
    if 'GK' not in pos:
        if len(stats_df) == 0:
            stats_df = getColumnNames(soup, stats_df, col)

        for i,row in enumerate(table_players.tbody.find_all('tr')):
            match_stats = []
            date = rows[i].text.strip()  
            match_stats.append(name)  
            match_stats.append(team)
            match_stats.append(squad_url)
            match_stats.append(date)
            columns = row.find_all('td')
            for cell in columns:
                cell = cell.text.strip()
                match_stats.append(cell)
            if len(match_stats) == 32:
                stats_df.append(match_stats)

    else: 
        if len(stats_df_gk) == 0:
            stats_df_gk = getColumnNamesGK(soup, stats_df_gk, col)

        for i,row in enumerate(table_players.tbody.find_all('tr')):
            match_stats = []
            date = rows[i].text.strip()  
            match_stats.append(name)  
            match_stats.append(team)
            match_stats.append(squad_url)
            match_stats.append(date)
            columns = row.find_all('td')
            for cell in columns:
                cell = cell.text.strip()
                match_stats.append(cell)
            if len(match_stats) == 24:
                stats_df_gk.append(match_stats)


    return stats_df


def getSeasonURL(soup, year): 
    for caption in soup.find_all('caption'):
                if 'Domestic Leagues' in caption.get_text():
                    table_players = caption.find_parent('table')
                    break

    rows = table_players.tbody.find_all('tr')
    season_url2 = None
    squad_url2 = None   
    for i, row in enumerate(table_players.tbody.find_all('th')):
        columns = rows[i].find_all('td', {'data-stat':'matches'})
        columns2 = rows[i].find_all('td', {'data-stat':'squad'})
        player_year = row.text.strip()
        if len(player_year) > 4:
            player_year = player_year[:3]
        if len(player_year) == 4:
            player_year = int(player_year)
        if year == player_year:
            season_url = columns[0].find_all('a', href=True)
            season_url = formatHREF(season_url)
            print(season_url)

            squad_url = columns2[0].find_all('a', href=True)
            squad_url = formatHREF(squad_url)

        if int(year - 1) == player_year:
            if len(columns[0]) > 0:
                season_url2 = columns[0].find_all('a', href=True)
                season_url2 = formatHREF(season_url2)
                print(season_url2)

            squad_url2 = columns2[0].find_all('a', href=True)
            squad_url2 = formatHREF(squad_url2)

    return season_url, squad_url, season_url2, squad_url2
        

def getSigningStats(url, year, col, stats_df, stats_df_gk): 
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')
    season_url = getSeasonURL(soup, year)
    
    if season_url[2] != None:

        r2 = requests.get(season_url[0])
        soup2 = BeautifulSoup(r2.content, features='lxml')
        stats_df = getPlayerStats(soup2,season_url[1], stats_df, stats_df_gk,  col)

        r3 = requests.get(season_url[2])
        soup3 = BeautifulSoup(r3.content, features='lxml')
        stats_df = getPlayerStats(soup3,season_url[3], stats_df, stats_df_gk,  col)

    return stats_df, stats_df_gk


def getAllSquadSigningStats(df, col):
    stats_df = []
    stats_df_gk = []
    
    for i, row in df.iterrows():
        year = row['Year']
        list = row[col]
        print(list)
        
        for i, url in enumerate(list):
            signing_stats = getSigningStats(url, year, col, stats_df,stats_df_gk )
            stats_df = signing_stats[0]
            stats_df_gk = signing_stats[1]
            sleep(randint(5,10))

    stats_df = pd.DataFrame(stats_df)
    stats_df_gk = pd.DataFrame(stats_df_gk)

    return stats_df, stats_df_gk


def getNormalizedStats(url, name, stats_names):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')

    for caption in soup.find_all('caption'):
                if 'Standard Stats' in caption.get_text():
                    table_standard = caption.find_parent('table')
                    break
    
    rows = table_standard.tbody.find_all('tr')
    stats_dict = createStatsDict(stats_names)
    player_dict = createStatsDict(stats_names)
    all_stats = True
    main_pos = []
    pos_players = []
    for i, row in enumerate(table_standard.tbody.find_all('th')):
        player_name = row.text.strip()
        position = rows[i].find_all('td', {'data-stat':'position'})
        
        if name == player_name:
            pos = position[0].text.strip()
            if ',' in pos:
                pos = pos.split(',')
                main_pos = pos
            else:
                main_pos.append(pos)
            break

    for i, row in enumerate(table_standard.tbody.find_all('th')):
        player_name = row.text.strip()
        position = rows[i].find_all('td', {'data-stat':'position'})
        minutes = rows[i].find_all('td', {'data-stat':'minutes'})
        minutes = minutes[0].text.strip()
        mins = formatMinutes(minutes)
        pos = position[0].text.strip()
        same_pos = False
        player_pos = []
        if ',' in pos:
            pos = pos.split(',')
            player_pos = pos
        else:
            player_pos.append(pos)

        for each_pos in player_pos:
            if each_pos in main_pos:
                same_pos = True

        if mins < 270:
            break
        
        if same_pos:
            pos_players.append(player_name)

    for i, row in enumerate(table_standard.tbody.find_all('th')):
        player_name = row.text.strip()

        minutes = rows[i].find_all('td', {'data-stat':'minutes'})
        goals = rows[i].find_all('td', {'data-stat':'goals'})
        assists = rows[i].find_all('td', {'data-stat':'assists'})
        pens_made = rows[i].find_all('td', {'data-stat':'pens_made'})
        pens_att = rows[i].find_all('td', {'data-stat':'pens_att'})
        cards_yellow = rows[i].find_all('td', {'data-stat':'cards_yellow'})
        cards_red = rows[i].find_all('td', {'data-stat':'cards_red'})
        
        if player_name in pos_players:
            mins = formatMinutes(minutes[0].text.strip())
            goal = formatStat(goals[0].text.strip())
            ast = formatStat(assists[0].text.strip())
            pk = formatStat(pens_made[0].text.strip())
            pkatt = formatStat(pens_att[0].text.strip())
            crdY = formatStat(cards_yellow[0].text.strip())
            crdR = formatStat(cards_red[0].text.strip())
            
            
            stats_dict = updateDict(stats_dict, 'Min', mins)
            stats_dict = updateDict(stats_dict, 'Gls', goal[0])
            stats_dict = updateDict(stats_dict, 'Ast', ast[0])
            stats_dict = updateDict(stats_dict, 'PK', pk[0])
            stats_dict = updateDict(stats_dict, 'PKatt', pkatt[0])
            stats_dict = updateDict(stats_dict, 'CrdY', crdY[0])
            stats_dict = updateDict(stats_dict, 'CrdR', crdR[0])
        
        if player_name == name:

            player_dict = updateDict(player_dict, 'Min', mins)
            player_dict = updateDict(player_dict, 'Gls', goal[0])
            player_dict = updateDict(player_dict, 'Ast', ast[0])
            player_dict = updateDict(player_dict, 'PK', pk[0])
            player_dict = updateDict(player_dict, 'PKatt', pkatt[0])
            player_dict = updateDict(player_dict, 'CrdY', crdY[0])
            player_dict = updateDict(player_dict, 'CrdR', crdR[0])
        
    for caption in soup.find_all('caption'):
                if 'Shooting' in caption.get_text():
                    table_shooting = caption.find_parent('table')
                    break
    
    rows = table_shooting.tbody.find_all('tr')
    for i, row in enumerate(table_shooting.tbody.find_all('th')):
        player_name = row.text.strip()

        shots_total = rows[i].find_all('td', {'data-stat':'shots_total'})
        shots_on_target = rows[i].find_all('td', {'data-stat':'shots_on_target'})

        if player_name in pos_players:
            sh = formatStat(shots_total[0].text.strip())
            sot = formatStat(shots_on_target[0].text.strip())

            stats_dict = updateDict(stats_dict, 'Sh', sh[0])
            stats_dict = updateDict(stats_dict, 'SoT', sot[0])

        if player_name == name:

            player_dict = updateDict(player_dict, 'Sh', sh[0])
            player_dict = updateDict(player_dict, 'SoT', sot[0])


    for caption in soup.find_all('caption'):
                if 'Miscellaneous Stats ' in caption.get_text():
                    table_miscellaneous = caption.find_parent('table')
                    break
    
    rows = table_miscellaneous.tbody.find_all('tr')
    for i, row in enumerate(table_miscellaneous.tbody.find_all('th')):
        player_name = row.text.strip()

        fouls = rows[i].find_all('td', {'data-stat':'fouls'})
        fouled = rows[i].find_all('td', {'data-stat':'fouled'})
        offsides = rows[i].find_all('td', {'data-stat':'offsides'})
        crosses = rows[i].find_all('td', {'data-stat':'crosses'})
        interceptions = rows[i].find_all('td', {'data-stat':'interceptions'})
        tackles_won = rows[i].find_all('td', {'data-stat':'tackles_won'})
        own_goals = rows[i].find_all('td', {'data-stat':'own_goals'})
        
        if player_name in pos_players:
            
            fls = formatStat(fouls[0].text.strip())
            fld = formatStat(fouled[0].text.strip())
            off = formatStat(offsides[0].text.strip())
            crs = formatStat(crosses[0].text.strip())
            int = formatStat(interceptions[0].text.strip())
            tklw = formatStat(tackles_won[0].text.strip())
            og = formatStat(own_goals[0].text.strip())

            stats_dict = updateDict(stats_dict, 'Fls', fls[0])
            stats_dict = updateDict(stats_dict, 'Fld', fld[0])
            stats_dict = updateDict(stats_dict, 'Off', off[0])
            stats_dict = updateDict(stats_dict, 'Crs', crs[0])
            stats_dict = updateDict(stats_dict, 'Int', int[0])
            stats_dict = updateDict(stats_dict, 'TklW', tklw[0])
            stats_dict = updateDict(stats_dict, 'OG', og[0])
        
        if player_name == name:

            player_dict = updateDict(player_dict, 'Fls', fls[0])
            player_dict = updateDict(player_dict, 'Fld', fld[0])
            player_dict = updateDict(player_dict, 'Off', off[0])
            player_dict = updateDict(player_dict, 'Crs', crs[0])
            player_dict = updateDict(player_dict, 'Int', int[0])
            player_dict = updateDict(player_dict, 'TklW', tklw[0])
            player_dict = updateDict(player_dict, 'OG', og[0])

    normalized_stats = {}
    normalized_dict ={}
    all_stats = True
    empty_player_dict = True
    for key in player_dict:
        if len(player_dict[key]) == 0 and (key != "PKcon" and key != "PKwon") :
            empty_player_dict = False
    if empty_player_dict:
        normalized_stats = normalizedStats(player_dict, stats_dict)
        normalized_dict = normalized_stats[0]
        all_stats = normalized_stats[1]


    return normalized_dict, all_stats, len(pos_players), main_pos, empty_player_dict

def getMinGroup(url, name):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')
    total_mins = []
    max_min = 0
    player_min = 0
    info = soup.find_all('strong') 
    col_league = False
    for strong in info:
        if 'Governing Country' in strong.get_text():
            p = strong.find_parent('p')
            country = p.find('a')
            country = country.get_text()

            if 'Colombia' in country:
                col_league = True


    for caption in soup.find_all('caption'):
                if 'Standard Stats' in caption.get_text():
                    table_standard = caption.find_parent('table')
                    break
    
    rows = table_standard.tbody.find_all('tr')
    for i, row in enumerate(table_standard.tbody.find_all('th')):
        player_name = row.text.strip()
        minutes = rows[i].find_all('td', {'data-stat':'minutes'})
        mins = formatMinutes(minutes[0].text.strip())
        if i ==0:
            max_min = mins
        
        if player_name == name:
            player_min = mins


        if mins < 270:
            break

        
        total_mins.append(mins)
    
    group_min = groupMin(player_min, max_min, total_mins)


    return group_min, col_league

'''
DATAFRAME FUNCTIONS
'''

def iterLinks(df):
    cols = df.columns.tolist()
    for col in cols:
        if col != 'Year':
            for i, row in df.iterrows(): 
                df.at[i, col] = formatLinks(row[col])
    
    return df

'''
EXPORT FUNCTIONS
'''

def exportFinalCSV(df, path, name):
    route = cf.export_dir.replace('/App', '') + path
    df.to_csv(route + str(name) + '.csv')

    return None

def exportCleanFinalCSV(df, path, name):
    route = cf.clean_export_dir.replace('/App', '') + path
    df.to_csv(route + str(name) + '.csv')

    return None

