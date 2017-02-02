library(lme4)

nbValue=10
space=2
dat = read.csv("complete.csv", header = FALSE,sep = ";", dec=",")
dat$V2=paste(substr(dat$V2,0,6),"20",substr(dat$V2,7,9),sep="")

dat$V2=as.numeric(as.Date(dat$V2, format = "%d/%m/%Y"))
listV1=levels(unique(dat$V1))
list<-lmList(V6 ~ V2 | V1, data=dat)

coeff<-coef(list)
coeff[,-1]

dat<-dat[order(dat[,1],dat[,2]),]
iv=1
byrowsSol<-data.frame(matrix(NA,nrow=0,ncol=14))
for (ch in listV1) {
  selOne<-dat[dat$V1==ch,]
  
  for (iv in 1:(nrow(selOne)-1)) {
    if(iv+nbValue-1<nrow(selOne)&&!is.nan(selOne[(iv+nbValue-1),]$V6)){
      lineComp<-cbind(ch,t(scale(selOne[iv:(iv+nbValue-1),]$V6,center = TRUE,scale = TRUE)))
      lineComp[2:nbValue]<-as.numeric(lineComp[2:nbValue])

      lineComp=data.frame(lineComp)
      lineComp[2:nbValue+1]<-lapply(lineComp[2:nbValue+1], function(x) as.numeric(as.character(x)))
      lineComp<-cbind(lineComp,data.frame((selOne[(iv+nbValue),]$V6-selOne[(iv+nbValue-1),]$V6)/selOne[(iv+nbValue),]$V6))
      colnames(lineComp) <- paste("col", (1:(nbValue+2)), sep = "")
      byrowsSol<-rbind(byrowsSol,lineComp)
    }
  }
}
write.csv(byrowsSol, file = "MyData.csv")
