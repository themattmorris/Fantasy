### ========================================================= ###
###                      IMPORT PACKAGES                      ### 
### ========================================================= ###

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn import metrics, linear_model, svm, ensemble
from sklearn.feature_extraction import DictVectorizer

### ========================================================= ###
###                  INITIALIZE VARIABLES                     ### 
### ========================================================= ###

salCap = 60000 # dollars

# Number of players by position in lineup
QB = 1
RB = 2
WR = 3
TE = 1
K = 1
DEF = 1

### ========================================================= ###
###                      FUNCTIONS                            ### 
### ========================================================= ###

def TrainingSet(n, df):

        # Creates random sample of records from the input dataframe    
        return df.ix[np.random.choice(df.index, n, replace = False)]


def CleanData(position, df, df_features, df_compare_features):

    # Goes through feature lists and removes any predictors that are not also included in the comparison feature list
    # This is done so that the model data, training set, and test set all have the same predictors.

    lst = list()
    count = -1

    # Intialize boolean array length of input array to be hit against input array to pull only True values out
    mask = np.ones(len(df_features[position]), dtype = bool)
    for feature in df_features[position]:
        count += 1
        if feature not in df_compare_features[position]:
            mask[count] = False
            
    player_count = 0
    while player_count < len(df[position]):
        lst.append(df[position][player_count][mask])
        player_count += 1
        
    return np.asarray(lst)

### ========================================================= ###
###                     PREPARE DATA                          ### 
### ========================================================= ###

# Go through both offense and defense
sides = list()
sides = ('offense', 'defense')

for side in sides:

    # Read in historical csv file
    df = pd.read_csv('C:/Users/Matt/Documents/Documents/College Crap/Indiana University/Final Project/proj-fantasy/historical_' + str(side) + '_data.txt')
    
    # Position data dictionary
    positions = list()
    positions = set(df['Position'])
    
    model_data = dict((position, 0) for position in positions)
    
    maxWeek = max(set(df['Week']))
    curWeek = maxWeek + 1
    
    # Read in current week players with predictor variables included to run through models
    weekdf = pd.read_csv('C:/Users/Matt/Documents/Documents/College Crap/Indiana University/Final Project/proj-fantasy/Week' + str(curWeek) + '_' + str(side) + '_query.txt')
    
    # Position data dictionary
    df1 = dict((position, 0) for position in positions)
    
    df2 = dict((position, 0) for position in positions)
    
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
    
    # Output dictionary
    output_data = dict((position, None) for position in positions)
    
    # Create a different model for each position in data
    for position in positions:
        model_data[position] = weekdf[weekdf['Position'] == position]
        output_data[position] = model_data[position]
        df1[position] = df[df['Position'] == position]
        
        # Create training and test sets
        for player in set(df1[position]['Name']):
            playerCount[player] = df1[position]['Name'][df1[position]['Name'] == player].count()
    
            # Only include players that show up more than once
            if playerCount[player] > 1:
                df2[player] = df1[position][df1[position]['Name'] == player]
                try:
                    train[position] = train[position].append(TrainingSet(math.floor(playerCount[player]*0.7), df2[player]))
                except:
                    train[position] = TrainingSet(math.floor(playerCount[player]*0.7), df2[player])
            
                # Find indices not in training set that should be included in test set
                for index in df2[player].index:
                    if index not in train[position].index:
                        try:
                            test[position] = test[position].append(df2[player].loc[[index]])
                            test_target[position] = test_target[position].append(df2[player].loc[[index]]['FanDuelpts'])
                        except:
                            test[position] = df2[player].loc[[index]]
                            test_target[position] = df2[player].loc[[index]]['FanDuelpts']
                    else:
                        try:
                            train_target[position] = train_target[position].append(df2[player].loc[[index]]['FanDuelpts'])
                        except:
                            train_target[position] = df2[player].loc[[index]]['FanDuelpts']
    
        # Convert data frame vectors to lists to pass into models
        train_target[position] = train_target[position].values.T.tolist()
        test_target[position] = test_target[position].values.T.tolist()
    
        # Use only columns determined to be relevant predictors for each position.  Drop all columns in list below.
        columns = list()
        if position == 'QB':
            # Include passing and rushing metrics
            columns = ('Position', 'Opponent', 'First Name', 'Last Name', 'cmp', 'pass_att', 'pass_yd', 'pass_td', 'int_thrown', 'rush_att', 'rush_yd', 'rush_td', 'targets', 'receptions', 'rec_yd', 'rec_td', 'fumbles_lost', 'kick_ret_td', 'punt_ret_td', 'xpm', 'xpa', 'fgm', 'fga', 'off_snap_count', 'def_snap_count', 'st_snap_count', 'qbr', 'traditional_fantasy_points', 'two_pt_conv', 'FanDuelpts', 'Receiving_RK', 'Receiving_REC', 'Receiving_AVG', 'Receiving_TD', 'Receiving_FUML', 'Kickoff_Return_AVG', 'Kickoff_Return_TD', 'Punt_Return_AVG', 'Punt_Return_TD', 'Week')
        elif position == 'RB':
            # Include rushing, receiving, and return metrics
            columns = ('Position', 'Opponent', 'First Name', 'Last Name', 'cmp', 'pass_att', 'pass_yd', 'pass_td', 'int_thrown', 'rush_att', 'rush_yd', 'rush_td', 'targets', 'receptions', 'rec_yd', 'rec_td', 'fumbles_lost', 'kick_ret_td', 'punt_ret_td', 'xpm', 'xpa', 'fgm', 'fga', 'off_snap_count', 'def_snap_count', 'st_snap_count', 'qbr', 'traditional_fantasy_points', 'two_pt_conv', 'FanDuelpts', 'Passing_RK', 'Passing_PCT', 'Passing_YDS/A', 'Passing_TD', 'Passing_INT', 'Passing_RATE', 'Week')
        elif (position == 'WR') or (position == 'TE'):
            # Include receiving and return metrics
            columns = ('Position', 'Opponent', 'First Name', 'Last Name', 'cmp', 'pass_att', 'pass_yd', 'pass_td', 'int_thrown', 'rush_att', 'rush_yd', 'rush_td', 'targets', 'receptions', 'rec_yd', 'rec_td', 'fumbles_lost', 'kick_ret_td', 'punt_ret_td', 'xpm', 'xpa', 'fgm', 'fga', 'off_snap_count', 'def_snap_count', 'st_snap_count', 'qbr', 'traditional_fantasy_points', 'two_pt_conv', 'FanDuelpts', 'Total_R YDS/G', 'Passing_RK', 'Passing_PCT', 'Passing_YDS/A', 'Passing_TD', 'Passing_INT', 'Passing_RATE', 'Rushing_RK', 'Rushing_ATT', 'Rushing_YDS/A', 'Rushing_TD', 'Rushing_FUML', 'Week')
        elif position == 'K':
            # Return only kicking metrics
            columns = ('Position', 'Opponent', 'First Name', 'Last Name', 'cmp', 'pass_att', 'pass_yd', 'pass_td', 'int_thrown', 'rush_att', 'rush_yd', 'rush_td', 'targets', 'receptions', 'rec_yd', 'rec_td', 'fumbles_lost', 'kick_ret_td', 'punt_ret_td', 'xpm', 'xpa', 'fgm', 'fga', 'off_snap_count', 'def_snap_count', 'st_snap_count', 'qbr', 'traditional_fantasy_points', 'two_pt_conv', 'FanDuelpts', 'Total_P YDS/G', 'Total_R YDS/G', 'Passing_RK', 'Passing_PCT', 'Passing_YDS/A', 'Passing_TD', 'Passing_INT', 'Passing_RATE',  'Rushing_RK', 'Rushing_ATT', 'Rushing_YDS/A', 'Rushing_TD', 'Rushing_FUML', 'Receiving_RK', 'Receiving_REC', 'Receiving_AVG', 'Receiving_TD', 'Receiving_FUML', 'Kickoff_Return_AVG', 'Kickoff_Return_TD', 'Punt_Return_AVG', 'Punt_Return_TD', 'Week')
        elif position == 'DEF':
            columns = ('Position', 'opponent', 'First Name', 'Last Name', 'Week', 'FanDuelpts')
    
        for column in columns:
            train[position] = train[position].drop(column, axis = 1)
            test[position] = test[position].drop(column, axis = 1)
            try:
                # All columns that are being dropped in train and test should be dropped in the current week dataframe to be ran through the model.
                # However, this dataframe has fewer columns than the train and test sets, so attempting to drop some will throw an error.
                model_data[position] = model_data[position].drop(column, axis = 1)
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
        
        ### CLEAN THE THREE DIFFERENT DATASETS. ###
    
        # Remove features from the current week data to be passed through the model that do not exist in the training set
        train[position] = CleanData(position, train, train_features, model_features)
        model_data[position] = CleanData(position, model_data, model_features, train_features)
        test[position] = CleanData(position, test, test_features, model_features)
    
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
    
        # Use best model to run projection on current week of data
        model_pred[position] = gbm[position].predict(model_data[position])
    
    ### ========================================================= ###
    ###                       WRITE OUTPUT                        ### 
    ### ========================================================= ###
    
        # Set correct indices for model predictions, and convert it to a dataframe
        model_pred[position] = pd.DataFrame(model_pred[position]).set_index(output_data[position].index, append = False)
        model_pred[position].rename(columns = {0:'Projection'}, inplace = True)
        output_data[position] = pd.concat([output_data[position], model_pred[position]], axis = 1)
        
    # Create dataset with positions all in one dataset
    count = 0
    for position in output_data:
        if count == 0:
            output = output_data[position]
        else:
            output = output.append(output_data[position])
        count += 1
    
    # Read in current week players to append projections to
    outdf = pd.read_csv('C:/Users/Matt/Documents/Documents/College Crap/Indiana University/Final Project/proj-fantasy/FanDuel_2015_Week' + str(curWeek) + '.csv')
    outdf = outdf.drop('Starter', axis = 1)
    
    # Remove all unnecessary columns from dataframe before writing
    columns = list()
    columns = ('Name', 'Projection')
    
    for col in output.columns:
        if col not in columns:
            output = output.drop(col, axis = 1)
    
    # Merge dataframes together
    outdf = pd.merge(output, outdf, on = 'Name')
    
    # Write output to csv file
    if side == 'offense':
        outdf.to_csv('C:/Users/Matt/Documents/Documents/College Crap/Indiana University/Final Project/proj-fantasy/Week' + str(curWeek) + '_projections.csv', index = False, sep=',', header = True)
    elif side == 'defense':
        with open('C:/Users/Matt/Documents/Documents/College Crap/Indiana University/Final Project/proj-fantasy/Week' + str(curWeek) + '_projections.csv', 'a') as f:
            outdf.to_csv(f, index = False, header = False)
