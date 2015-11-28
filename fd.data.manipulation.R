data.packages <- c('dplyr', 'ggplot2', 'RColorBrewer', 'ggthemes', 'scales', 'tidyr', 'MASS')
lapply(data.packages, library, character.only = T)

## redefine select from dplyr because MASS package causes issues
select <- dplyr::select

## import raw data as a table
Salary <- tbl_df(read.csv("/Users/brett/GitHub/proj-fantasy/Salary.csv", header = TRUE, ";", skipNul = FALSE, stringsAsFactors = FALSE))

## cleaned up; removed extra rows, columns; renamed column headers with context
fd.sal <- Salary %>%
  select(Week, Name, Position = Pos, Team, Home.Away = h.a, Opponent = Oppt, FanDuel.pts = FD.points, FanDuel.sal = FD.salary)

## convert columns to relevant data formats
fd.sal$Week <- factor(fd.sal$Week, levels = c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"))
fd.sal$Position <- factor(fd.sal$Position, levels = c("QB", "RB", "WR", "TE", "PK", "Def"))
fd.sal$Team <- as.factor(fd.sal$Team)
fd.sal$Home.Away <- as.factor(fd.sal$Home.Away)
fd.sal$Opponent <- as.factor(fd.sal$Opponent)
fd.sal$FanDuel.pts <- as.double(fd.sal$FanDuel.pts)
fd.sal$FanDuel.sal <- as.double(fd.sal$FanDuel.sal)

## remove any salary that is less than 0; as these players either aren't players or weren't available
fd.data <- fd.sal %>%
  filter(FanDuel.sal >= 1)
glimpse(fd.data)

## output data here
write.csv(fd.data, "/Users/brett/GitHub/proj-fantasy/FanDuel 2015 Season Summary.csv")