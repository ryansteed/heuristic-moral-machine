library(ggplot2)
library(tidyverse)
library(ggrepel)

primary_bold = "#1f78b4"
primary_light = "#C1DAEA"
secondary = "#6a3d9a"

## Frequency plots ##
freq_scenario = read.csv("figures/data/freq_scenario.csv")
freq_character = read.csv("figures/data/freq_character.csv")
freq_country = read.csv("figures/data/freq_countries.csv")

ggplot(freq_character, aes(x=reorder(X, frequency), y=frequency)) + 
  geom_bar(stat="identity") + 
  geom_col(fill=primary_bold) + 
  xlab("Character") +
  ylab("Frequency") +
  coord_flip() +
  theme_minimal() +
  theme(
    axis.text.y = element_text(face="bold"),
    axis.title.x = element_text(face="bold"),
    axis.title.y = element_blank()
  )
ggsave('figures/freq_character.png', width=4, height=6)

n=30
df = head(arrange(freq_country, desc(UserCountry3)), n=n)
df$X = factor(df$X, levels=df$X[order(df$UserCountry3)])
other = tail(arrange(freq_country, desc(UserCountry3)), n=nrow(freq_country)-n)
de = data.frame("Other", sum(other$UserCountry3))
names(de) = c("X", "UserCountry3")
df = rbind(de, df)

ggplot(df, aes(x=X, y=UserCountry3)) + 
  geom_bar(stat="identity") + 
  geom_col(fill=secondary) + 
  xlab("Character") +
  ylab("Frequency") +
  coord_flip() +
  theme_minimal() +
  theme(
    axis.text.y = element_text(face="bold", size=12),
    axis.title.x = element_text(face="bold", size=12),
    axis.title.y = element_blank()
  )
ggsave('figures/freq_countries.png', width=4, height=6)


## Scatters ##
lfanalysis_weighted = read.csv("figures/data/mm-weights.csv")
format_lf_name = function(x) {
  x = gsub("_", " ", x)
  if (x == "utilitarian anthro") return("utilitarian (human)")
  if (x %in% c("youth", "doctors", "females")) return(paste("save", x))
  if (x %in% c("pets", "homeless", "criminals")) return(paste("sacrifice", x))
  if (x=="inaction") return("intervene")
  if (x=="status") return("favor executives")
  if (x=="legal") return("favor legal crossing")
  if (x=="illegal") return("disfavor illegal crossing")
  return(x)
}
lfanalysis_weighted$X = lapply(lfanalysis$X, format_lf_name)
lfanalysis_weighted$Weight = lfanalysis_weighted$weight
ggplot(lfanalysis_weighted, aes(x=Coverage, y=Emp..Acc., size=Weight)) +
  geom_point(fill=primary_light, colour=primary_bold, shape=21, stroke=1) +
  scale_size_continuous(range = c(1,15)) +
  labs(y="Accuracy", x="Coverage") +
  ggtitle("Heuristic Accuracy vs. Coverage") +
  theme(legend.position=c(.90, .70)) +
  geom_label_repel(aes(label=X), size=3, box.padding=0.75, point.padding=0.5)
ggsave('figures/mm-weights.png', width=7.5, height=7.5)

## Histograms ##
L = read.csv("figures/data/mm-density.csv")
find_density = function(x) {
  return(length(which(x[-1] != -1)))
}
L$density = apply(L, 1, find_density)
ggplot(L, aes(x=density)) +
  geom_density(color="#1f78b4", fill="#C1DAEA", adjust=1.5) +
  labs(y="Smoothed Density", x="Non-Abstaining Heuristic Functions") +
  theme_minimal()
ggsave('figures/mm-density.png', width=3, height=3)