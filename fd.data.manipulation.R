
#### housekeeping ####
data.packages <- c('dplyr', 'ggplot2', 'RColorBrewer', 'RCurl', 'ggthemes', 'ggExtra', 'gridExtra', 'scales', 'tidyr', 'MASS', 'devtools', 'lubridate', 'mosaic')
lapply(data.packages, library, character.only = T)

## redefine select from dplyr because MASS package causes issues
select <- dplyr::select

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
clean.lu <- addNewData("/Users/brett/GitHub/proj-fantasy/data/lookup_table.csv", clean, allowedVars)

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
write.csv(clean.lu, "/Users/brett/GitHub/proj-fantasy/data/fanduel_2015_season_summary.csv")

## import profootref data
pro.foot.ref <- tbl_df(read.csv("https://raw.githubusercontent.com/brttstl/proj-fantasy/master/data/fantasy_data_20151202.csv", header = TRUE, skipNul = FALSE, stringsAsFactors = FALSE))

## have to add home.away and reuse lookup table
Home.Away <- c(" ")
pfr.data <- cbind(pro.foot.ref, Home.Away)

pfr.data <- pfr.data %>%
  mutate(Home.Away = "") %>%
  filter(position %in% c("QB", "RB", "FB", "WR", "TE", "KR", "K", "P", "CB", "DEF") & season == "2015") %>%
  select(Name = player, Date = date, Location = location, cmp:pts_allowed, Season = season, Week = week, Position = position, Home.Away)

## lookup tables for fb's and kr's
source_gist("https://gist.github.com/dfalster/5589956")
allowedVars <- c("Name", "Position", "Home.Away")
pfr.lu <- addNewData("/Users/brett/GitHub/proj-fantasy/data/lookup_table.csv", pfr.data, allowedVars)

## drop Home.Away column
pfr.clean <- pfr.lu %>%
  select(-Home.Away, -Position)

## join data from profootball reference into fanduel data set of players
fan.full <- full_join(clean.lu, pfr.clean, by = c("Name", "Week", "Season"))

## convert columns of full
fan.full$Week <- factor(fan.full$Week, levels = c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"))
fan.full$Location <- as.factor(fan.full$Location)
fan.full$off_snap_count_pct <- as.numeric(substr(fan.full$off_snap_count_pct,0,nchar(fan.full$off_snap_count_pct)-1))
fan.full$def_snap_count_pct <- as.numeric(substr(fan.full$def_snap_count_pct,0,nchar(fan.full$def_snap_count_pct)-1))
fan.full$st_snap_count_pct <- as.numeric(substr(fan.full$st_snap_count_pct,0,nchar(fan.full$st_snap_count_pct)-1))
fan.full$Date <- as.Date(fan.full$Date, "%m/%d/%Y")

## quick clean
full.data <- fan.full %>%
  select(week = Week, name = Name, position = Position, team = Team, home.away = Home.Away, opponent = Opponent, fanduel.pts = FanDuel.pts, fanduel.sal = FanDuel.sal, date = Date, location = Location, cmp:pts_allowed)

#### create metrics/tiers ####
## add column with average fanduel pts for week for position
fd.desc <- full.data %>%
  group_by(position, week) %>%
  mutate(pos.avg = mean(fanduel.pts, na.rm = TRUE),
         pos.sal.avg = mean(fanduel.sal, na.rm = TRUE), 
         pts.dif = fanduel.pts - pos.avg,
         sal.dif = fanduel.sal - pos.sal.avg,
         pts.per.sal = fanduel.pts / fanduel.sal,
         pts.per.sal.avg = mean(fanduel.pts / fanduel.sal)) %>%
  group_by(name) %>%
  mutate(plyr.avg = mean(fanduel.pts, na.rm = TRUE),
         plyr.sal.avg = mean(fanduel.sal, na.rm = TRUE),
         plyr.pts.sd = sd(pts.dif, na.rm = TRUE),
         plyr.sal.sd = sd(sal.dif, na.rm = TRUE),
         pts.per.sal.avg = mean(pts.per.sal, na.rm = TRUE),
         pts.per.sal.sd = sd(pts.per.sal, na.rm = TRUE))

## removes duplicates and NAs and only includes players that scored fanduel.pts
plyr.set <- fd.desc %>% 
  select(name:team, pos.avg:pos.sal.avg, pts.per.sal.avg:pts.per.sal.sd) %>%
  distinct(name) %>%
  ungroup() %>%
  filter(!is.na(plyr.pts.sd), !is.na(plyr.sal.sd)) %>%
  arrange(desc(pts.per.sal.avg), desc(pts.per.sal.sd))

# this just helps me see
ggplot(plyr.set,
       aes(x = pts.per.sal.avg)) + 
  geom_histogram() + 
  labs(x = "points per dollar") +
  theme_tufte(16)
  
# create tiered threshold values based on quantile
tiers <- tbl_df(data.frame(quantile(plyr.set$pts.per.sal.avg, probs = c(.7, .8, .9))))
rownames(tiers) <- c("Bronze", "Silver", "Gold")
colnames(tiers) <- c("threshold")
limits <- t(tiers)

plyrs <- plyr.set %>%
  mutate(tier = derivedFactor(
    "primary" = (position %in% c("QB", "RB", "WR", "TE", "PK", "DEF") & pts.per.sal.avg >= limits[1,3]),
    "secondary" = (position %in% c("QB", "RB", "WR", "TE", "PK", "DEF") & pts.per.sal.avg >= limits[1,2] & pts.per.sal.avg < limits[1,3]),
    "tertiary" = (position %in% c("QB", "RB", "WR", "TE", "PK", "DEF") & pts.per.sal.avg >= limits[1,1] & pts.per.sal.avg < limits[1,2]),
    .method = "first",
    .default = NA
  ))

# filter out na's
opti.plyrs <- plyrs %>%
  filter(!is.na(tier))

# left with final optimal player list
opti.plyrs %>%
  group_by(position) %>%
  summarise(count = n())

#### output full data here ####
write.csv(opti.plyrs, "/Users/brett/GitHub/proj-fantasy/data/optimal_player_list.csv")