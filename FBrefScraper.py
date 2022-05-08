'''
WEB SCRAPING FUNCTIONS FOR FBREF
'''

'''
LIBRARIES
'''

from cgitb import html
from tabnanny import check
from typing import final
import requests
from bs4 import BeautifulSoup
from soupsieve import match



'''
FORMAT FUNCTIONS
'''

def formatHREF(href):
    href = href[0]
    href = 'https://www.fbref.com/' + str(href['href'])
    return href



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

def getSquads(url):
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

    return squads

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

def getMatchReportStats(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')
   
    titles_list = []
    squads_names = []
    extra_stats = []
    initial_stats = []

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
        j = 0
        if i % 2 == 0:
            initial_stats.append(stat.text.strip())
            initial_stats.append(titles_list[j])
            j =+ 1
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

    return final_stats, squads_names
    