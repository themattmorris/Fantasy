packages <- c('rvest', 'knitr', 'pipeR', 'MASS')
lapply(packages, library, character.only = T)

fd.sites <- c("http://rotoguru1.com/cgi-bin/fyday.pl?week=12&game=fd&scsv=1",
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

d <- matrix(nrow = 12, ncol = 1)

for (i in 1:12) {
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
  write(d, file = "/Users/bsteele/GitHub/proj-fantasy/salary.csv", sep = ";")
}