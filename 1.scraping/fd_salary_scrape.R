#### install & load packages and fix functions ####
## install package function
ipak <- function(pkg){
  new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
  if (length(new.pkg)) 
    install.packages(new.pkg, dependencies = TRUE)
  sapply(pkg, require, character.only = TRUE)
}

## packages to install and load
packages <- c('rvest', 'knitr', 'pipeR', 'MASS')
ipak(packages)
lapply(packages, library, character.only = T)

#### IMPORTANT: specify final output path here ####
output.path = "/Users/brett/GitHub/proj-fantasy/data/salary.csv"

#### create list of season 2015 results through week 14 ####
fd.sites <- c("http://rotoguru1.com/cgi-bin/fyday.pl?week=14&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=13&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=12&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=11&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=10&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=9&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=8&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=7&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=6&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=5&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=4&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=3&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=2&game=fd&scsv=1",
            "http://rotoguru1.com/cgi-bin/fyday.pl?week=1&game=fd&scsv=1")

d <- matrix(nrow = 14, ncol = 1)

#### for loop to scrape results and output a csv ####
for (i in 1:14) {
  ## loop through pages above
  roto <- fd.sites[i]
  urls <- read_html(roto)
  ## scrape semi-colon separated files to a character string
  d[i,] <- try({
    urls %>% 
      html_node("td pre") %>%
      html_text()
  })
  ## save raw data for archival
  write(d, output.path, sep = ";")
}