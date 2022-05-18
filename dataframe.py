import FBrefScraper as FBref
import DataFunctions as Dfx
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
signings = signings.drop([4])
signings = FBref.iterLinks(signings)
signings = Dfx.signingsCount(signings)
FBref.exportCleanFinalCSV(signings,'','signings_count')

def getSigningsData(col_name, name):
    signings_stats = FBref.getAllSquadSigningStats(signings, col_name)
    FBref.exportFinalCSV(signings_stats[0],'/teams/', name)
    FBref.exportFinalCSV(signings_stats[1],'/teams/', (name + str('_GK')))
    
    return None

