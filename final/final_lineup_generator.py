import pandas as pd
import io
import requests

'''
grab projections columns and id column from projection csv and merge with player list from FanDuel league
'''
fields1 = ['Name', 'Id', 'Projection',]
fields2 = ['Id', 'Position', 'FPPG', 'Salary', 'Team', 'Opponent', 'Injury Indicator']

'''
import two csvs
'''
url1 = "https://raw.githubusercontent.com/brttstl/proj-fantasy/master/final/week_13_projections.csv"
url2 = "https://raw.githubusercontent.com/brttstl/proj-fantasy/master/final/FanDuel-NFL-2015-12-13-13913-players-list.csv"
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
value_list = ['IR', 'Q']
healthy = merged[~merged.injury.isin(value_list)]


healthy.to_csv("/Users/brett/GitHub/proj-fantasy/final/final_merged_projections.csv", index=False)
