mydata = read.csv("MyData.csv")
boxplot(mydata$col14)
hist(mydata$col14)


mydata$quartile <- with(mydata, cut(mydata$col14,breaks=quantile(mydata$col14, probs=c(0, 0.25, 0.70, 0.91, 1), na.rm=TRUE),include.lowest=TRUE))
table(mydata$quartile)
mydata$quartileBin=as.numeric(mydata$quartile)
mydata<-mydata[complete.cases(mydata), ]
library(neuralnet)
f <- as.formula("quartileBin ~ col2 + col3 + col4 + col5 + col6 + col7 + col8 + col9 + col10 + col11")
net<-neuralnet(f,data=mydata[,c(3:12,17)],hidden=c(1000,1000,1000),linear.output=F)