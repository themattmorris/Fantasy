#### load packages and fix functions ####
data.packages <- c('dplyr', 'ggplot2', 'RColorBrewer', 'RCurl', 'ggthemes', 'ggExtra', 'gridExtra', 'scales', 'tidyr', 'MASS', 'devtools', 'lubridate', 'mosaic')
lapply(data.packages, library, character.only = T)

## redefine select from dplyr because MASS package causes issues
select <- dplyr::select

#### IMPORTANT: specify final output path here ####
output.path = "/Users/brett/GitHub/proj-fantasy/data/fanduel_2015_season_summary.csv"
lookup.table.path = "/Users/brett/GitHub/proj-fantasy/data/lookup_table.csv"

#### bring in salary data from fanduel ####
## get data from github and import as a table
salary <- tbl_df(read.csv("https://raw.githubusercontent.com/brttstl/proj-fantasy/master/data/salary.csv", header = TRUE, ";", skipNul = FALSE, stringsAsFactors = FALSE))

#### clean up ####
## remove gid column and filter out def for name format reshape remove salaries that are 0 as these players weren't available
no.def <- salary %>%
  select(Season = Year, Week, Name, Position = Pos, Team, Home.Away = h.a, Opponent = Oppt, FanDuel.pts = FD.points, FanDuel.sal = FD.salary) %>% 
  filter(Position %in% c("QB", "RB", "WR", "TE", "PK"), FanDuel.sal >= 1)

def <- salary %>%
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
fully.cleaned <- addNewData(lookup.table.path, clean, allowedVars)

## format columns to match profootball reference export
fully.cleaned$Season <- as.integer(fully.cleaned$Season)
fully.cleaned$Week <- as.integer(fully.cleaned$Week)
fully.cleaned$Position <- factor(fully.cleaned$Position, levels = c("QB", "RB", "WR", "TE", "K", "DEF"))
fully.cleaned$Team <- as.factor(toupper(fully.cleaned$Team))
fully.cleaned$Opponent <- as.factor(toupper(fully.cleaned$Opponent))
fully.cleaned$Home.Away <- as.factor(fully.cleaned$Home.Away)
fully.cleaned$FanDuel.pts <- as.double(fully.cleaned$FanDuel.pts)
fully.cleaned$FanDuel.sal <- as.double(fully.cleaned$FanDuel.sal)

## save cleaned fanduel output
write.csv(fully.cleaned, output.path)