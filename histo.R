library(neuralnet)
library(rpart)
library(ade4)

mydata = read.csv("MyData.csv")
boxplot(mydata$col12)
hist(mydata$col12)


mydata$quartile <- with(mydata, cut(mydata$col12,breaks=quantile(mydata$col12, probs=c(0, 0.25, 0.70, 0.91, 1), na.rm=TRUE),include.lowest=TRUE))
table(mydata$quartile)
mydata$quartileBin=as.numeric(mydata$quartile)
mydata=cbind(mydata,acm.disjonctif(data.frame(mydata$quartile)))
mydata<-mydata[complete.cases(mydata), ]
colnames(mydata)[16:19] <- c("col16","col17","col18","col19")

## 75% of the sample size
smp_size <- floor(0.75 * nrow(mydata))

## set the seed to make your partition reproductible
set.seed(123)
mydata_ind <- sample(seq_len(nrow(mydata)), size = smp_size)

train <- mydata[mydata_ind, ]
test <- mydata[-mydata_ind, ]
train_ <- train
test_ <- test

f <- as.formula("col16+col17+col18+col19 ~ col2 + col3 + col4 + col5 + col6 + col7 + col8 + col9 + col10 + col11")

net<-neuralnet(f,data=train[,c(3:12,16:19)],hidden=c(100,100,100),linear.output=F,rep=20,algorithm="rprop+")
print(net)
test.res=compute(net,test[,c(3:12)])$net.result

length(test.res[,1])
length(test_$col16)
table(round(test.res[,1]) , test_$col16)
table(round(test.res[,2]) , test_$col17)
table(round(test.res[,3]) , test_$col18)
table(round(test.res[,4]) , test_$col19)

