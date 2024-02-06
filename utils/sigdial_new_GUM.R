library(stringr)


GUM_facts <- read.table("data/GUM9/GUM_facts.tab", stringsAsFactors = T, header=T,sep = "\t")
attach(GUM_facts)

# explicit vs. implicit vs. distracting 
# GUM v9
GUM_exp = sum(dm=="y")
GUM_imp = sum(dm=="n")
GUM_exp_prop = GUM_exp / (GUM_exp + GUM_imp)
GUM_imp_prop = GUM_imp / (GUM_exp + GUM_imp)
GUM_distractors = sum(distractor=="y")
GUM_distractors_prop = GUM_distractors / length(distractor)

GUM_exp
GUM_exp_prop
GUM_imp
GUM_imp_prop
GUM_distractors
GUM_distractors_prop

# > nrow(facts[facts$attach_label_error_count_bot>2 & facts$distractor=="y",])
# [1] 116


# density plots 
library(ggplot2)
library(gridExtra)

# GUM 
GUM_facts$connective = GUM_facts$dm
p1<-ggplot(GUM_facts, aes(GUM_facts$attach_error_bot, fill = connective)) + geom_density(alpha = 0.2) + xlab("bottom-up attachment error counts") + labs(fill="conn")
p2<-ggplot(GUM_facts, aes(GUM_facts$attach_error_top, fill = connective)) + geom_density(alpha = 0.2) + xlab("top-down attachment error counts") + labs(fill="conn")
p3<-ggplot(GUM_facts, aes(GUM_facts$attach_error_bot, fill = distractor)) + geom_density(alpha = 0.2) + xlab("bottom-up attachment error counts") + labs(fill="dstr")
p4<-ggplot(GUM_facts, aes(GUM_facts$attach_error_top, fill = distractor)) + geom_density(alpha = 0.2) + xlab("top-down attachment error counts") + labs(fill="dstr")

grid.arrange(p1, p2, p3,p4,nrow = 2)


# regression models
library(betareg)
library(glmmTMB)

# attachment error only
GUM_facts$attach_error_bot_percent = ifelse(GUM_facts$attach_error_bot/5==1,0.99, 
                                            ifelse(GUM_facts$attach_error_bot/5==0,0.01, GUM_facts$attach_error_bot/5))
GUM_facts$attach_error_top_percent = ifelse(GUM_facts$attach_error_top/5==1,0.99, 
                                            ifelse(GUM_facts$attach_error_top/5==0,0.01, GUM_facts$attach_error_top/5))
# bottom-up
# EDU_OOV
summary(m<-betareg(data=GUM_facts, attach_error_bot_percent~dm+edu_oov_rate))
# intersent
summary(m<-betareg(data=GUM_facts, attach_error_bot_percent~dm+gold_subord))
# interpara
summary(m<-betareg(data=GUM_facts, attach_error_bot_percent~dm+gold_interpara))
# intersent+interpara
summary(m<-betareg(data=GUM_facts, attach_error_bot_percent~dm+gold_subord+gold_interpara))
# more
summary(m<-betareg(data=GUM_facts,attach_error_bot_percent~dm+edu_len+distractor+edu_oov_rate))
summary(m<-betareg(data=GUM_facts,attach_error_bot_percent~dm+edu_len+distractor+edu_oov_rate+gold_interpara+gold_subord))
summary(m<-betareg(data=GUM_facts,attach_error_bot_percent~dm+edu_len+distractor+edu_oov_rate+gold_interpara+gold_subord+genre))
summary(m<-betareg(data=GUM_facts,attach_error_bot_percent~dm+edu_len+distractor+edu_oov_rate+gold_interpara+gold_subord+genre+gold_rel_class))


# top-down
summary(m<-betareg(data=GUM_facts, attach_error_top_percent~dm+edu_oov_rate))
summary(m<-betareg(data=GUM_facts, attach_error_top_percent~dm+gold_subord))
summary(m<-betareg(data=GUM_facts, attach_error_top_percent~dm+gold_interpara))
summary(m<-betareg(data=GUM_facts, attach_error_top_percent~dm+gold_subord+gold_interpara))



# attachment_or_label error
GUM_facts$attach_label_error_bot_percent = ifelse(GUM_facts$attach_label_error_count_bot/5==1,0.99, 
                                                ifelse(GUM_facts$attach_label_error_count_bot/5==0,0.01,GUM_facts$attach_label_error_count_bot/5))
GUM_facts$attach_label_error_top_percent = ifelse(GUM_facts$attach_label_error_count_top/5==1,0.99, 
                                                ifelse(GUM_facts$attach_label_error_count_top/5==0,0.01,GUM_facts$attach_label_error_count_top/5))

# bottom up - GUM
summary(glmmTMB(data=GUM_facts, attach_label_error_bot_percent~dm+distractor+(1|doc_name), family=list(family="beta",link="logit")))
summary(glmmTMB(data=GUM_facts, attach_label_error_bot_percent~dm+distractor+gold_subord+(1|doc_name), family=list(family="beta",link="logit")))
summary(glmmTMB(data=GUM_facts, attach_label_error_bot_percent~dm+distractor+gold_subord+edu_oov_rate+edu_len+genre+(1|doc_name), family=list(family="beta",link="logit")))



# intersent / subord 
summary(glmmTMB(data=GUM_facts, attach_label_error_top_percent~dm+gold_subord+(1|doc_name), family=list(family="beta",link="logit")))
summary(glmmTMB(data=GUM_facts, attach_label_error_bot_percent~dm+edu_oov_rate+(1|doc_name), family=list(family="beta",link="logit")))
summary(glmmTMB(data=GUM_facts, attach_label_error_top_percent~dm+edu_oov_rate+(1|doc_name), family=list(family="beta",link="logit")))

