#### install & load packages and fix functions ####
install.packages("dplyr")
install.packages("Rglpk")

data.packages <- c('dplyr', 'Rglpk')
lapply(data.packages, library, character.only = T)

#### IMPORTANT: specify final output path here ####
output.path = "/Users/b/GitHub/proj-fantasy/3.final_optimized_lineup/optimal_lineup_mnmax.csv"

#### import output from player_projections_&_fanduel_merge.py ####
Players <- tbl_df(read.csv("/Users/b/GitHub/proj-fantasy/data/week_16_projections.csv", header = TRUE, ",", skipNul = FALSE, stringsAsFactors = FALSE))

num.x <- length(Players$Position)

#### set objective: ####
obj <- Players$Median

#### vars are represented as booleans ####
var.types <- rep("B", num.x)

#### constraints ####
matrix <- rbind(as.numeric(Players$Position == "QB"),
                as.numeric(Players$Position == "RB"),
                as.numeric(Players$Position == "WR"),
                as.numeric(Players$Position == "TE"),
                as.numeric(Players$Position == "K"),
                as.numeric(Players$Position == "DEF"),
                as.numeric(Players$Position %in% c("QB", "RB", "WR", "TE", "K", "DEF")),
                Players$Salary)

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
         1, # D
         9, # Total
         60000) #Salary         

#### solve optimal lineup ####
sol <- Rglpk_solve_LP(obj = obj, mat = matrix, dir = direction, rhs = rhs,
                      types = var.types, max = TRUE)

sol

optimal <- Players[sol$solution==1,]
optimal
#### return and write optimal lineup for game ####
write.csv(optimal[,4:8], output.path, row.names = FALSE)