##Project: Fantasy Football Team Optimizer
- Brett Steele, Matt Morris, & Roderick Head
- INFO 590-34717
- December 18, 2015

####Software
This project used both R ([version 3.2.2]()) and Python (version 2.7.9) for the analysis.  Below is a list of packages from each that are required to be installed in order to run the analysis:
- Python:
  - BeautifulSoup
  - datetime
  - io
  - math
  - numpy
  - pandas
  - re
  - requests
  - sklearn
- R:
  - dplyr
  - Rglpk

Python is used for web scraping, data wrangling, and machine learning.  Data is pulled from the web using the BeautifulSoup package, and that data is manipulated using Python lists, dictionaries, pandas dataframes, and numpy arrays.  The sklearn machine learning package is then used to train several regression models on the data to create player performance projections.  Regression metrics such as mean squared error, mean absolute error, median squared error and R-squared, are used to evaluate which model is best to use to create the projections.

R is used to do the linear optimization problem to find the optimal lineup given the projections and lineup constraints.  The projections from Python are pulled in and the constraints are defined.  The Rglpk package is then used to run the linear optimization and output the optimal lineup.

####Instructions
Below are instructions on how to run all stages of the program from start to finish.  The end result will be: 1) an optimal fantasy football lineup based on FanDuel.com scoring and salary system and 2) a list of all of the players for the current week from FanDuel.com with projections based on output from the regression model.

  1. Install all necessary Python and R packages (see package list near beginning of report)
  2. Download FanDuel.com’s latest player list.  To do this simply visit [FanDuel.com](https://www.fanduel.com) and click:
    1. Login (or create username if necessary)
    2. Click first contest ($1.75M NFL Sunday Million)
    3. Enter this contest
    4. Click “Download players list” link near the top middle of page.
  3. Upload the players list downloaded in step 2 to Github.
  4. Open python file [projections.py](https://github.com/brttstl/proj-fantasy/blob/master/3.projections/projections.py).  Go to lines 5-8 of the code and update these user inputs:
    * Line 5: NFL week to create projection for (week 15 in example)
    * Line 6: NFL season (2015 in example)
    * Line 7: Input file: This is the Github location of the file uploaded in step 3.
    * Line 8: Filepath: directory location of where output csv should be saved to.
    * Run script.
  5. Save output file from step 4 to Github.
  6. Open R file [optimal_lineup.r](https://github.com/brttstl/proj-fantasy/blob/master/4.lineup_optimization/optimal_lineup.r).  User inputs are required on 2 lines of the code:
    * Line 9: Output path: Designate directory of output csv file.
    * Line 12: Change location of file being read to be the location of the file saved in step 5.
    * Run script.
  7. The optimal lineup based on projections is now saved as a csv file to the location specified in step 6a.
