install.packages("xlsx")
library("xlsx")

ad_detail_path<-"G:/touchpal/天天新闻/ad_stastic.xlsx"
ad_detail<-read.csv(file = "G:/touchpal/code/graph/ad_stastic.csv",header=TRUE)

ad_detail$代码位ID<-factor(ad_detail$代码位ID)
ad_detail<-na.omit(ad_detail) #delete na rows
#translate into date
ad_detail$时间<-as.character(ad_detail$时间)
ad_detail$时间<-as.Date(ad_detail$时间,format='%Y%m%d')

detail_colnames<-colnames(ad_detail)
detail_colnames[12:13]<-c('填充率','点击率')

ad_detail1<-ad_detail[ad_detail$APP=='触宝电话',]
colnames(ad_detail1)<-detail_colnames
ad_detail1<- subset(ad_detail1,select = -c(点击收入,展现收入,填充率))

library(ggplot2)

#ggplot(data=ad_detail,aes(时间,收入,color=代码位ID,label=收入))+geom_point(na.rm=TRUE)+
 # geom_line()+scale_x_date(date_breaks = '1 week')+
  #geom_text()

p<-ggplot(data=ad_detail1)
p+geom_line(aes(时间,展现,color=代码位ID))+geom_point(aes(时间,展现,color=代码位ID))+
  facet_wrap(~代码位,ncol = 4)+guides(color=FALSE)
p+geom_line(aes(时间,点击,color=代码位ID))+geom_point(aes(时间,点击,color=代码位ID))+facet_wrap(~代码位,ncol = 4)+guides(color=FALSE)
p+geom_line(aes(时间,收入,color=代码位ID))+geom_point(aes(时间,收入,color=代码位ID))+facet_wrap(~代码位,ncol = 4)+guides(color=FALSE)

p+geom_line(aes(时间,展现,color='展现'))+geom_line(aes(时间,点击,color='点击'))+
  geom_point(aes(时间,展现,color='展现'))+geom_point(aes(时间,点击,color='点击'))+
  facet_wrap(~代码位,ncol = 4)

#twoord
install.packages("twoord")
#填充背景
day<-unique(strptime(ad_detail1$时间,format='%Y-%m-%d'))
time_df<-data.frame(min=day,max=day+60*60*24*7,fill=as.factor(as.character(day)))
p<-ggplot(data=ad_detail1)
p+geom_rect(data=time_df,aes(xmin=min,xmax=max,ymin=min(ad_detail1$点击),ymax=max(ad_detail1$点击),fill=fill))+
  geom_line(aes(时间,点击))+scale_x_date(date_breaks = '2 day')#error
  


#微信数据可视化
getwd()
setwd("G:/Workspaces/python/itchat")

###导入数据
library(xlsx)
friends <- read.xlsx('wechatFriends.xlsx', header=TRUE, sheetName = "Sheet1", stringsAsFactors=F , encoding='UTF-8')
#用“未知”标识空的城市、省份
friends[is.na(friends$城市),]$城市 <- "未知"
friends[is.na(friends$省份),]$省份 <- "未知"
#用“海外”标识海外的城市、省份，即若字符串为英文则替换为“海外” 【知识点1：正则表达式】
friends[grep("\\w", substr(friends$省份,1,1)),]$省份 <- "海外"
friends[grep("\\w", substr(friends$城市,1,1)),]$城市 <- "海外"

###基础数据准备
install.packages("sqldf")
library(sqldf)
##sex
#基于sqldf包，统计不同性别的人数，使用SQL语句，返回结果为数据框，下同【知识点2：SQL语句】
sex <- sqldf("select 性别, count(*) as 人数 from friends group by 性别")
sex$性别 <- c("未知","男","女")
##province
#统计不同省份的人数
province <- sqldf("select 省份, count(*) as 人数 from friends group by 省份")
##city
#统计不同城市的人数
city <- sqldf("select 城市, count(*) as 人数 from friends group by 城市")

###数据可视化
##微信好友地区分布排名--条形图
library(ggplot2)
#将好友数大于或等于3的城市选出，将好友数不足3的城市统一为“其他”，并统计其他城市的好友总数；最后，创建新的数据框city_new
city_new <- rbind(city[which(city$人数>=3),], c("其他", sum(city[-which(city$人数>=3),]$人数)))
city_new$人数 <- as.integer(city_new$人数)
#利用ggplot2包的ggplot()函数制作“微信好友地区分布排名”图【知识点3：ggplot作图】
#在作图时，为使条形图从高到低依次排序，在aes()中使用reorder()函数【知识点4：reorder()函数】
ggplot(data = city_new, mapping = aes(x=reorder(city_new$城市,-city_new$人数), y = city_new$人数, fill = -city_new$人数)) + 
  geom_bar(stat = "identity") + 
  labs(x="城市",y="人数", title = "微 信 好 友 地 区 分 布 排 名") +
  geom_text(mapping = aes(label = city_new$人数), size = 3.5, colour = "darkblue", vjust = -0.6) + 
  theme(legend.position='none',
        text = element_text(family = 'STSong'), 
        axis.title.y=element_text(angle=0, vjust = 0.5),
        plot.title = element_text(size=16, hjust = 0.5),
        axis.title = element_text(size = 13),
        axis.text.x = element_text(vjust = 0.5, color = "black", size=10))