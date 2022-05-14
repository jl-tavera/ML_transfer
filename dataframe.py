import FBrefScraper as FBref

seasons = FBref.getSeasons('https://fbref.com/en/comps/41/history/Primera-A-Seasons')
# print(seasons)
squads = FBref.getSquads(seasons, 2016, 2022)
# print(squads)
teams_A = FBref.getATeams(squads)
print(teams_A)
# matchReports = FBref.getSeasonMatchReports(squads)
# team_stats = FBref.getMatchReportStats('https://fbref.com/en/matches/9329c509/Bengaluru-Mumbai-City-November-19-2017-Indian-Super-League')
# print(team_stats)
