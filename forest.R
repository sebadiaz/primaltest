library(neuralnet)
library(rpart)
library(ade4)

mydata = read.csv("MyDataDiff.csv")
boxplot(mydata$col11)
hist(mydata$col11)


mydata$quartile <- with(mydata, cut(mydata$col11,breaks=quantile(mydata$col11, probs=c(0, 0.25, 0.70, 0.91, 1), na.rm=TRUE),include.lowest=TRUE))
table(mydata$quartile)
mydata$quartileBin=as.numeric(mydata$quartile)
mydata=cbind(mydata,acm.disjonctif(data.frame(mydata$quartile)))
mydata<-mydata[complete.cases(mydata), ]
colnames(mydata)[15:18] <- c("col16","col17","col18","col19")

## 75% of the sample size
smp_size <- floor(0.75 * nrow(mydata))

## set the seed to make your partition reproductible
set.seed(123)
mydata_ind <- sample(seq_len(nrow(mydata)), size = smp_size)

train <- mydata[mydata_ind, ]
test <- mydata[-mydata_ind, ]
train_ <- train
test_ <- test

fable.res <- rpart (quartile ~ col2 + col3 + col4 + col5 + col6 + col7 + col8 + col9 + col10, train)
plot(tree.res)

table(test$quartile, predict(fable.res, test_,type="class"))

library(randomForest)
fit <- randomForest(quartile ~ col2 + col3 + col4 + col5 + col6 + col7 + col8 + col9 + col10,   data=train)
print(fit) # view results 
importance(fit)