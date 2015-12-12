#### install & load packages and fix functions ####
## install package function
ipak <- function(pkg){
  new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
  if (length(new.pkg)) 
    install.packages(new.pkg, dependencies = TRUE)
  sapply(pkg, require, character.only = TRUE)
}
## packages to install and load
data.packages <- c('dplyr', 'ggplot2', 'RColorBrewer', 'RCurl', 'ggthemes', 'ggExtra', 'gridExtra', 'scales', 'tidyr', 'MASS', 'devtools', 'lubridate', 'mosaic')
ipak(data.packages)
lapply(data.packages, library, character.only = T)

## redefine select from dplyr because MASS package causes issues
select <- dplyr::select

#### IMPORTANT: specify final output path here ####
output.path = "/Users/brett/GitHub/proj-fantasy/data/fanduel_season_data.csv"
lookup.table.path = "/Users/brett/GitHub/proj-fantasy/data/lookup_table.csv"

#### bring in salary data from fanduel ####
## get data from github and import as a table
salary <- tbl_df(read.csv("https://raw.githubusercontent.com/brttstl/proj-fantasy/master/data/salary.csv", header = TRUE, ";", skipNul = FALSE, stringsAsFactors = FALSE))

#### clean up ####
## remove gid column and filter out def for name format reshape remove salaries that are 0 as these players weren't available
no.def <- salary %>%
  select(Week, Year, GID, Name, Pos, Team, "h/a" = h.a, Oppt, "FD points" = FD.points, Salary = FD.salary) %>% 
  filter(Pos %in% c("QB", "RB", "WR", "TE", "PK"), Salary >= 1)

def <- salary %>%
  select(Week, Year, GID, Name, Pos, Team, "h/a" = h.a, Oppt, "FD points" = FD.points, Salary = FD.salary) %>% 
  filter(Pos == "Def", Salary >= 1)

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
allowedVars <- c("Name", "Pos")
fully.cleaned <- addNewData(lookup.table.path, clean, allowedVars)

## format columns to match profootball reference export
fully.cleaned$Year <- as.integer(fully.cleaned$Year)
fully.cleaned$Week <- as.integer(fully.cleaned$Week)
fully.cleaned$Pos <- factor(fully.cleaned$Pos, levels = c("QB", "RB", "WR", "TE", "K", "DEF"))
fully.cleaned$`FD points` <- as.double(fully.cleaned$`FD points`)
fully.cleaned$Salary <- as.double(fully.cleaned$Salary)

## create conditional location column
final <- fully.cleaned %>%
  mutate(Location = ifelse(`h/a` == "h", Team, Oppt))

## rearrange rows
final <- final[,c("Week", "Year", "GID", "Name", "Pos", "Team", "Location", "h/a", "Oppt", "FD points", "Salary")]

## finish proper formatting
final$Team <- as.factor(toupper(final$Team))
final$Oppt <- as.factor(toupper(final$Oppt))
final$`h/a` <- as.factor(final$`h/a`)
final$Location <- as.factor(toupper(final$Location))

#### save cleaned fanduel output ####
write.csv(final, output.path, row.names = FALSE)