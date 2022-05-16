import FBrefScraper as FBref
import pandas as pd

def createDFSignings():
    seasons = FBref.getSeasons('https://fbref.com/en/comps/41/history/Primera-A-Seasons')
    squads = FBref.getSquads(seasons, 2015, 2022)
    teams_A = FBref.getATeams(squads)
    filter_squads = FBref.filterSquads(squads, teams_A)
    players = FBref.getSignings(filter_squads)
    signings = FBref.filterSignings(players)
    FBref.exportFinalCSV(signings,'','signings')
    return None

signings = FBref.loadCSV('signings.csv')
signings = signings.rename(columns={'Unnamed: 0': 'Year'})
signings = signings.drop([0])
signings = FBref.iterLinks(signings)
print(signings.head)

signings_stats = FBref.getAllSquadSigningStats(signings, 'Santa Fe')
FBref.exportFinalCSV(signings_stats[0],'/teams/', 'SantaFe')
FBref.exportFinalCSV(signings_stats[1],'/teams/','SantaFe_GK')

