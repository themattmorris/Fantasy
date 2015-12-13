### ========================================================= ###
###                        USER INPUTS                        ### 
### ========================================================= ###

curWeek = 14 # week to create projections for
year = 2015 # football season
filepath = 'C:/Users/Matt/Desktop/' # location of where to write output file

### ========================================================= ###
###                      IMPORT PACKAGES                      ### 
### ========================================================= ###

import numpy as np
import pandas as pd
import math
import requests
import re
import io
from sklearn import metrics, linear_model, svm, ensemble
from sklearn.feature_extraction import DictVectorizer
from collections import defaultdict
from BeautifulSoup import BeautifulSoup

### ========================================================= ###
###                  INITIALIZE VARIABLES                     ### 
### ========================================================= ###

salCap = 60000 # dollars
colName = 'Projection' # column name for Fan Duel projections
filename ='Week' + str(curWeek) + '_projections.csv' # name of file to write output to
iterations = 10 # number of model iterations to run

# Number of players by position in lineup
pos_count = dict()
pos_count = {
'QB':1,
'RB':2,
'WR':3,
'TE':1,
'K':1,
'DEF':1}

# Both sides of the ball
sides = list()
sides = ('offense', 'defense')

# Variables for web scraping
tags = list()

stats = list()
stats = (
'passing',
'rushing',
'receiving',
'returning')

stats2 = (
'Passing',
'Rushing',
'Receiving',
'Returning')
statsDict = dict()

statsDict = {
'passing':'Passing',
'rushing':'Rushing',
'receiving':'Receiving',
'returning':'Returning',
'NA':'Total'}

teams = dict()
teams = {
'Baltimore':'BAL',
'Cincinnati':'CIN',
'Cleveland':'CLE',
'Pittsburgh':'PIT',
'Houston':'HOU',
'Indianapolis':'IND',
'Jacksonville':'JAX',
'Tennessee':'TEN',
'Buffalo':'BUF',
'Miami':'MIA',
'New England':'NWE',
'NY Jets':'NYJ',
'Denver':'DEN',
'Kansas City':'KAN',
'Oakland':'OAK',
'San Diego':'SDG',
'Chicago':'CHI',
'Detroit':'DET',
'Green Bay':'GNB',
'Minnesota':'MIN',
'Atlanta':'ATL',
'Carolina':'CAR',
'New Orleans':'NOR',
'Tampa Bay':'TAM',
'Dallas':'DAL',
'NY Giants':'NYG',
'Philadelphia':'PHI',
'Washington':'WAS',
'Arizona':'ARI',
'San Francisco':'SFO',
'Seattle':'SEA',
'St. Louis':'STL'}

# Standardize abbreviations within datasets
teamabr = dict()
teamabr = {
'GB':'GNB',
'JAC':'JAX',
'KC':'KAN',
'NE':'NWE',
'NO':'NOR',
'SD':'SDG',
'SF':'SFO',
'TB':'TAM'}

# Dataframes
off_result = pd.DataFrame
def_result = pd.DataFrame

### ========================================================= ###
###                      FUNCTIONS                            ### 
### ========================================================= ###

def TrainingSet(n, df):

        # Creates random sample of records from the input dataframe    
        return df.ix[np.random.choice(df.index, n, replace = False)]


def CleanData(position, df, df_features, df_compare_features):

    # Goes through feature lists and removes any predictors that are not also included in the comparison feature list
    # This is done so that the model data, training set, and test set all have the same predictors.

    predictorslist = list()
    featureslist = list

    # Intialize boolean array length of input array to be hit against input array to pull only True values out
    mask = np.ones(len(df_features[position]), dtype = bool)
    for i, feature in enumerate(df_features[position]):
        if feature not in df_compare_features[position]:
            mask[i] = False
            
    for i, player in enumerate(df[position]):
        predictorslist.append(df[position][i][mask])
    
    featureslist = list(np.asarray(df_features[position])[np.asarray(mask)])
        
    return np.asarray(predictorslist), featureslist
    

def ReformatDataFrame(year, dataframe, flag, stat, side):

    global off_result
    global def_result
    global statsDict

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
    if side == 'offense':
        if flag == 1:
            off_result = df3
        elif flag == 2:
            # Join to result dataset
            off_result = pd.merge(off_result, df3, on = ['TEAM', 'SEASON'])
    elif side == 'defense':
        if flag == 1:
            def_result = df3
        elif flag == 2:
            # Join to result dataset
            def_result = pd.merge(def_result, df3, on = ['TEAM', 'SEASON'])

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


def WebScrape(url, side):

    global stats
    global year

    tags = list()
    tags.append(url)
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data)

    # Find all the different stats sections in the data
    for stat in stats:
        if side == 'offense':
            tags.append(soup.findAll(href = re.compile('http://espn.go.com/nfl/statistics/team/_/stat/' + str(stat))))
        elif side == 'defense':
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
        # If it is the first stats page (total offense statistics)
        if side == 'offense':
            if url == 'http://espn.go.com/nfl/statistics/team/_/stat/total':
                ReformatDataFrame(year, df[0], 1, FindStat(url), side) 
            # Other statistics
            else:
                ReformatDataFrame(year, df[0], 2, FindStat(url), side)
        elif side == 'defense':
            if url == 'http://espn.go.com/nfl/statistics/team/_/stat/total/position/defense':
                ReformatDataFrame(year, df[0], 1, FindStat(url), side)
            # Other statistics
            else:
                ReformatDataFrame(year, df[0], 2, FindStat(url), side)

    return


def CleanWeekDF():

    # Cleans the fan duel current weekly player list (lineup prior to gametime)
    
    # Read in current week players with predictor variables included to run through models
    weekdf = requests.get('https://raw.githubusercontent.com/brttstl/proj-fantasy/master/data/FanDuel-NFL-2015-12-13-13913-players-list.csv').content
    weekdf = pd.read_csv(io.StringIO(weekdf.decode('utf-8')))

    # Get correct team name for looking up
    for i, team in enumerate(weekdf['Team']):
        if team in teamabr:
            weekdf.loc[i, 'Team'] = teamabr[team]

    for i, team in enumerate(weekdf['Opponent']):
        if team in teamabr:
            weekdf.loc[i, 'Opponent'] = teamabr[team]

    # Initialize blank dataframes
    x = np.repeat(0, len(weekdf), axis = 0)
    x = list(x)
    names = pd.DataFrame({'Name':x})
    locations = pd.DataFrame({'Location':x})
    ha = pd.DataFrame({'h/a':x})
    weekdf = pd.concat([weekdf, names, locations, ha], axis = 1, ignore_index = False)

    # Write columns for name, location, and home/away
    count = 0
    while count < len(weekdf):
        
        # Find location from game column (in format NE@HOU, etc.)
        weekdf.loc[count, 'Location'] = weekdf.loc[count, 'Game'][weekdf.loc[count, 'Game'].find('@') + 1:]
        
        # Fix team abbreviations to be consistent with all datasets (look up in dictionary)
        if weekdf.loc[count, 'Location'] in teamabr:
            weekdf.loc[count, 'Location'] = teamabr[weekdf.loc[count, 'Location']]

        # Determine if the current player is at home or away
        if weekdf.loc[count, 'Location'] == weekdf.loc[count, 'Team']:
            weekdf.loc[count, 'h/a'] = 'H'
        else:
            weekdf.loc[count, 'h/a'] = 'A'
            
        # Reformat name attributes (to be joined to later)
        if weekdf['Position'][count] == 'D':
            weekdf.loc[count, 'Position'] = 'DEF'
            name = str(weekdf['Team'][count]) + ' Defense'
        else:
            name = str(weekdf['First Name'][count]) + ' ' + str(weekdf['Last Name'][count])
        weekdf.loc[count, 'Name'] = name
        count += 1

    return weekdf


### ========================================================= ###
###                     SCRAPE FOR DATA                       ### 
### ========================================================= ###

# Get stats for opposing team offense (in the case of fantasy defense) and opposing team defense
# (in the case of fantasy offensive position player
for side in sides:
    if side == 'offense':
        url = 'http://espn.go.com/nfl/statistics/team/_/stat/total'
    elif side == 'defense':
        url = 'http://espn.go.com/nfl/statistics/team/_/stat/total/position/defense'
    WebScrape(url, side)

### ========================================================= ###
###                     PREPARE DATA                          ### 
### ========================================================= ###

# Go through both offense and defense
outdf = dict((side, None) for side in sides)

for side in sides:

    # Read in historical csv file
    if side == 'offense':
        df = def_result
    elif side == 'defense':
        df = off_result
        
    # Drop unnecessary columns
    columns = list()
    if side == 'offense':
        columns = (
                'SEASON',
                'Total_PTS',
                'Total_YDS',
                'Total_YDS/G',
                'Total_PASS',
                'Total_RUSH',
                'Passing_ATT',
                'Passing_COMP',
                'Passing_YDS',
                'Passing_YDS/A',
                'Passing_LONG',
                'Passing_SACK',
                'Passing_YDSL',
                'Rushing_ATT',
                'Rushing_YDS',
                'Rushing_LONG',
                'Rushing_FUM',
                'Receiving_YDS',
                'Receiving_AVG',
                'Receiving_LONG',
                'Receiving_FUM',
                'Returning_RK',
                'Returning_YDS',
                'Returning_ATT',
                'Returning_AVG',
                'Returning_LNG',
                'Returning_TD',
                'Returning_FC')
    elif side == 'defense':
        columns = (
                'SEASON',
                'Total_PTS',
                'Total_YDS',
                'Total_PASS',
                'Total_RUSH',
                'Passing_ATT',
                'Passing_COMP',
                'Passing_YDS',
                'Passing_YDS/A',
                'Passing_LONG',
                'Passing_TD',
                'Passing_YDSL',
                'Rushing_ATT',
                'Rushing_YDS',
                'Rushing_YDS/A',
                'Rushing_LONG',
                'Rushing_TD',
                'Rushing_FUM',
                'Receiving_YDS',
                'Receiving_AVG',
                'Receiving_LONG',
                'Receiving_FUM',
                'Returning_RK',
                'Returning_YDS',
                'Returning_AVG',
                'Returning_LNG',
                'Returning_TD',
                'Returning_ATT',
                'Returning_FC')
        
    for column in columns:
        df = df.drop(column, axis = 1)
    
    # Read in current week players with predictor variables included to run through models
    weekdf = CleanWeekDF()

    # Drop unnecessary columns
    columns = list()
    columns = (
            'Played',
            'Location',
            'h/a',
            'First Name',
            'Last Name',
            'ID',
            'Game',
            'Opponent',
            'Team',
            'Injury Details',
            'Salary',)
    for column in columns:
        weekdf = weekdf.drop(column, axis = 1)

    # Read in fan duel season data into model
    seasondf = requests.get('https://raw.githubusercontent.com/brttstl/proj-fantasy/master/data/fanduel_season_data.csv').content
    seasondf = pd.read_csv(io.StringIO(seasondf.decode('utf-8')))

    # Drop unnecessary columns
    columns = list()
    columns = (
            'GID',
            'Year',
            'Week',
            'Pos')
    for column in columns:
        seasondf = seasondf.drop(column, axis = 1)
    
    # Read in current stadium data csv and merge it to the other datasets
    stadiums = requests.get('https://raw.githubusercontent.com/brttstl/proj-fantasy/master/data/stadiums.csv').content
    stadiums = pd.read_csv(io.StringIO(stadiums.decode('utf-8')))
    
    # Drop unnecessary columns
    columns = list()
    columns = (
            'season',
            'stadium_name',
            'city',
            'state',
            'team',
            'capacity',
            'surface_description')
    for column in columns:
        stadiums = stadiums.drop(column, axis = 1)

    # Merge datasets to create one dataset
    df = pd.merge(left = df, right = seasondf, left_on = 'TEAM', right_on = 'Oppt')
    df = pd.merge(left = df, right = weekdf, left_on = 'Name', right_on = 'Name')
    df = pd.merge(left = df, right = stadiums, left_on = 'Location', right_on = 'location')
    
    # Remove players that aren't playing and remove unnecessary columns
    df = df[(df['Injury Indicator'] != 'O') & (df['Injury Indicator'] != 'IR')]
    # df = df[df['Starter'] == 'Y']
    if side == 'offense':
        df = df[df['Position'] <> 'DEF']
    elif side == 'defense':
        df = df[df['Position'] == 'DEF']
    columns = list()
    columns = (
            'TEAM',
            #'Starter',
            'Total_P YDS/G',
            'Total_R YDS/G',
            'Receiving_YDS/G',
            'Injury Indicator',
            'Location')
    for column in columns:
        df = df.drop(column, axis = 1)

    # Sort columns in order
    df = df.reindex_axis(sorted(df.columns), axis = 1)

    # Position data dictionary
    positions = list()
    positions = set(df['Position'])

    df1 = dict((position, 0) for position in positions)    
    df2 = dict((position, 0) for position in positions)
    
    # Output dictionary
    output_data = dict((position, None) for position in positions)

    # Statistical dictionaries
    mean = dict((position, []) for position in positions)
    median = dict((position, []) for position in positions)
    stdev = dict((position, []) for position in positions)

    if side == 'offense':
        df4 = def_result
    elif side == 'defense':
        df4 = off_result

    # Read in current week players with predictor variables included to run through models
    weekdf = CleanWeekDF()

    weekdf = pd.merge(left = df4, right = weekdf, left_on = 'TEAM', right_on = 'Opponent')
    weekdf = pd.merge(left = weekdf, right = stadiums, left_on = 'Location', right_on = 'location')
    
    # Remove players that aren't playing and remove unnecessary columns
    weekdf = weekdf[(weekdf['Injury Indicator'] != 'O') & (weekdf['Injury Indicator'] != 'IR')]
    #weekdf = weekdf[weekdf['Starter'] == 'Y']
    if side == 'offense':
        weekdf = weekdf[weekdf['Position'] <> 'DEF']
    elif side == 'defense':
        weekdf[weekdf['Position'] == 'DEF']
    columns = list()
    columns = (
            'Id',
            'TEAM',
            #'Starter',
            'Total_P YDS/G',
            'Total_YDS/G',
            'Total_R YDS/G',
            'Receiving_YDS/G',
            'Injury Details',
            'Injury Indicator',
            'First Name',
            'Last Name',
            'Played',
            'Game',
            'SEASON',
            'Total_PTS',
            'Total_YDS',
            'Total_YDS/G',
            'Total_PASS',
            'Total_RUSH',
            'Passing_ATT',
            'Passing_COMP',
            'Passing_YDS',
            'Passing_YDS/A',
            'Passing_LONG',
            'Passing_YDSL',
            'Rushing_ATT',
            'Rushing_YDS',
            'Rushing_YDS/A',
            'Total_YDS/G',
            'Rushing_LONG',
            'Rushing_FUM',
            'Receiving_YDS',
            'Receiving_AVG',
            'Receiving_LONG',
            'Receiving_FUM',
            'Returning_RK',
            'Returning_YDS',
            'Returning_AVG',
            'Returning_LNG',
            'Returning_TD',
            'Returning_ATT',
            'Returning_FC')
    for column in columns:
        weekdf = weekdf.drop(column, axis = 1)

    # Sort columns in order
    weekdf = weekdf.reindex_axis(sorted(weekdf.columns), axis = 1)
    
    # Create a different model for each position in data
    for position in positions:
        output_data[position] = weekdf[weekdf['Position'] == position]
        iteration = 0
        while iteration < iterations:
            
            # Player count dictionary
            playerCount = dict((position, 0) for position in positions)
            
            # Training and test set dictionaries
            train = dict((position, None) for position in positions)
            train2 = dict((position, []) for position in positions)
            train_target = dict((position, None) for position in positions)
            train_features = dict((position, None) for position in positions)
            test = dict((position, None) for position in positions)
            test2 = dict((position, []) for position in positions)
            test_target = dict((position, None) for position in positions)
            test_features = dict((position, None) for position in positions)
            all_data = dict((position, None) for position in positions)
            all_features = dict((position, None) for position in positions)
            all_data_target = dict((position, None) for position in positions)
            
            # Model dictionaries
            model_data = dict((position, None) for position in positions)
            model_data2 = dict((position, []) for position in positions)
            model_pred = dict((position, None) for position in positions)
            model_features = dict((position, None) for position in positions)
            gbm = dict((position, None) for position in positions)
            gbm_pred_train = dict((position, None) for position in positions)
            gbm_pred_test = dict((position, None) for position in positions)
            gbm_mae_train = dict((position, None) for position in positions)
            gbm_mae_test = dict((position, None) for position in positions)
            gbm_mse_train = dict((position, None) for position in positions)
            gbm_mse_test = dict((position, None) for position in positions)
            gbm_medae_train = dict((position, None) for position in positions)
            gbm_medae_test = dict((position, None) for position in positions)
            gbm_r2_train = dict((position, None) for position in positions)
            gbm_r2_test = dict((position, None) for position in positions)            
            
            model_data[position] = weekdf[weekdf['Position'] == position]
            df1[position] = df[df['Position'] == position]
            
            # Create training and test sets
            for player in set(df1[position]['Name']):
                playerCount[player] = df1[position]['Name'][df1[position]['Name'] == player].count()
        
                # Only include players that show up more than once
                if playerCount[player] > 1:
                    df2[player] = df1[position][df1[position]['Name'] == player]
                    try:
                        train[position] = train[position].append(TrainingSet(math.floor(playerCount[player]*0.7), df2[player]))
                        all_data[position] = all_data[position].append(TrainingSet(playerCount[player], df2[player]))
                        all_data_target[position] = all_data_target[position].append(df2[player]['FD points'])
                    except:
                        train[position] = TrainingSet(math.floor(playerCount[player]*0.7), df2[player])
                        all_data[position] = TrainingSet(playerCount[player], df2[player])
                        all_data_target[position] = df2[player]['FD points']
                
                    # Find indices not in training set that should be included in test set
                    for index in df2[player].index:
                        if index not in train[position].index:
                            try:
                                test[position] = test[position].append(df2[player].loc[[index]])
                                test_target[position] = test_target[position].append(df2[player].loc[[index]]['FD points'])
                            except:
                                test[position] = df2[player].loc[[index]]
                                test_target[position] = df2[player].loc[[index]]['FD points']
                        else:
                            try:
                                train_target[position] = train_target[position].append(df2[player].loc[[index]]['FD points'])
                            except:
                                train_target[position] = df2[player].loc[[index]]['FD points']
                else:
                    all_data[position] = all_data[position][all_data[position]['Name'] <> player]
        
            # Convert data frame vectors to lists to pass into models
            train_target[position] = train_target[position].values.T.tolist()
            test_target[position] = test_target[position].values.T.tolist()
        
            # Use only columns determined to be relevant predictors for each position.  Drop all columns in list below.
            columns = list()
            if position == 'QB':
                # Include passing and rushing metrics
                columns = (
                        'Position',
                        'Oppt',
                        'FD points',
                        'Receiving_RK',
                        'Receiving_REC',
                        'Receiving_TD',
                        'Receiving_FUML',
                        'Passing_SACK')
            elif position == 'RB':
                # Include rushing and receiving metrics
                columns = (
                        'Position',
                        'Oppt',
                        'FD points',
                        'Passing_RK',
                        'Passing_PCT',
                        'Passing_TD',
                        'Passing_INT',
                        'Passing_RATE',
                        'Passing_SACK')
            elif (position == 'WR') or (position == 'TE'):
                # Include only receiving metrics
                columns = (
                        'Position',
                        'Oppt',
                        'FD points',
                        'Passing_RK',
                        'Passing_PCT',
                        'Passing_TD',
                        'Passing_INT',
                        'Passing_RATE',
                        'Rushing_RK',
                        'Rushing_YDS/A',
                        'Rushing_TD',
                        'Rushing_YDS/G',
                        'Rushing_FUML',
                        'Passing_SACK')
            elif position == 'K':
                # Return only kicking metrics
                columns = (
                        'Position',
                        'Oppt',
                        'FD points',
                        'Passing_RK',
                        'Passing_PCT',
                        'Passing_TD',
                        'Passing_INT',
                        'Passing_RATE',
                        'Passing_YDS/G',
                        'Rushing_RK',
                        'Rushing_YDS/A',
                        'Rushing_TD',
                        'Rushing_YDS/G',
                        'Rushing_FUML',
                        'Receiving_RK',
                        'Receiving_REC',
                        'Receiving_TD',
                        'Receiving_FUML',
                        'Passing_SACK')
            elif position == 'DEF':
                # Include relevant metrics from opposing offense
                columns = (
                        'Position',
                        'Oppt',
                        'FD points',
                        'Receiving_TD',
                        'Passing_TD',
                        'Rushing_TD',
                        'Rushing_YDS/G',
                        'Passing_YDS/G',
                        'Total_YDS/G',
                        'Rushing_YDS/G',
                        'Passing_YDS/G',
                        'Receiving_REC',
                        'Receiving_RK',
                        'Rushing_RK',
                        'Passing_RK')
        
            # Drop columns
            for column in columns:
                try:
                    train[position] = train[position].drop(column, axis = 1)
                except:
                    Exception
                try:
                    test[position] = test[position].drop(column, axis = 1)
                except:
                    Exception
                try:
                    model_data[position] = model_data[position].drop(column, axis = 1)
                except:
                    Exception
                try:
                    all_data[position] = all_data[position].drop(column, axis = 1)
                except:
                    Exception
                
            # Convert string predictors to numeric for regression models
            dv = DictVectorizer(sparse = False)
            
            # Current week data to be passed through the model
            model_data[position] = model_data[position].convert_objects(convert_numeric = True)
            model_data[position] = dv.fit_transform(model_data[position].to_dict(orient = 'records'))
            model_features[position] = dv.get_feature_names()
            
            # Training set
            train[position] = train[position].convert_objects(convert_numeric = True)
            train[position] = dv.fit_transform(train[position].to_dict(orient = 'records'))
            train_features[position] = dv.get_feature_names()
        
            # Test set    
            test[position] = test[position].convert_objects(convert_numeric = True)
            test[position] = dv.fit_transform(test[position].to_dict(orient = 'records'))
            test_features[position] = dv.get_feature_names()
    
            # Full data set    
            all_data[position] = all_data[position].convert_objects(convert_numeric = True)
            all_data[position] = dv.fit_transform(all_data[position].to_dict(orient = 'records'))
            all_features[position] = dv.get_feature_names()
            
            ### CLEAN ALL OF THE DIFFERENT DATASETS. ###
        
            # Remove features from the current week data to be passed through the model that do not exist in the other set
            # so that there is a consistent number of predictors.
            model_data[position], model_features[position] = CleanData(position, model_data, model_features, test_features)
            model_data[position], model_features[position] = CleanData(position, model_data, model_features, train_features)
            test[position], test_features[position] = CleanData(position, test, test_features, model_features)
            train[position], train_features[position] = CleanData(position, train, train_features, model_features)
            all_data[position], all_features[position] = CleanData(position, all_data, all_features, model_features)
    
        ### ========================================================= ###
        ###                      TRAIN MODELS                         ### 
        ### ========================================================= ###
        
            # Create a different model for every position in list
        
            #### GENERALIZED LINEAR MODEL ###
            #lm = linear_model.LinearRegression()
            #lm.fit(train, train_target)
            #pred_train_lm = lm.predict(train)
            #pred_test_lm = lm.predict(test)
            #print('MSE on ' + str(position) + ' training set of ' + str(np.mean((pred_train_lm - train_target)**2)))
            #print('MSE on ' + str(position) + ' test set of ' + str(np.mean((pred_test_lm - test_target)**2)))
        
            ### GRADIENT BOOSTED MACHINE ###
            params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 1, 'learning_rate': 0.01, 'loss': 'ls'}
            gbm[position] = ensemble.GradientBoostingRegressor(**params)
            gbm[position].fit(train[position], train_target[position])
            gbm_pred_train[position] = gbm[position].predict(train[position])
            gbm_pred_test[position] = gbm[position].predict(test[position])
        
            #### SUPPORT VECTOR MACHINE ###
            #clf = svm.SVC()
            #clf.fit(train, train_target)
            #pred_train_svm = clf.predict(train)
            #pred_test_svm = clf.predict(test)
    
        ### ========================================================= ###
        ###                     EVALUATE MODELS                       ### 
        ### ========================================================= ###
        
            # Put all of the metrics of the various models in dictionaries by position
        
            # Mean absolute error
            gbm_mae_train[position] = metrics.mean_absolute_error(train_target[position], gbm_pred_train[position])
            gbm_mae_test[position] = metrics.mean_absolute_error(test_target[position], gbm_pred_test[position])
            
            # Mean squared error
            gbm_mse_train[position] = metrics.mean_squared_error(train_target[position], gbm_pred_train[position])
            gbm_mse_test[position] = metrics.mean_squared_error(test_target[position], gbm_pred_test[position])
        
            # Median absolute error
            gbm_medae_train[position] = metrics.median_absolute_error(train_target[position], gbm_pred_train[position])
            gbm_medae_test[position] = metrics.median_absolute_error(test_target[position], gbm_pred_test[position])
        
            # R-squared
            gbm_r2_train[position] = metrics.r2_score(train_target[position], gbm_pred_train[position])
            gbm_r2_test[position] = metrics.r2_score(test_target[position], gbm_pred_test[position])
    
    ### ========================================================= ###
    ###                         RUN MODEL                         ### 
    ### ========================================================= ###

            ### GRADIENT BOOSTED MACHINE ###
            params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 1, 'learning_rate': 0.01, 'loss': 'ls'}
            gbm[position] = ensemble.GradientBoostingRegressor(**params)
            gbm[position].fit(all_data[position], all_data_target[position])
        
            # Use best model to run projection on current week of data
            model_pred[position] = gbm[position].predict(model_data[position])
    
    ### ========================================================= ###
    ###                       WRITE OUTPUT                        ### 
    ### ========================================================= ###

            # Set correct indices for model predictions, and convert it to a dataframe
            model_pred[position] = pd.DataFrame(model_pred[position]).set_index(output_data[position].index, append = False)
            model_pred[position].rename(columns = {0:colName + ' ' + str(iteration + 1)}, inplace = True)
            output_data[position] = pd.concat([output_data[position], model_pred[position]], axis = 1)

            iteration += 1

        # Add statistical metrics to dataset
        count = 0
        while count < len(output_data[position]):
            mean[position].append(np.mean(output_data[position].reset_index().loc[count, colName + ' ' + str(1):colName + ' ' + str(iterations)]))
            median[position].append(np.median(output_data[position].reset_index().loc[count, colName + ' ' + str(1):colName + ' ' + str(iterations)])        )
            stdev[position].append(np.std(output_data[position].reset_index().loc[count, colName + ' ' + str(1):colName + ' ' + str(iterations)])        )
            count += 1
            
        mean[position] = pd.DataFrame({'Mean':mean[position]}).set_index(output_data[position].index, append = False)
        median[position] = pd.DataFrame({'Median':median[position]}).set_index(output_data[position].index, append = False)
        stdev[position] = pd.DataFrame({'Standard Deviation':stdev[position]}).set_index(output_data[position].index, append = False)    
        output_data[position] = pd.concat([output_data[position], mean[position], median[position], stdev[position]], axis = 1)

        # Remove unnecessary columns from output data
        columns = list()
        columns = (
                'Passing_INT',
                'Passing_PCT',
                'Passing_RATE',
                'Passing_RK',
                'Passing_SACK',
                'Passing_TD',
                'Passing_YDS/G',
                'Receiving_FUML',
                'Receiving_REC',
                'Receiving_RK',
                'Receiving_TD',
                'Rushing_FUML',
                'Rushing_RK',
                'Rushing_TD',
                'Rushing_YDS/G',
                'Total_PTS/G',
                'Total_RK',
                'h/a',
                'roof_type',
                'surface_type',
                'location')
                
        for column in columns:
            if column in output_data[position]:
                output_data[position] = output_data[position].drop(column, axis = 1)
            
    # Create dataset with positions all in one dataset
    for i, position in enumerate(output_data):
        if (i == 0) and (side == 'offense'):
            output = output_data[position]
        else:
            output = output.append(output_data[position])
    
# Write projections to csv file at end
output.to_csv(filepath + filename, index = False, sep=',', header = True)

### ========================================================= ###
###                     OPTIMIZE LINEUP                       ### 
### ========================================================= ###

# Initially was going to try to optimize in this script, but this is done in another script.
# The lineup variable below spits out the best lineup, but does not take salary cap into account.

# Position data dictionary
positions = list()
positions = set(output['Position'])

# Sort lineup dataframe by highest fantasy points
output = output.sort(['Mean'], ascending = False)
output = output.reset_index()

# Lineup dictionary
lineup = defaultdict(dict)

# Create lineup with best players by projections regardless of salary cap
for position in positions:
    plist = list()
    ptlist = list()
    slist = list()
    while len(plist) < pos_count[position]:
        for index, row in output.iterrows():
            if (row['Position'] == position) and (row['Name'] not in plist):
                plist.append(row['Name'])
                ptlist.append(row['Mean'])
                slist.append(row['Salary'])
                break
    for i, player in enumerate(plist):
        lineup[position][player] = {colName: ptlist[i], 'Salary': slist[i]}
