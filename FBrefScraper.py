'''
WEB SCRAPING FUNCTIONS FOR FBREF
'''

#Libraries
from cgitb import html
import requests
from bs4 import BeautifulSoup

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
            squad_href = squad_href[0]
            squad_href = 'https://www.fbref.com/' + str(squad_href['href'])

            squads[squad] = squad_href

    return squads