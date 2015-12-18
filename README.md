##Project: Fantasy Football Team Optimizer
- Brett Steele, Matt Morris, & Roderick Head
- INFO 590-34717
- December 18, 2015

####Define Problem
The most challenging aspect of owning and operating a daily fantasy football team is not having a great deal of football knowledge; it is determining the best lineup to use for the upcoming week.  Many experts weigh in with their weekly projections based on historical player performance and how they perceive the player will do given their current health and their opponent.  Many of these projections rely on player and football knowledge.  Player and football knowledge is still necessary when determining lineups, but we wanted to pursue a more data-driven approach to building a weekly lineup.  Our team sought to tackle two main problems when creating the optimal lineup:
Create a data-driven weekly player performance projection model based on historical data available.
Optimize the weekly lineup by choosing players with the highest performance projections while keeping the team under a given salary cap.

The first problem is a classic regression problem using historical data to predict future performance.  The output of this model, predicted fantasy points, is a necessary input into the second part of the problem.
The second problem is necessary because weekly fantasy football-like sites institute a team salary cap that must not be exceeded when building a team.  They also have a requirement on number of players at each position.  This is a problem with combinatorial optimization often referred to as the “knapsack problem with multiple constraints”.  Our team followed the FanDuel.com format.  Each week, every player is given a salary.  Better players have higher salaries. The crux of the second problem is to take the projections from the first model and create a team that produces the highest number of projected fantasy points while remaining within the salary cap and position constraints.

####Define Software
This project used both R (version 3.2.2) and Python (version 2.7.9) for the analysis.  Below is a list of packages from each that are required to be installed in order to run the analysis:
- R: rvest, knitr, pipeR, MASS, dplyr, tidyr, Rglpk
- Python: numpy, pandas, math, requests, re, io, sklearn, BeautifulSoup, datetime

Python is used for web scraping, data wrangling, and machine learning.  Data is pulled from the web using the BeautifulSoup package, and that data is manipulated using Python lists, dictionaries, pandas dataframes, and numpy arrays.  The sklearn machine learning package is then used to train several regression models on the data to create player performance projections.  Regression metrics such as mean squared error, mean absolute error, median squared error and R-squared, are used to evaluate which model is best to use to create the projections.

R is used to do the linear optimization problem to find the optimal lineup given the projections and lineup constraints.  The projections from Python are pulled in and the constraints are defined.  The Rglpk package is then used to run the linear optimization and output the optimal lineup.

####Documentation
#####Github Project Location: [Project Fantasy](https://github.com/brttstl/proj-fantasy)
######Part 1: Web Scraping
######Script Location: [Projections.py](https://github.com/brttstl/proj-fantasy/blob/master/3.projections/projections.py)
This script scrapes several web pages for data input into the regression model.  Below are the sources it pulls from:
- [ESPN](espn.go.com/nfl/statistics/team/_/stat/)
   Historical (from current season) team aggregate data. Used for opponent team statistics.
- [Fox Sports Depth Charts](http://www.foxsports.com/fantasy/football/commissioner/Players/DepthCharts.aspx)
   Current week depth charts.  Used to determine where a player fits on the team’s roster.  Below shows which players are considered in this model:
  - Quarterbacks: only starters
  - Running backs: starters and backups
  - Wide Receivers: WR1, WR2, WR3, and reserves
  - Tight Ends: starters and reserves
  - Kickers: only starters
- [RotoGuru](http://rotoguru1.com/cgi-bin/fyday.pl)
   FanDuel.com historical player performance and salary.  Player performance used as target variable in projection models.

######Part 2: Projections Model
Script Location: [Projections.py](https://github.com/brttstl/proj-fantasy/blob/master/3.projections/projections.py)
- External data inputs:
  - [NFL stadium attributes](https://raw.githubusercontent.com/brttstl/proj-fantasy/master/data/stadiums.csv)
  - [Eligible FanDuel Player List](https://github.com/brttstl/proj-fantasy/blob/master/data/FanDuel-NFL-2015-12-20-13996-players-list.csv)
    List of the next week’s available players (week to project for).  In this case, it is week 15 of the 2015 NFL season.

- Output: Next week’s projections in a csv format to folder set by user in one of the first lines of code within the script.

How it works:
1. Gather user input.  In the first several lines of code within the script, the user inputs the week to create projections for and the file path of where the csv will be saved.  It is worth noting that the projections can only be created for weeks that FanDuel has the player and salary list published.  Typically, this is the upcoming week of the season.  No data is available for weeks that are far off.
2. Scrape the web.  The script scrapes ESPN.com for offense and defense season statistics for each team.  These statistics are used as predictors for a player that is matched up against that team.  For instance, a running back that is facing the Chicago Bears will have various Chicago Bears rushing defense statistics passed through the model when determining that player’s projected points for the week.
3. Clean and merge datasets.  The datasets that were retrieved from scraping within this script and the datasets that were pulled from Github require some cleaning in order to remove columns that are not required in the model as predictors and to clean up variables that will be used to join the datasets.  Additional columns are also appended.  For instance, whether the player is at home or away is determined based on which team they are on and the location of the game.
4. Prepare training and test sets for regression model.  A training set that matches 70% of the data available for each player is created.  The remaining data is used on the test set.
5. Run several different regression models.  In this analysis a gradient boosting machine and a generalized linear model were both tested.  The parameters of the gradient boosting machine were tweaked for several different trials to optimize this model.  A different model was created for each different player position.  The models were run on a training set that was comprised of 70% of the available data for each player, and the test set was the remaining 30% of the available data.
6. Evaluate models.  Metrics were used to determine which model performed the best at creating projections.  The metrics reviewed were mean absolute error, mean squared error, median absolute error and R2.  A chart with that compares the mean squared error between the different models can be found at the end of this report.
7. Run best model on data to create projections.  Based on the metrics evaluating the different models, the gradient boosting machine with the following parameters was deemed the best model:
  - n_estimators = 250
  - max_depth = 3
  - min_samples_split = 1
  - learning_rate = 0.01
This model was used on all of the available data to create player point projections for the next week.  Once again, a different model was created for each player position.
8. Append statistical measures of multiple iterations of model to output dataset.  In this analysis, the determined best model was run 10 times.  The number of iterations can be manually changed by changing the value of the variable ‘iterations’ within the script, though 10 was determined to be sufficient.  The projections of each iteration were included, and the mean, median, and standard deviation of projections for each player were appended.  How these are used is detailed in the section about the lineup optimizer script.
9. Write output projections to csv file.  The final dataset with players, projections, and statistical measures is written to a csv file at a location specified by the user.  This csv file is then read into the lineup optimizer script.
