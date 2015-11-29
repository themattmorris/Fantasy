data.packages <- c('dplyr', 'ggplot2', 'RColorBrewer', 'ggthemes', 'scales', 'tidyr', 'MASS', 'devtools', 'lubridate')
lapply(data.packages, library, character.only = T)

## redefine select from dplyr because MASS package causes issues
select <- dplyr::select

## import raw data as a table
Salary <- tbl_df(read.csv("/Users/brett/GitHub/proj-fantasy/salary.csv", header = TRUE, ";", skipNul = FALSE, stringsAsFactors = FALSE))

#### clean up
## remove gid column and filter out def for name format reshape remove salaries that are 0 as these players weren't available
no.def <- Salary %>%
  select(Season = Year, Week, Name, Position = Pos, Team, Home.Away = h.a, Opponent = Oppt, FanDuel.pts = FD.points, FanDuel.sal = FD.salary) %>% 
  filter(Position %in% c("QB", "RB", "WR", "TE", "PK"), FanDuel.sal >= 1)

def <- Salary %>%
  select(Season = Year, Week, Name, Position = Pos, Team, Home.Away = h.a, Opponent = Oppt, FanDuel.pts = FD.points, FanDuel.sal = FD.salary) %>% 
  filter(Position == "Def", FanDuel.sal >= 1)

## split names by comma
split <- no.def %>%
  separate(Name, c("last", "first"), ", ")
## and rearrange in first last format
reorg <- split %>%
  unite(Name, first, last, sep = " ")

## bind defense rows + first last name rows
clean <- rbind(reorg, def)

## lookup tables
library(devtools, quietly=TRUE)
source_gist("https://gist.github.com/dfalster/5589956")
allowedVars <- c("Name", "Position", "Home.Away")
clean.lu <- addNewData("/Users/brett/GitHub/proj-fantasy/lookup_table.csv", clean, allowedVars)

## format columns to match profootball reference export
clean.lu$Season <- as.integer(clean.lu$Season)
clean.lu$Week <- as.integer(clean.lu$Week)
clean.lu$Position <- factor(clean.lu$Position, levels = c("QB", "RB", "WR", "TE", "K", "DEF"))
clean.lu$Team <- as.factor(toupper(clean.lu$Team))
clean.lu$Opponent <- as.factor(toupper(clean.lu$Opponent))
clean.lu$Home.Away <- as.factor(clean.lu$Home.Away)
clean.lu$FanDuel.pts <- as.double(clean.lu$FanDuel.pts)
clean.lu$FanDuel.sal <- as.double(clean.lu$FanDuel.sal)

## save cleaned fanduel output
write.csv(clean.lu, "/Users/brett/GitHub/proj-fantasy/fanduel_2015_season_summary.csv")

## import profootref data
PFR <- tbl_df(read.csv("/Users/brett/GitHub/proj-fantasy/fantasy_data.csv", header = TRUE, skipNul = FALSE, stringsAsFactors = FALSE))

## have to add home.away for a min because i'm lazy and want to reuse lookup table
Home.Away <- c(" ")
pfr.data <- cbind(PFR, Home.Away)

pfr.data <- pfr.data %>%
  mutate(Home.Away = "") %>%
  filter(position %in% c("QB", "RB", "FB", "WR", "TE", "KR", "K", "P", "CB", "DEF") & season == "2015") %>%
  select(Name = player, Date = date, Location = location, cmp:pts_allowed, Season = season, Week = week, Position = position, Home.Away)

## lookup tables for fb's and kr's
source_gist("https://gist.github.com/dfalster/5589956")
allowedVars <- c("Name", "Position", "Home.Away")
pfr.lu <- addNewData("/Users/brett/GitHub/proj-fantasy/lookup_table.csv", pfr.data, allowedVars)

## drop Home.Away column
pfr.clean <- pfr.lu %>%
  select(-Home.Away, -Position)

## join data from profootball reference into fanduel data set of players
fan.full <- full_join(clean.lu, pfr.clean, by = c("Name", "Week", "Season"))

## convert columns of full
fan.full$Week <- factor(fan.full$Week, levels = c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"))
fan.full$Location <- as.factor(fan.full$Location)
fan.full$off_snap_count_pct <- as.numeric(substr(fan.full$off_snap_count_pct,0,nchar(fan.full$off_snap_count_pct)-1))
fan.full$def_snap_count_pct <- as.numeric(substr(fan.full$def_snap_count_pct,0,nchar(fan.full$def_snap_count_pct)-1))
fan.full$Date <- as.Date(fan.full$Date, "%m/%d/%Y")

## quick cliean
full.data <- fan.full %>%
  select(week = Week, name = Name, position = Position, team = Team, home.away = Home.Away, opponent = Opponent, fanduel.pts = FanDuel.pts, fanduel.sal = FanDuel.sal, date = Date, location = Location, cmp:pts_allowed)

## output full data here
write.csv(full.data, "/Users/brett/GitHub/proj-fantasy/fully_merged.csv")