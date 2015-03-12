library(caret)
library(dplyr)


setwd('~/Projects/ml_titanic/m01')

train <- read.csv('../data/train.csv', header=T)
test <- read.csv('../data/test.csv', header=T)
test$Survived <- NA
all <- rbind(train, test)

classes <- lapply(all, function(x) class(x))
lapply(all, function(x) class(x))
lapply(all, function(x) sum(is.na(x)))
# for (i in 1:length(classes)) {
#   # print(i)
#   # print(classes[[i]])
#   if (classes[[i]]=="factor") {
#     all[,names(all)[i]][all[,names(all)[i]]==""] <- NA
#   }
# }

train$Survived <- factor(train$Survived)

inTrain <- createDataPartition(y=train$Survived, p=0.75, list=F)
train1 <- train[inTrain,]
test1 <- train[-inTrain,]

set.seed(1236)

# prep <- preProcess(train1[,-c(1:4, dim(train1)[2])], method="pca", thresh=.8)
# prep <- preProcess(train1[,-c(1:4, dim(train1)[2])], method="pca", pcaComp=13)

# trainpc <- predict(prep, train1[,-c(1:4, dim(train1)[2])])
# testpc <- predict(prep, test1[,-c(1:4, dim(train1)[2])])
# testspc <- predict(prep, tests[,-c(1:4, dim(train1)[2])])

fit <- train(Survived~Sex+Age+Pclass+Fare+Embarked+SibSp, method='rf', data=train1)

confusionMatrix(test1[,'Survived'], predict(fit, test1))

answers <- predict(fit, test)
answers <- cbind(answers, test$PassengerId)

write.csv(answers, file="results1.csv")