'''
WEB SCRAPING FUNCTIONS FOR FBREF
'''

'''
Libraries
'''

from cgitb import html
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
            
            squad_href = columns[0].find_all('a', href=True)
            squad_href = formatHREF(squad_href)

            squads[squad] = squad_href

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