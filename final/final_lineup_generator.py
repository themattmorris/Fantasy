import pandas as pd
import io
import requests
from optparse import OptionParser
from itertools import groupby
from openopt import *
from FuncDesigner import *

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
injured = ['IR', 'O', 'Q']
healthy = merged[~merged.injury.isin(injured)]

'''
write to csv for sake keeping
'''
healthy.to_csv("/Users/brett/GitHub/proj-fantasy/final/final_merged_projections.csv", index=False)

maxSalary = 60000
options.stackLimit = 4

# constrain positions, salary, num players per team
constraints = lambda values: (values['salary'] <= maxSalary, values['QB'] == 1, values['RB'] == 2, values['WR'] == 3, values['TE'] == 1, values['K'] == 1, values['D'] == 1,
                              values["ARI"] < options.stackLimit, values["ATL"] < options.stackLimit, values["BAL"] < options.stackLimit, values["BUF"] < options.stackLimit,
                              values["CAR"] < options.stackLimit, values["CHI"] < options.stackLimit, values["CIN"] < options.stackLimit, values["CLE"] < options.stackLimit,
                              values["DAL"] < options.stackLimit, values["DEN"] < options.stackLimit, values["DET"] < options.stackLimit, values["HOU"] < options.stackLimit,
                              values["IND"] < options.stackLimit, values["JAC"] < options.stackLimit, values["KC"] < options.stackLimit, values["MIA"] < options.stackLimit,
                              values["MIN"] < options.stackLimit, values["NE"] < options.stackLimit, values["NO"] < options.stackLimit, values["NYG"] < options.stackLimit,
                              values["NYJ"] < options.stackLimit, values["OAK"] < options.stackLimit, values["PHI"] < options.stackLimit, values["PIT"] < options.stackLimit,
                              values["SD"] < options.stackLimit, values["SEA"] < options.stackLimit, values["SF"] < options.stackLimit, values["STL"] < options.stackLimit,
                              values["TB"] < options.stackLimit, values["TEN"] < options.stackLimit, values["WAS"])
objective = "projection"

p = KSP(objective, healthy.projection, goal='max', constraints = constraints)
r = p.solve('glpk')

print(r.xf)
