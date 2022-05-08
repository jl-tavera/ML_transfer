import FBrefScraper as FBref

# seasons = FBref.getSeasons('https://fbref.com/en/comps/82/history/Indian-Super-League-Seasons')
# squads = FBref.getSquads('https://fbref.com/en/comps/82/Indian-Super-League-Stats')
# matchReports = FBref.getSeasonMatchReports(squads)
team_stats = FBref.getMatchReportStats('https://fbref.com/en/matches/a985620d/Tolima-CD-America-February-7-2017-Categoria-Primera-A')
print(team_stats)
