library(ggplot2)
library(tidyverse)
library(ggrepel)
library(dplyr)
library(tidyr)
library(repurrrsive)

primary_bold = "#1f78b4"
primary_bold_ke = "#1b9e77"
primary_light = "#C1DAEA"
primary_light_ke = "#ACDBCD"
secondary = "#6a3d9a"
secondary_ke = "#d95f02"
secondary_light  = "#BBA6D1"
secondary_light_ke = "#f1c4a3"
tertiary = "#F991CC"
tertiary_ke = "#7570b3"
tertiary_light = "#FCD7EC"
tertiary_light_ke = "#CCCBE3"
muted = "grey60"
muted_light = "grey75"

format_lf_name = function(d) {
  x = gsub("_", " ", d)
  print(x)
  if (x == "utilitarian anthro") return("utilitarian (human)")
  if (x %in% c("youth", "doctors", "females", "elderly")) return(paste("save", x))
  if (x %in% c("pets", "homeless", "criminals")) return(paste("sacrifice", x))
  if (x=="action") return("always intervene")
  if (x=="status") return("favor executives")
  if (x=="legal") return("favor legal crossing")
  if (x=="illegal") return("disfavor illegal crossing")
  if (x=="pred") return("Generative Model")
  if (x=="pred weighted majority") return("Weighted Majority Voter")
  if (x=="health") return("Choose no health issues")
  if (x=="age") return("Choose younger")
  if (x=="alcohol") return("Choose drinks less")
  return(x)
}


####################################################################
## Frequency plots ##
freq_scenario = read.csv("figures/data/freq_scenario.csv")
freq_character = read.csv("figures/data/freq_character.csv")
freq_country = read.csv("figures/data/freq_countries.csv")

ggplot(freq_character, aes(x=reorder(X, frequency), y=frequency)) + 
  geom_bar(stat="identity") + 
  geom_col(fill=primary_light, color=primary_bold) + 
  xlab("Character") +
  ylab("Frequency") +
  coord_flip() +
  theme(
    axis.text.y = element_text(face="bold"),
    axis.title.x = element_text(face="bold"),
    axis.title.y = element_blank()
  ) +
  ggtitle("Moral Machine Character Frequency")
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
  geom_col(fill=secondary_light, color=secondary) + 
  xlab("Character") +
  ylab("Frequency") +
  coord_flip() +
  theme(
    axis.text.y = element_text(face="bold", size=12),
    axis.title.x = element_text(face="bold", size=12),
    axis.title.y = element_blank()
  ) +
  ggtitle("Moral Machine Respondents by Country")
ggsave('figures/freq_countries.png', width=4, height=6)

mm_perturb = read.csv("figures/data/mm-perturb.csv")
mm_perturb$formatted = mapply(format_lf_name, mm_perturb$heuristic)
mm_perturb$color = rep(primary_bold, nrow(mm_perturb))
mm_perturb$fill = rep(primary_light, nrow(mm_perturb))
mm_perturb$color[mm_perturb$value_added <= 0] = secondary
mm_perturb$fill[mm_perturb$value_added <= 0] = secondary_light
ggplot(mm_perturb, aes(x=reorder(formatted, value_added), y=value_added)) + 
  geom_bar(stat="identity") + 
  geom_col(fill=mm_perturb$fill, color=mm_perturb$color) + 
  ylab("Accuracy Gain") +
  coord_flip() +
  theme(
    axis.text.y = element_text(face="bold", size=12),
    axis.title.x = element_text(face="bold", size=12),
    axis.title.y = element_blank()
  ) +
  ggtitle("Accuracy Gain per Heuristic")
ggsave("figures/mm-perturb.png", width=5, height=5)


####################################################################
## Faceted Bar ##
preds_scenario = read.csv("figures/data/mm-preds_scenario.csv")
# need to calculate accuracy per scenario
to_calc = setdiff(colnames(preds_scenario), c("scenario", "actual", "X"))
acc_t = preds_scenario %>%
  group_by(scenario) %>%
  summarise_at(vars(!!to_calc), funs(
    sum(. == actual) / (n() - sum(. == -1))
  ))
## TODO add error bars with a proportion confidence interval https://stackoverflow.com/questions/17810684/in-ggplot2-how-can-i-make-a-bar-chart-of-proportions-across-factors-and-add-er
acc <- data.frame(t(acc_t[-1]))
colnames(acc) <- acc_t$scenario
acc$lf <- row.names(acc)
accs = acc %>% gather(scenario, acc, Age:Utilitarian) %>% drop_na()
accs$lf = factor(accs$lf, levels=c(c("preds"), setdiff(colnames(preds_scenario), c("preds"))))
accs$lf_formatted = mapply(format_lf_name, accs$lf)
accs$lf_formatted = factor(accs$lf_formatted, levels=c(setdiff(unique(accs$lf_formatted), c("Generative Model")), c("Generative Model")))
accs$fill = rep(primary_light, nrow(accs))
accs$fill[accs$lf_formatted == "Generative Model"] = secondary_light
accs$color = rep(primary_bold, nrow(accs))
accs$color[accs$lf_formatted == "Generative Model"] = secondary
ggplot(accs, aes(x=lf_formatted, y=acc)) +
  geom_bar(stat="identity",position="dodge") +
  facet_wrap(~ scenario, ncol=2) +
  geom_col(fill=accs$fill, color=accs$color) +
  coord_flip() +
  labs(x="Accuracy", "Heuristic") +
  theme(
    axis.text.y = element_text(size=8, face=c(rep("plain", 17), "bold")),
    axis.title.x = element_text(size=8)
  ) +
  ggtitle("Heuristic Accuracy")
ggsave('figures/mm-preds_scenario.png', width=7, height=9)


preds_scenario_ke = read.csv("figures/data/ke-preds_scenario.csv")
# need to calculate accuracy per scenario
to_calc = setdiff(colnames(preds_scenario_ke), c("scenario", "actual", "X"))
acc_t = preds_scenario_ke %>%
  group_by(scenario) %>%
  summarise_at(vars(!!to_calc), funs(
    sum(. == actual) / (n() - sum(. == -1))
  ))
## TODO add error bars with a proportion confidence interval https://stackoverflow.com/questions/17810684/in-ggplot2-how-can-i-make-a-bar-chart-of-proportions-across-factors-and-add-er
acc <- data.frame(t(acc_t[-1]))
colnames(acc) <- acc_t$scenario
acc$lf <- row.names(acc)
accs = acc %>% gather(scenario, acc, Age:Random) %>% drop_na()
accs$lf = factor(accs$lf, levels=c(c("preds", "preds_weighted_majority"), setdiff(colnames(preds_scenario_ke), c("preds", "preds_weighted_majority"))))
accs$lf_formatted = mapply(format_lf_name, accs$lf)
accs$lf_formatted = factor(accs$lf_formatted, levels=c(setdiff(unique(accs$lf_formatted), c("Generative Model", "Weighted Majority Voter")), c("Weighted Majority Voter", "Generative Model")))
accs$fill = rep(primary_light_ke, nrow(accs))
accs$fill[accs$lf_formatted == "Generative Model"] = secondary_light_ke
accs$fill[accs$lf_formatted == "Weighted Majority Voter"] = tertiary_light_ke
accs$color = rep(primary_bold_ke, nrow(accs))
accs$color[accs$lf_formatted == "Generative Model"] = secondary_ke
accs$color[accs$lf_formatted == "Weighted Majority Voter"] = tertiary_ke
ggplot(accs, aes(x=lf_formatted, y=acc)) +
  geom_bar(stat="identity",position="dodge") +
  facet_wrap(~ scenario, ncol=2) +
  geom_col(fill=accs$fill, color=accs$color) +
  coord_flip() +
  labs(x="Accuracy", y="Heuristic") +
  theme(
    axis.text.y = element_text(size=8, face=c(rep("plain", 17), "bold")),
    axis.title.x = element_text(size=8)
  ) +
  ggtitle("Heuristic Accuracy")
ggsave('figures/ke-preds_scenario.png', width=6, height=5)


####################################################################
## Scatters ##
lfanalysis_weighted = read.csv("figures/data/mm-weights.csv")
lfanalysis_weighted$X = factor(lfanalysis_weighted$X, levels=unique(lfanalysis_weighted$X))
lfanalysis_weighted$X_formatted = mapply(format_lf_name, lfanalysis_weighted$X)
lfanalysis_weighted$Weight = lfanalysis_weighted$weight
ggplot(lfanalysis_weighted, aes(x=Coverage, y=Emp..Acc., size=Weight)) +
  geom_point(fill=primary_light, colour=primary_bold, shape=21, stroke=1) +
  scale_size_continuous(range = c(1,15)) +
  labs(y="Accuracy", x="Coverage") +
  ggtitle("Heuristic Accuracy vs. Coverage") +
  theme(legend.position=c(.90, .70)) +
  geom_label_repel(aes(label=X_formatted), size=3, box.padding=0.75, point.padding=0.5)
ggsave('figures/mm-weights.png', width=7.5, height=7.5)

## not very good - deprecated
#
# lf_analysis_weighted_ke = read.csv("figures/data/ke-weights.csv")
# lf_analysis_weighted_ke$X = factor(lf_analysis_weighted_ke$X, levels=unique(lf_analysis_weighted_ke$X))
# lf_analysis_weighted_ke$X_formatted = mapply(format_lf_name, lf_analysis_weighted_ke$X)
# lf_analysis_weighted_ke$Weight = lf_analysis_weighted_ke$weight
# ggplot(lf_analysis_weighted_ke, aes(x=Coverage, y=Emp..Acc., size=Weight)) +
#   geom_point(fill=primary_light, colour=primary_bold, shape=21, stroke=1) +
#   scale_size_continuous(range = c(1,15)) +
#   labs(y="Accuracy", x="Coverage") +
#   ggtitle("Heuristic Accuracy vs. Coverage") +
#   theme(legend.position=c(.90, .70)) +
#   geom_label_repel(aes(label=X_formatted), size=3, box.padding=0.75, point.padding=0.5)
# ggsave('figures/ke-weights.png', width=5, height=5)

####################################################################
## Lines ##
accs = read.csv("figures/data/mm-accs_voters.csv")
ggplot(data = accs, mapping=aes(x=n_voters)) +
  geom_point(aes(y=acc_gold), color=primary_light) +
  geom_point(aes(y=acc_heuristic), color=secondary_light) +
  geom_ribbon(aes(ymin=acc_gold-1.96*std_gold, ymax=acc_gold+1.96*std_gold), fill=muted, alpha=alpha) +
  geom_ribbon(aes(ymin=acc_heuristic-1.96*std_heuristic, ymax=acc_heuristic+1.96*std_heuristic), fill=muted, alpha=alpha) +
  geom_smooth(aes(y=acc_gold, color=primary_bold), formula=(y~sqrt(x)), se=T) +
  geom_smooth(aes(y=acc_heuristic,  color=secondary), formula=(y~sqrt(x)), se=T) +
  scale_color_identity(guide="legend", name="Model trained on", labels=c("Respondent Labels", "Heuristic Labels")) +
  scale_y_continuous(breaks=round(seq(0.4, 0.8, by=0.05), 2), limits=c(0.4, 0.8)) +
  theme(legend.position=c(.75, .25), plot.title=element_text(size=12)) +
  labs(y="Accuracy", x="Number of Respondents") +
  ggtitle("Discriminative Accuracy vs. Number of Respondents (Moral Machine)")
ggsave("figures/mm-accs_voter.png", width=6, height=6)

accs_ke = read.csv("figures/data/ke-accs_voters.csv")
ggplot(data = accs_ke, mapping=aes(x=n_voters)) +
  geom_point(aes(y=acc_gold), color=primary_light_ke) +
  geom_point(aes(y=acc_heuristic), color=secondary_light_ke) +
  geom_point(aes(y=acc_borda), color=tertiary_light_ke) +
  geom_ribbon(aes(ymin=acc_gold-1.96*std_gold, ymax=acc_gold+1.96*std_gold), fill=muted, alpha=alpha) +
  geom_ribbon(aes(ymin=acc_heuristic-1.96*std_heuristic, ymax=acc_heuristic+1.96*std_heuristic), fill=muted, alpha=alpha) +
  geom_ribbon(aes(ymin=acc_borda-1.96*std_borda, ymax=acc_borda+1.96*std_borda), fill=muted, alpha=alpha) +
  geom_smooth(aes(y=acc_gold, color=primary_bold_ke), formula=(y~sqrt(x)), se=T) +
  geom_smooth(aes(y=acc_heuristic,  color=secondary_ke), formula=(y~sqrt(x)), se=T) +
  geom_smooth(aes(y=acc_borda,  color=tertiary_ke), formula=(y~sqrt(x)), se=T) +
  scale_color_identity(guide="legend", name="Model trained on", labels=c("Respondent Labels", "Heuristic Labels - Borda Weighting", "Heuristic Labels - Generative")) +
  scale_y_continuous(breaks=round(seq(0.6, 1.0, by=0.05), 2), limits=c(0.6, 1.0)) +
  theme(legend.position=c(.75, .25), plot.title=element_text(size=12)) +
  labs(y="Accuracy", x="Number of Respondents") +
  ggtitle("Discriminative Accuracy vs. Number of Respondents (Kidney Exchange)")
ggsave("figures/ke-accs_voter.png", width=6, height=6)

accs_n = read.csv("figures/data/mm-accs_data.csv")
alpha = .25
ggplot(data = accs_n, mapping=aes(x=n_rows)) +
  geom_point(aes(y=acc_gold), color=primary_light) +
  geom_point(aes(y=acc_heuristic), color=secondary_light) +
  geom_ribbon(aes(ymin=acc_gold-1.96*std_gold, ymax=acc_gold+1.96*std_gold), fill=muted, alpha=alpha) +
  geom_ribbon(aes(ymin=acc_heuristic-1.96*std_heuristic, ymax=acc_heuristic+1.96*std_heuristic), fill=muted, alpha=alpha) +
  geom_smooth(aes(y=acc_gold, color=primary_bold), formula=(y~sqrt(x)), se=F) +
  geom_smooth(aes(y=acc_heuristic,  color=secondary), formula=(y~sqrt(x)), se=F) +
  scale_color_identity(guide="legend", name="Model trained on", labels=c("Respondent Labels", "Heuristic Labels")) +
  scale_y_continuous(breaks=round(seq(0.4, 0.9, by=0.05), 2), limits=c(0.4, 0.9)) +
  theme(legend.position=c(.75, .25)) +
  labs(y="Accuracy", x="Training Set Size") +
  ggtitle("Discriminative Accuracy vs. Size of Training Set (Moral Machine)")
ggsave("figures/mm-accs_data.png", width=6, height=6)

accs_n_ke = read.csv("figures/data/ke-accs_data.csv")
ggplot(data = accs_n_ke, mapping=aes(x=n_rows)) +
  geom_point(aes(y=acc_gold), color=primary_light_ke) +
  geom_point(aes(y=acc_heuristic), color=secondary_light_ke) +
  geom_point(aes(y=acc_freedman), color=tertiary_light_ke) +
  geom_ribbon(aes(ymin=acc_gold-1.96*std_gold, ymax=acc_gold+1.96*std_gold), fill=muted, alpha=alpha) +
  geom_ribbon(aes(ymin=acc_heuristic-1.96*std_heuristic, ymax=acc_heuristic+1.96*std_heuristic), fill=muted, alpha=alpha) +
  geom_ribbon(aes(ymin=acc_freedman-1.96*std_freedman, ymax=acc_freedman+1.96*std_freedman), fill=muted, alpha=alpha) +
  geom_smooth(aes(y=acc_gold, color=primary_bold_ke), formula=(y~sqrt(x)), se=F) +
  geom_smooth(aes(y=acc_heuristic,  color=secondary_ke), formula=(y~sqrt(x)), se=F) +
  geom_smooth(aes(y=acc_freedman,  color=tertiary_ke), formula=(y~sqrt(x)), se=F) +
  scale_color_identity(guide="legend", name="Model trained on", labels=c("Respondent Labels", "Freedman et al.", "Heuristic Labels")) +
  scale_y_continuous(breaks=round(seq(0.5, 1.0, by=0.05), 2), limits=c(0.5, 1.0)) +
  theme(legend.position=c(.75, .25)) +
  labs(y="Accuracy", x="Training Set Size") +
  ggtitle("Discriminative Accuracy vs. Size of Training Set (Kidney Exchange)")
ggsave("figures/ke-accs_data.png", width=6, height=6)

F####################################################################
## Histograms ##
L = read.csv("figures/data/mm-density.csv")
find_density = function(x) {
  return(length(which(x[-1] != -1)))
}
L$density = apply(L, 1, find_density)
ggplot(L, aes(x=density)) +
  geom_histogram(binwidth=1, color=primary_bold, fill=primary_light) +
  labs(y="Density", x="Non-Abstaining Heuristic Functions") +
  ggtitle("Labeling Density (Moral Machine)")
ggsave('figures/mm-density.png', width=4, height=4)

ke = read.csv("figures/data/ke-density.csv")
ke$density = apply(ke, 1, find_density)
ggplot(ke, aes(x=density)) +
  geom_histogram(binwidth=1, color=primary_bold_ke, fill=primary_light_ke) +
  labs(y="Density", x="Non-Abstaining Heuristic Functions") +
  ggtitle("Labeling Density (Kidney Exchange)")
ggsave('figures/ke-density.png', width=4, height=4)


