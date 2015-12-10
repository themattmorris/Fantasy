import pandas as pd
import io
import requests

'''
IMPORTANT: specify final output path here
'''
output_path = "/Users/brett/GitHub/proj-fantasy/data/player_pool.csv"

'''
grab projections columns and id column from projection csv and merge with player list from FanDuel league
'''
fields1 = ['Name', 'Id', 'Projection',]
fields2 = ['Id', 'Position', 'FPPG', 'Salary', 'Team', 'Opponent', 'Injury Indicator']

'''
import two csvs
'''
url1 = "https://raw.githubusercontent.com/brttstl/proj-fantasy/master/data/week_13_projections.csv"
url2 = "https://raw.githubusercontent.com/brttstl/proj-fantasy/master/data/FanDuel-NFL-2015-12-13-13913-players-list.csv"
projs = requests.get(url1).content
plyrs = requests.get(url2).content
df1 = pd.read_csv(io.StringIO(projs.decode('utf-8')), usecols=fields1)
df2 = pd.read_csv(io.StringIO(plyrs.decode('utf-8')), usecols=fields2)

'''
merge datasets
'''
merged = df1.merge(df2, on="Id").fillna("")
merged = merged.drop('Id', 1)
merged.columns = ['name', 'projection',	'position', 'fppg', 'salary', 'team', 'opponent', 'injury']

'''
remove injury risks
'''
injured = ['IR', 'O', 'Q']
healthy = merged[~merged.injury.isin(injured)]

'''
drop unneccessary variables
'''
players = healthy[['name', 'projection', 'position', 'salary', 'team']]

'''
write to csv for sake keeping
'''
players.to_csv(output_path, index=False)