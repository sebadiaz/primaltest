library(neuralnet)
library(rpart)

mydata = read.csv("MyData.csv")
boxplot(mydata$col14)
hist(mydata$col14)


mydata$quartile <- with(mydata, cut(mydata$col14,breaks=quantile(mydata$col14, probs=c(0, 0.25, 0.70, 0.91, 1), na.rm=TRUE),include.lowest=TRUE))
table(mydata$quartile)
mydata$quartileBin=as.numeric(mydata$quartile)
mydata<-mydata[complete.cases(mydata), ]


## 75% of the sample size
smp_size <- floor(0.75 * nrow(mydata))

## set the seed to make your partition reproductible
set.seed(123)
mydata_ind <- sample(seq_len(nrow(mydata)), size = smp_size)

train <- mydata[mydata_ind, ]
test <- mydata[-mydata_ind, ]
train_ <- train
test_ <- test

f <- as.formula("quartileBin ~ col2 + col3 + col4 + col5 + col6 + col7 + col8 + col9 + col10 + col11")
net<-neuralnet(f,data=train[,c(3:12,17)],hidden=c(100,100,100,50),linear.output=F)
print(net)
test.res=compute(net,test[,c(3:12)])$net.result
test<- test[order(test.res),]
table(as.integer(test.res),test$quartileBin)

fit<-rpart(f, data=train[,c(3:12,17)], method="class")
printcp(fit) # display the results
plotcp(fit) # visualize cross-validation results
summary(fit)