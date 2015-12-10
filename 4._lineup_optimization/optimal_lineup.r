#### load packages and fix functions ####
data.packages <- c('dplyr', 'Rglpk')
lapply(data.packages, library, character.only = T)

#### IMPORTANT: specify final output path here ####
output.path = "/Users/brett/GitHub/proj-fantasy/5._final_optimized_lineup/optimal_lineup.csv"

#### set file path for reproducibility ####
mypath = file.path("/Users", "brett", "GitHub", "proj-fantasy", "final")

#### import output from player_projections_&_fanduel_merge.py ####
players <- read.csv("https://raw.githubusercontent.com/brttstl/proj-fantasy/master/data/player_pool.csv", header = TRUE, ",", skipNul = FALSE, stringsAsFactors = FALSE)
num.x <- length(players$position)

#### set objective: ####
obj <- players$projection

#### vars are represented as booleans ####
var.types <- rep("B", num.x)

#### constraints ####
matrix <- rbind(as.numeric(players$position == "QB"),
                as.numeric(players$position == "RB"),
                as.numeric(players$position == "WR"),
                as.numeric(players$position == "TE"),
                as.numeric(players$position == "K"),
                as.numeric(players$position == "DEF"),
                as.numeric(players$position %in% c("QB", "RB", "WR", "TE", "K", "DEF")),  
                players$salary)                  

direction <- c("==",
               "==",
               "==",
               "==",
               "==",
               "==",
               "==",
               "<=")

rhs <- c(1, # QB
         2, # RB
         3, # WR
         1, # TE
         1, # K
         1, # Def
         9, # Total
         60000)               

#### solve optimal lineup ####
sol <- Rglpk_solve_LP(obj = obj, mat = matrix, dir = direction, rhs = rhs,
                      types = var.types, max = TRUE)

#### return and write optimal lineup for game ####
optimal <- tbl_df(players[sol$solution==1,])

write.csv(optimal, output.path)