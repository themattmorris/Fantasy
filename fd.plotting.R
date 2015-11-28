data.packages <- c('dplyr', 'ggplot2', 'RColorBrewer', 'ggthemes', 'ggExtra', "gridExtra")
lapply(data.packages, library, character.only = T)

## look at summaries and added points per dollar metric col
fd <- fd.data %>% 
  mutate(PPD = FanDuel.pts / FanDuel.sal) %>% 
  select(Week, Position, Home.Away, FanDuel.pts, FanDuel.sal, PPD)

## position & tier groupings for plots
fd.qb <- fd %>% 
  filter(Position == "QB")

fd.skill <- fd %>% 
  filter(Position %in% c("RB", "WR", "TE"))

fd.rb <- fd %>% 
  filter(Position == "RB")

fd.wr <- fd %>% 
  filter(Position == "WR")

fd.te <- fd %>% 
  filter(Position == "TE")

fd.rest <- fd %>% 
  filter(Position %in% c("PK", "Def"))

fd.pk <- fd %>% 
  filter(Position  == "PK")

fd.def <- fd %>% 
  filter(Position == "Def")

## colorblind palette
cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

## marginal histograms by position
qb.sp <- ggplot(fd.qb,
                aes(x = FanDuel.sal,
                    y = FanDuel.pts,
                    shape = Home.Away)) +
  geom_point(col = "#E69F00",
             size = 3) +
  geom_smooth(aes(col = Home.Away), 
              method = loess, 
              se = FALSE, 
              fullrange = TRUE) + 
  scale_colour_manual(values = c("#8E07F5", "#07F537")) + 
  labs(x = "Salary",
       y = "Points") +
  theme_tufte(16)

qb.hist <- ggMarginal(qb.sp + theme_tufte(), 
                      type = "histogram", 
                      fill = "#E69F00", 
                      col = "white")

rb.sp <- ggplot(fd.rb,
                aes(FanDuel.sal,
                    FanDuel.pts,
                    shape = Home.Away)) +
  geom_point(col = "#56B4E9",
             size = 3) +
  geom_smooth(aes(col = Home.Away), 
              method = loess, 
              se = FALSE, 
              fullrange = TRUE) + 
  scale_colour_manual(values = c("#8E07F5", "#07F537")) + 
  labs(x = "Salary",
       y = "Points") +
  theme_tufte(16)

rb.hist <- ggMarginal(rb.sp + theme_tufte(), 
                      type = "histogram", 
                      fill = "#56B4E9", 
                      col = "white")

wr.sp <- ggplot(fd.wr,
                aes(FanDuel.sal,
                    FanDuel.pts,
                    shape = Home.Away)) +
  geom_point(col = "#009E73",
             size = 3) +
  geom_smooth(aes(col = Home.Away), 
              method = loess, 
              se = FALSE, 
              fullrange = TRUE) + 
  scale_colour_manual(values = c("#8E07F5", "#07F537")) + 
  labs(x = "Salary",
       y = "Points") +
  theme_tufte(16)

geom_point()
wr.hist <- ggMarginal(wr.sp + theme_tufte(), 
                      type = "histogram", 
                      fill = "#009E73", 
                      col = "white")

te.sp <- ggplot(fd.te,
                aes(FanDuel.sal,
                    FanDuel.pts,
                    shape = Home.Away)) +
  geom_point(col = "#CC79A7",
             size = 3) +
  geom_smooth(aes(col = Home.Away), 
              method = loess, 
              se = FALSE, 
              fullrange = TRUE) + 
  scale_colour_manual(values = c("#8E07F5", "#07F537")) + 
  labs(x = "Salary",
       y = "Points") +
  theme_tufte(16)

te.hist <- ggMarginal(te.sp + theme_tufte(), 
                      type = "histogram", 
                      fill = "#CC79A7", 
                      col = "white")

pk.sp <- ggplot(fd.pk,
                aes(FanDuel.sal,
                    FanDuel.pts,
                    shape = Home.Away)) +
  geom_point(col = "#0072B2",
             size = 3) +
  geom_smooth(aes(col = Home.Away), 
              method = loess, 
              se = FALSE, 
              fullrange = TRUE) + 
  scale_colour_manual(values = c("#8E07F5", "#07F537")) + 
  labs(x = "Salary",
       y = "Points") +
  theme_tufte(16)

pk.hist <- ggMarginal(pk.sp + theme_tufte(), 
                      type = "histogram", 
                      fill = "#0072B2", 
                      col = "white")

def.sp <- ggplot(fd.def,
                 aes(FanDuel.sal,
                     FanDuel.pts,
                     shape = Home.Away)) +
  geom_point(col = "#D55E00",
             size = 3) +
  geom_smooth(aes(col = Home.Away), 
              method = loess, 
              se = FALSE, 
              fullrange = TRUE) + 
  scale_colour_manual(values = c("#8E07F5", "#07F537")) + 
  labs(x = "Salary",
       y = "Points") +
  theme_tufte(16)

def.hist <- ggMarginal(def.sp + theme_tufte(), 
                       type = "histogram", 
                       fill = "#D55E00", 
                       col = "white")

## positional comparison
positions <- grid.arrange(qb.hist, 
                          rb.hist, 
                          wr.hist, 
                          te.hist, 
                          pk.hist, 
                          def.hist, 
                          nrow = 2, 
                          top = "marginal histograms")

## save
png("/Users/brett/GitHub/proj-fantasy/marginal_histograms.png", 
    height = 720, 
    width = 1280)
plot(positions)
dev.off()

## density curves: 
qb <- ggplot(fd.qb, 
             aes(FanDuel.pts)) + 
  geom_density(aes(group = Position, 
                   col = Position, 
                   fill = Position), 
               col = "#E69F00",
               fill = "#E69F00",
               alpha = 0.2) + 
  xlim(0,50) + 
  ylim(0,.1750) + 
  theme_bw(16)

skill <- ggplot(fd.skill, 
                aes(FanDuel.pts)) + 
  geom_density(aes(group = Position, 
                   col = Position, 
                   fill = Position),
               alpha = 0.2) + 
  scale_colour_manual(
    values = c("RB" = "#56B4E9",
               "WR" = "#009E73",
               "TE" = "#CC79A7")) + 
  scale_fill_manual(
    values = c("RB" = "#56B4E9",
               "WR" = "#009E73",
               "TE" = "#CC79A7")) +  
  xlim(0,50) + 
  ylim(0,.1750) + 
  theme_bw(16)

rest <- ggplot(fd.rest, 
               aes(FanDuel.pts)) + 
  geom_density(aes(group = Position, 
                   col = Position, 
                   fill = Position), 
               alpha = 0.2) + 
  scale_colour_manual(
    values = c("PK" = "#0072B2",
               "Def" = "#D55E00")) + 
  scale_fill_manual(
    values = c("PK" = "#0072B2",
               "Def" = "#D55E00")) +
  xlim(0,50) + 
  ylim(0,.1750) + 
  theme_bw(16)

## comparison of all three densities
dens <- grid.arrange(qb, 
                     skill, 
                     rest, 
                     nrow = 1)

## save
png("/Users/brett/GitHub/proj-fantasy/density_curves.png", 
    height = 720, 
    width = 1280)
plot(dens)
dev.off()

## loess smoothing by tier
qb.reg <- ggplot(fd.qb, 
                 aes(FanDuel.sal, 
                     FanDuel.pts, 
                     shape = Home.Away,
                     col = Position)) + 
  geom_point(col = "#E69F00",
             size = 3) + 
  labs(x = "Salary",
       y = "Points")  + 
  xlim(4000,10000) + 
  ylim(0,40) + 
  geom_smooth(method = loess,
              col = "black") + 
  scale_colour_manual(values = c("#8E07F5", "#07F537")) + 
  theme_tufte(16)
  
skill.reg <- ggplot(fd.skill, 
                    aes(FanDuel.sal, 
                        FanDuel.pts, 
                        shape = Home.Away,
                        col = Position)) + 
  geom_point(size = 3) + 
  scale_colour_manual(
    values = c("RB" = "#56B4E9",
               "WR" = "#009E73",
               "TE" = "#CC79A7")) + 
  labs(x = "Salary",
       y = "Points") + 
  xlim(4000,10000) + 
  ylim(0,40) + 
  geom_smooth(method = loess,
              col = "black") + 
  theme_tufte(16)

rest.reg <- ggplot(fd.rest, 
                   aes(FanDuel.sal, 
                       FanDuel.pts, 
                       shape = Home.Away,
                       col = Position)) + 
  geom_point(size = 3) + 
  scale_colour_manual(
    values = c("PK" = "#0072B2",
               "Def" = "#D55E00")) + 
  labs(x = "Salary",
       y = "Points") + 
  xlim(4000,6000) + 
  ylim(0,40) + 
  geom_smooth(method = loess,
              col = "black") + 
  theme_tufte(16)

## comparision of tiered smoothing
tier.reg <- grid.arrange(qb.reg, skill.reg, rest.reg, nrow = 1, top = "loess smoothing")

## save
png("/Users/brett/GitHub/proj-fantasy/tiered_smoothing.png", height = 720, width = 1280)
plot(tier.reg)
dev.off()

## positional violin 
fd.vio <- ggplot(fd,
                 aes(Position,
                     FanDuel.pts,
                     fill = Position)) + 
  geom_violin(trim = FALSE) + 
  geom_boxplot(width = .15, 
               fill = "white", 
               outlier.colour = NA) +
  stat_summary(fun.y = mean, 
               geom = "point", 
               fill = "#999999", 
               shape = 23, 
               size = 3) + 
  scale_fill_manual(
    values = c("QB" = "#E69F00",
               "RB" = "#56B4E9",
               "WR" = "#009E73",
               "TE" = "#CC79A7",
               "PK" = "#0072B2",
               "Def" = "#D55E00")) + 
  guides(fill = FALSE) + 
  labs(x = "Position",
       y = "Points") + 
  ylim(-10, 50) + 
  theme_tufte(16)

ggsave("/Users/brett/GitHub/proj-fantasy/position_violins.png", fd.vio)