library(xgboost)

facts = read.table("data/GUM9/GUM_facts.tab", stringsAsFactors = T, header=T,sep = "\t")

names(facts)[names(facts) == "gold_head_dep_func"] <- "syntax_func"
names(facts)[names(facts) == "gold_interpara"] <- "interpara"
names(facts)[names(facts) == "gold_child_count"] <- "children"
names(facts)[names(facts) == "gold_descendant_count"] <- "descendants"
names(facts)[names(facts) == "gold_rel_class"] <- "rel"
names(facts)[names(facts) == "edu_oov_rate"] <- "oov"
names(facts)[names(facts) == "gold_inersent"] <- "intersent"

dev = subset(facts,partition=="dev")
dev = droplevels(dev)
dev$is_err_bot = dev$attach_label_error_count_bot > 2. # attach_label_error_count_bot
dev$is_err_top = dev$attach_label_error_count_top > 2. # attach_label_error_count_bot

test = subset(facts,partition=="test")
test = droplevels(test)
test$is_err_bot = test$attach_label_error_count_bot > 2. # attach_label_error_count_bot
test$is_err_top = test$attach_label_error_count_top > 2. # attach_label_error_count_bot


feats_r = c("genre","edu_len","oov","dm","syntax_func")
feats_f = c("genre","edu_len","oov","dm","distractor","intersent","interpara","children","descendants","rel","syntax_func")


# realistic model bot
dtrain_r_bot <- xgb.DMatrix(data = data.matrix(dev[,feats_r]), label=data.matrix(dev[,"is_err_bot"]))
dtest_r_bot <- xgb.DMatrix(data = data.matrix(test[,feats_r]), label=data.matrix(test[,"is_err_bot"]))

clf_r_bot = xgboost(data=dtrain_r_bot, nrounds = 15, objective = "binary:logistic", verbose = 2)
pred_r_bot <- predict(clf_r_bot, data.matrix(test[,feats_r]))
xtab_r_bot = table(pred_r_bot>0.5,test[,"is_err_bot"])
acc_r_bot = sum(diag(xtab_r_bot))/sum(xtab_r_bot)
acc_r_bot

importance_matrix_r_bot <- xgb.importance(model = clf_r_bot)
print(importance_matrix_r_bot)
p1<-xgb.plot.importance(importance_matrix = importance_matrix_r_bot)


# realistic model top
dtrain_r_top <- xgb.DMatrix(data = data.matrix(dev[,feats_r]), label=data.matrix(dev[,"is_err_top"]))
dtest_r_top <- xgb.DMatrix(data = data.matrix(test[,feats_r]), label=data.matrix(test[,"is_err_top"]))

clf_r_top = xgboost(data=dtrain_r_top, nrounds = 15, objective = "binary:logistic", verbose = 2)
pred_r_top <- predict(clf_r_bot, data.matrix(test[,feats_r]))
xtab_r_top = table(pred_r_bot>0.5,test[,"is_err_top"])
acc_r_top = sum(diag(xtab_r_top))/sum(xtab_r_top)
acc_r_top

importance_matrix_r_top <- xgb.importance(model = clf_r_top)
print(importance_matrix_r_top)
p1<-xgb.plot.importance(importance_matrix = importance_matrix_r_top)


# fulll model bottom up
dtrain_f_bot <- xgb.DMatrix(data = data.matrix(dev[,feats_f]), label=data.matrix(dev[,"is_err_bot"]))
dtest_f_bot <- xgb.DMatrix(data = data.matrix(test[,feats_f]), label=data.matrix(test[,"is_err_bot"]))

clf_f_bot = xgboost(data=dtrain_f_bot, nrounds = 15, objective = "binary:logistic", verbose = 2)
pred_f_bot <- predict(clf_f_bot, data.matrix(test[,feats_f]))
xtab_f_bot = table(pred_f_bot>0.5,test[,"is_err_bot"])
acc_f_bot = sum(diag(xtab_f_bot))/sum(xtab_f_bot)
acc_f_bot

importance_matrix_f_bot <- xgb.importance(model = clf_f_bot)
print(importance_matrix_f_bot)
p1<-xgb.plot.importance(importance_matrix = importance_matrix_f_bot)


# fulll model topdown
dtrain_f_top <- xgb.DMatrix(data = data.matrix(dev[,feats_f]), label=data.matrix(dev[,"is_err_top"]))
dtest_f_top <- xgb.DMatrix(data = data.matrix(test[,feats_f]), label=data.matrix(test[,"is_err_top"]))

clf_f_top = xgboost(data=dtrain_f_top, nrounds = 15, objective = "binary:logistic", verbose = 2)
pred_f_top <- predict(clf_f_top, data.matrix(test[,feats_f]))
xtab_f_top = table(pred_f_bot>0.5,test[,"is_err_top"])
acc_f_top = sum(diag(xtab_f_top))/sum(xtab_f_top)
acc_f_top

importance_matrix_f_top <- xgb.importance(model = clf_f_top)
print(importance_matrix_f_top)
p1<-xgb.plot.importance(importance_matrix = importance_matrix_f_top)



library(Ckmeans.1d.dp)
library(ggplot2)
library(gridExtra)

# par(mfrow=c(2,1))
# importance_matrix1 <- xgb.importance(model = clf_r)
# p1<-xgb.ggplot.importance(importance_matrix = importance_matrix1, n_clusters=2)
# importance_matrix2 <- xgb.importance(model = clf_f)
# p2<-xgb.ggplot.importance(importance_matrix = importance_matrix2, n_clusters=2)
# par(mfrow=c(1,1))

# grid.arrange(p1, p2,nrow = 2)

p1<-xgb.ggplot.importance(importance_matrix = importance_matrix_r_bot, n_clusters=2)
p2<-xgb.ggplot.importance(importance_matrix = importance_matrix_r_top, n_clusters=2)
p3<-xgb.ggplot.importance(importance_matrix = importance_matrix_f_bot, n_clusters=2)
p4<-xgb.ggplot.importance(importance_matrix = importance_matrix_f_top, n_clusters=2)
grid.arrange(p1+theme(legend.position = "none"), p2+theme(legend.position = "none"), 
             p3+theme(legend.position = "none"), p4+theme(legend.position = "none"), nrow = 2)



