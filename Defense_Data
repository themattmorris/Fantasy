### ========================================================= ###
###                      IMPORT PACKAGES                      ### 
### ========================================================= ###

import requests
import re
import math
from BeautifulSoup import BeautifulSoup
import pandas as pd
import numpy as np

### ========================================================= ###
###                  INITIALIZE VARIABLES                     ### 
### ========================================================= ###

tags = list()

years = list()
years = (2012, 2013, 2014, 2015)

stats = list()
stats = ('passing', 'rushing', 'receiving', 'returning')
stats2 = ('Passing', 'Rushing', 'Receiving', 'Returning')
statsDict = dict()
statsDict = {'passing':'Passing', 'rushing':'Rushing', 'receiving':'Receiving', 'returning':'Returning', 'NA':'Total'}

teams = dict()
teams = {'Baltimore':'BAL','Cincinnati':'CIN','Cleveland':'CLE','Pittsburgh':'PIT','Houston':'HOU','Indianapolis':'IND','Jacksonville':'JAX','Tennessee':'TEN','Buffalo':'BUF','Miami':'MIA','New England':'NWE','NY Jets':'NYJ','Denver':'DEN','Kansas City':'KAN','Oakland':'OAK','San Diego':'SDG','Chicago':'CHI','Detroit':'DET','Green Bay':'GNB','Minnesota':'MIN','Atlanta':'ATL','Carolina':'CAR','New Orleans':'NOR','Tampa Bay':'TAM','Dallas':'DAL','NY Giants':'NYG','Philadelphia':'PHI','Washington':'WAS','Arizona':'ARI','San Francisco':'SFO','Seattle':'SEA','St. Louis':'STL'}

result = pd.DataFrame

### ========================================================= ###
###                      FUNCTIONS                            ### 
### ========================================================= ###

def ReformatDataFrame(year, dataframe, flag, merge, stat):

    global result
    global statsDict
    
    # Merge variable determines if the various years are ready to be merged yet.
    if ((merge == 1) and (int(year) > 2012)):
        if int(year) == 2013:
            result.to_csv('C:/Users/Matt/Desktop/Defense_Data.csv', index = False, sep=',', header = True)
            result = pd.DataFrame
        else:
            with open('C:/Users/Matt/Desktop/Defense_Data.csv', 'a') as f:
                result.to_csv(f, index = False, header = False)

    # Append season to data
    x = np.repeat(year, 32, axis = 0)
    season = list(x)
    season[0] = 'SEASON'
    season.append(year)
    df2 = pd.DataFrame(season)
    df3 = pd.concat([dataframe, df2], axis = 1, ignore_index = True)
    
    # Rename colums
    col = list()
    for c in df3.columns:
        if (df3[c][0] <> 'TEAM') and (df3[c][0] <> 'SEASON'):
            col.append(str(statsDict[stat]) + '_' + str(df3[c][0]))
        else:
            col.append(df3[c][0])
    df3.columns = col
    
    # Drop old header row in data
    df3 = df3.ix[1:]
    
    # Create resultant dataframe.
    if flag == 1:
        result = df3
    elif flag == 2:
        # Join to result dataset
        result = pd.merge(result, df3, on = ['TEAM', 'SEASON'])

    return


def FindStat(url):
    
    global stats

    for stat in stats:
        if url.find(stat) > -1:
            y = stat
            break
        else:
            y = 'NA'
            
    return y

### ========================================================= ###
###                      START CODE                           ### 
### ========================================================= ###

for year in years:
    if year < 2015:
        url = 'http://espn.go.com/nfl/statistics/team/_/stat/total/position/defense/year/' + str(year)
    elif year == 2015:
        url = 'http://espn.go.com/nfl/statistics/team/_/stat/total/position/defense'
    tags.append(url)
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data)
    
    # Find all the different stats sections in the data
    for stat in stats:
        if year < 2015:
            tags.append(soup.findAll(href = re.compile('http://espn.go.com/nfl/statistics/team/_/stat/' + str(stat) + '/position/defense/year/' + str(year))))
        elif year == 2015:
            tags.append(soup.findAll(href = re.compile('http://espn.go.com/nfl/statistics/team/_/stat/' + str(stat) + '/position/defense')))

# Go through each url
for url in tags:
    url = str(url)
    url = url.replace('[<a href="', '')
    url = url.replace('</a>]', '')
    for stat in stats2:
        url = url.replace('">' + str(stat), '')
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data)
    
    # Pull HTML table into Python
    table = str(soup.find("table", attrs = {"class":"tablehead"}))
        
    # Create dataframe using HTML table
    df = pd.read_html(table)
    
    # Change team field to be abbreviation to be used for joining to other tables
    # Start position is the row starting number.  Some tables have multiple header rows.
    if url.find('returning') > -1:
        df[0] = df[0].ix[1:]
        df[0] = df[0].reset_index(drop = True)
    
    row = 1
    for team in df[0][1][1:]:
        df[0][1][row] = teams[team]
        row += 1
    
    # Fix rank values that are null
    row = 1
    for rank in df[0][0][1:]:
        if math.isnan(float(df[0][0][row])):
            df[0][0][row] = df[0][0][row - 1]
        row += 1
        
    # Prepare data frame to be written to CSV
    # If it is the first stats page (total defense statistics)
    if url[0:74] == 'http://espn.go.com/nfl/statistics/team/_/stat/total/position/defense/year/':
        year = url[74:78]
        ReformatDataFrame(year, df[0], 1, 1, FindStat(url))
    
    # If it is year 2015 (total defense statistics)
    elif url == 'http://espn.go.com/nfl/statistics/team/_/stat/total/position/defense':
        year = 2015
        ReformatDataFrame(year, df[0], 1, 1, FindStat(url))
    
    # If it is any other year but other statistics
    elif url.find('201') > -1:
        year = url[url.find('201'):url.find('201') + 4]
        ReformatDataFrame(year, df[0], 2, 0, FindStat(url))
        
    # If 2015 and other statistics
    else:
        year = 2015
        ReformatDataFrame(year, df[0], 2, 0, FindStat(url))
        
# Print last result to csv
with open('C:/Users/Matt/Desktop/Defense_Data.csv', 'a') as f:
    result.to_csv(f, index = False, header = False)
