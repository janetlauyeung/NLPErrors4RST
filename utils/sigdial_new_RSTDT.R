library(stringr)

RSTDT_facts = read.table("/Users/janetliu/Desktop/PYR/NLPErrors4RST/data/RSTDT/RSTDT_facts.tab", stringsAsFactors = T, header=T,sep = "\t")
attach(RSTDT_facts)

# explicit vs. implicit vs. distracting 
# RSTDT
RSTDT_exp = sum(RSTDT_facts$dm=="y")
RSTDT_imp = sum(RSTDT_facts$dm=="n")
RSTDT_exp_pro = RSTDT_exp / (RSTDT_exp + RSTDT_imp)
RSTDT_imp_prop = RSTDT_imp / (RSTDT_exp + RSTDT_imp)
RSTDT_distractors = sum(RSTDT_facts$distractor=="y")
RSTDT_distractors_prop = RSTDT_distractors / length(RSTDT_facts$distractor)

RSTDT_exp
RSTDT_exp_pro
RSTDT_imp_prop
RSTDT_imp
RSTDT_distractors
RSTDT_distractors_prop


# density plots 
library(ggplot2)
library(gridExtra)

# RSTDT 
RSTDT_facts$connective = RSTDT_facts$dm
p1<-ggplot(RSTDT_facts, aes(RSTDT_facts$attach_error_bot, fill = connective)) + geom_density(alpha = 0.2) + xlab("bottom-up attachment error counts") + labs(fill="conn")
p2<-ggplot(RSTDT_facts, aes(RSTDT_facts$attach_error_top, fill = connective)) + geom_density(alpha = 0.2) + xlab("top-down attachment error counts") + labs(fill="conn")
p3<-ggplot(RSTDT_facts, aes(RSTDT_facts$attach_error_bot, fill = distractor)) + geom_density(alpha = 0.2) + xlab("bottom-up attachment error counts") + labs(fill="dstr")
p4<-ggplot(RSTDT_facts, aes(RSTDT_facts$attach_error_top, fill = distractor)) + geom_density(alpha = 0.2) + xlab("top-down attachment error counts") + labs(fill="dstr")

grid.arrange(p1, p2, p3, p4, nrow = 2)


# regression models
library(betareg)
library(glmmTMB)

RSTDT_facts$attach_error_bot_percent = ifelse(attach_error_bot/5==1,0.99, ifelse(attach_error_bot/5==0,0.01, attach_error_bot/5))

# attachment_or_label error
RSTDT_facts$attach_label_error_bot_percent = ifelse(RSTDT_facts$attach_label_error_count_bot/5==1,0.99, 
                                                  ifelse(RSTDT_facts$attach_label_error_count_bot/5==0,0.01,RSTDT_facts$attach_label_error_count_bot/5))
RSTDT_facts$attach_label_error_top_percent = ifelse(RSTDT_facts$attach_label_error_count_top/5==1,0.99, ifelse(RSTDT_facts$attach_label_error_count_top/5==0,0.01,RSTDT_facts$attach_label_error_count_top/5))

# bottom up - GUM
summary(glmmTMB(data=RSTDT_facts, attach_label_error_bot_percent~dm+distractor+(1|doc_name), family=list(family="beta",link="logit")))
summary(glmmTMB(data=RSTDT_facts, attach_label_error_bot_percent~dm+gold_inersent+(1|doc_name), family=list(family="beta",link="logit")))
summary(glmmTMB(data=RSTDT_facts, attach_label_error_bot_percent~dm+edu_oov_rate+(1|doc_name), family=list(family="beta",link="logit")))

summary(glmmTMB(data=RSTDT_facts, attach_label_error_bot_percent~dm+distractor+gold_inersent+(1|doc_name), family=list(family="beta",link="logit")))
summary(glmmTMB(data=RSTDT_facts, attach_label_error_bot_percent~dm+gold_inersent+edu_oov_rate+(1|doc_name), family=list(family="beta",link="logit")))
summary(glmmTMB(data=RSTDT_facts, attach_label_error_bot_percent~dm+distractor+edu_oov_rate+(1|doc_name), family=list(family="beta",link="logit")))
summary(glmmTMB(data=RSTDT_facts, attach_label_error_bot_percent~dm+distractor+gold_inersent+edu_oov_rate+(1|doc_name), family=list(family="beta",link="logit")))


