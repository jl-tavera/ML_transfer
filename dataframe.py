import FBrefScraper as FBref
import DataFunctions as Dfx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors

def createDFSignings():
    seasons = FBref.getSeasons('https://fbref.com/en/comps/41/history/Primera-A-Seasons')
    squads = FBref.getSquads(seasons, 2015, 2022)
    teams_A = FBref.getATeams(squads)
    filter_squads = FBref.filterSquads(squads, teams_A)
    players = FBref.getSignings(filter_squads)
    signings = FBref.filterSignings(players)
    FBref.exportFinalCSV(signings,'','signings')
    return None

def signingCounts(filename):
    signings = FBref.loadCSV(filename)
    signings = signings.rename(columns={'Unnamed: 0': 'Year'})
    signings = signings.drop([4])
    signings = FBref.iterLinks(signings)
    signings = signings.set_index(signings.columns[0])
    signings = Dfx.signingsCount(signings)
    FBref.exportCleanFinalCSV(signings,'','signings_count')

    signings_tr = signings.transpose() 
    signings_tr['Teams'] = signings_tr.index
    signings_tr = signings_tr.drop('Total', 1)


    count_plot = signings_tr.plot(x='Teams',
                    kind='barh', 
                    stacked=True,
                    title='Fichajes por Año', 
                    figsize=(12,6))
                    
    xlab = count_plot.xaxis.get_label()
    ylab = count_plot.yaxis.get_label()
    ttl = count_plot.title

    xlab.set_style('italic')
    xlab.set_size(10)
    ylab.set_style('italic')
    ylab.set_size(10)
    ttl.set_weight('bold')
    ttl.set_size(20)

    plot = count_plot.get_figure()
    path = 'img/count_plot'
    plot.savefig( path, dpi=300)

    return None



def getSigningsData(col_name, name):
    signings_stats = FBref.getAllSquadSigningStats(signings, col_name)
    FBref.exportFinalCSV(signings_stats[0],'/teams/', name)
    FBref.exportFinalCSV(signings_stats[1],'/teams/', (name + str('_GK')))
    
    return None

