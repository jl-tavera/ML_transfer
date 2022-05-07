import FBrefScraper as FBref

seasons = FBref.getSeasons('https://fbref.com/en/comps/82/history/Indian-Super-League-Seasons')
squads = FBref.getSquads('https://fbref.com/en/comps/82/Indian-Super-League-Stats')
matchReports = FBref.getSeasonMatchReports(squads)
print(seasons)