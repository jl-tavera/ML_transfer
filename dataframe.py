import FBrefScraper as FBref

# seasons = FBref.getSeasons('https://fbref.com/en/comps/82/history/Indian-Super-League-Seasons')
# squads = FBref.getSquads('https://fbref.com/en/comps/82/Indian-Super-League-Stats')
# matchReports = FBref.getSeasonMatchReports(squads)
team_stats = FBref.getMatchReportStats('https://fbref.com/en/matches/9329c509/Bengaluru-Mumbai-City-November-19-2017-Indian-Super-League')
print(team_stats)
