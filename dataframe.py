import FBrefScraper as FBref

squads = FBref.getSquads('https://fbref.com/en/comps/41/Categoria-Primera-A-Stats')
matchReports = FBref.getSeasonMatchReports(squads)
print(matchReports)