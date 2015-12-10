library(Rglpk)
library(dplyr)

players <- read.csv("/Users/brett/GitHub/proj-fantasy/final/player_pool.csv", header = TRUE, ",", skipNul = FALSE, stringsAsFactors = FALSE)
num.x <- length(players$position)

# objective:
obj <- players$projection
# the vars are represented as booleans
var.types <- rep("B", num.x)
# the constraints
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

sol <- Rglpk_solve_LP(obj = obj, mat = matrix, dir = direction, rhs = rhs,
                      types = var.types, max = TRUE)

optimal <- players[sol$solution==1,]
write.csv(optimal,"/Users/brett/GitHub/proj-fantasy/final/optimized.csv")