library(ggplot2)
#library(Cairo)
library(RColorBrewer)
library(cowplot)

fc=c("FC_4","FC_6","FC_10","FC_12","FC_17","FC_23","FC_26","FC_29","FC_41","FC_42")
hk=c("HK_2","HK_4","HK_5","HK_6","HK_7","HK_8","HK_9","HK_10","HK_11","HK_15")
ts=c("TS_4","TS_6","TS_17","TS_23","TS_31","TS_33","TS_34","TS_35","TS_36","TS_37")
zj=c("ZJ_3","ZJ_7","ZJ_8","ZJ_9","ZJ_12")
sz=c("SZ_3","SZ_4","SZ_5","SZ_22","SZ_23")
st=c("ST_16","ST_31","ST_32","ST_33","ST_34")
zz=c("DS_1","DS_2","DS_3","DS_4","DS_5")
wz=c("WZ_1","WZ_21","WZ_22","WZ_24","WZ_26")
zs=c("ZS_19","ZS_21","ZS_23","ZS_24","ZS_25")
ls=c("LS_2","LS_3","LS_7","LS_9","LS_11")
ly=c("LY_7","LY_14","LY_21","LY_42","LY_43")
wd=c("WD_40","WD_41","WD_44","WD_45","WD_46","WD_47","WD_48","WD_49","WD_50","WD_51")
yt=c("YT_3","YT_4","YT_5","YT_9","YT_11","YT_13","YT_14","YT_15","YT_16","YT_17")
tj=c("TJ_1","TJ_4","TJ_5","TJ_6","TJ_7","TJ_8","TJ_9","TJ_10","TJ_11","TJ_12")
order=c(fc,hk,ts,sz,zj,st,zz,wz,zs,ls,ly,wd,yt,tj)

col=list()
#b=brewer.pal(4,"Dark2")
b=c("#D1494E","#1C5595","#DBD0A7","#E69B21")
#for (i in seq(length(b))){b[i]=colorRampPalette(c(b[i],'#646464'))(3)[2]}
col[['2']]=b[1:2]
col[['3']]=b[c(1,3,2)]
col[['4']]=b[c(1,3,4,2)]
lp=list()
for (i in c('2','3','4')){
	file=paste("/public/storage/chenbh/newLM/pop/frappe/k",i,"/k",i,".result",sep="")
	d=read.table(file)
	d$V1=factor(d$V1,ordered=TRUE,levels=order)
	p=ggplot()+geom_bar(data=d,aes(x=V1,y=V2,fill=V3),stat="identity",position="stack")
	p=p+theme_bw()+ theme(legend.position = "none")
	p=p+theme(panel.grid.major =element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank(),axis.line = element_blank())
	p=p+theme(axis.text.y = element_blank(),axis.ticks = element_blank(),panel.border = element_blank())
	p=p+scale_fill_manual(values=col[[i]])
	p=p+theme(axis.title=element_text(size=18))
	p=p+ylab(paste("K=",i,sep=''))
	if (as.numeric(i)>2){
		p=p+theme(axis.title.x=element_blank())
		p=p+theme(axis.text=element_blank())
	}else{
		p=p+xlab("Individuals")
		p=p+theme(axis.text.x=element_text(angle=90,vjust=0.5,hjust=1,size=14))
		p=p+geom_rect(aes(xmin=c(0.5,30.5,70.5),xmax=c(30.5,70.5,100.5),ymin=rep(-0.09,3)),ymax=rep(-0.01,3),fill=col[['3']])
		p=p+geom_text(aes(x=c(15.5,50.5,85.5),y=c(rep(-0.05,3)),label=c('North','Middle','South')),color='white',size=9)
	}
	lp[[i]]=p
	ggsave(paste("/public/storage/chenbh/newLM/pop/frappe/k",i,".jpg",sep=""),lp[[i]],width=20,height=6)
}
p=plot_grid(lp[['4']],lp[['3']],lp[['2']],ncol = 1,nrow=3,align = "v",rel_heights=c(0.8,0.8,1.1))
save_plot('frappe.jpg',p,base_height=15,base_width=18)
