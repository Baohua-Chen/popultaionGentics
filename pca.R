#!/usr/bin/Rscript
#library(SNPRelate)
library(ggplot2)
library(ggforce)
library(ggnewscale)
library(car)
library(RColorBrewer)
library(showtext)

font_add('simheiArial', '/public/student/chenbh/fonts/simheiArial.ttf')
vcf2gds=function(){
	snpgdsVCF2GDS("snp.vcf.gz", "snp.gds", method = "biallelic.only")
}

indvLst=function(){
	zs<<-c("ZS_01","ZS_02","ZS_03","ZS_07","ZS_08","ZS_09","ZS_10","ZS_11","ZS_12","ZS_13","ZS_14","ZS_15","ZS_16","ZS_17","ZS_18","ZS_19","ZS_21")
	fd<<-c("FD_01","FD_02","FD_03","FD_05","FD_06","FD_07","FD_08","FD_15","FD_17","FD_21","FD_23","FD_26","FD_28","FD_31","FD_32","FD_33")
	dy<<-c("DY_01","DY_02","DY_03","DY_04","DY_05")
	ff<<-c("FF_01","FF_02","FF_03","FF_04","FF_05","FF_06","FF_07","FF_08","FF_09","FF_10")
	lj<<-c("LJ_01","LJ_02","LJ_03","LJ_04","LJ_05","LJ_06","LJ_07","LJ_08","LJ_09","LJ_10","LJ_11","LJ_12","LJ_13","LJ_14","LJ_15")
	xm<<-c("XM_03","XM_05","XM_10","XM_11","XM_15","XM_17","XM_18")
	ds<<-c("DS_01","DS_02","DS_23","DS_24","DS_25","DS_26","DS_27","DS_28","DS_29","DS_30","DS_31","DS_32","DS_33")
	zj<<-c("ZJ_03","ZJ_04","ZJ_05","ZJ_06","ZJ_07","ZJ_08","ZJ_09","ZJ_14","ZJ_16","ZJ_17","ZJ_21","ZJ_22","ZJ_23","ZJ_25","ZJ_27","ZJ_29")
	xw<<-c("XW_01","XW_06","XW_13","XW_15","XW_16","XW_17","XW_23","XW_24","XW_37","XW_38","XW_40","XW_42")
	lp<<-c("LP_01")
	samples<<-c(zs,fd,dy,ff,lj,ds,zj,xw)
	pops<<-c('ZS','FD','DY','FF','PT', 'DS','ZJ','XW')
}

run=function(){
	genofile <- snpgdsOpen("snp.gds")
	indvLst()
	pca <- snpgdsPCA(genofile,sample.id=samples,autosome.only=FALSE,maf=NaN,)
	pc.percent <<- head(format(pca$varprop*100,digits=2), 2)
	a=c()
	for (i in pca$sample.id){a=c(a,strsplit(i,"_")[[1]][1])}
	tab <<- data.frame(sample.id = pca$sample.id, EV1 = pca$eigenvect[,1], EV2 = pca$eigenvect[,2], POP=a, stringsAsFactors =F)
	tab$POP=factor(gsub('LJ', 'PT', tab$POP), ordered=TRUE, levels=pops)
	write.table(tab,file="pca.txt",quote=FALSE,sep="\t",eol = "\n", na = "NA", dec = ".", row.names = TRUE,col.names = TRUE, qmethod = c("escape", "double"),fileEncoding = "utf-8")
	print(pc.percent)
}
calEllipse=function(){
	tab1=transform(tab,SP=ifelse(sample.id %in% c(zs),"DQ",ifelse(sample.id %in% c(xw, zj, ds, xm, lj),"NH","MD")))
	tn=tab1[tab1$SP=='DQ',]
	ts=tab1[tab1$SP=='NH',]
	tm=tab1[tab1$SP=='MD',]
	en<<-data.frame(dataEllipse(tn$EV1,tn$EV2,level=0.95,segment=200))
	es<<-data.frame(dataEllipse(ts$EV1,ts$EV2,level=0.95,segment=200))
	em<<-data.frame(dataEllipse(tm$EV1,tm$EV2,level=0.95,segment=200))
}
plot=function(n){
	f='pca.jpg'
	indvLst()
	tab$sample.id=factor(tab$sample.id,ordered=TRUE,levels=samples)
	tab$POP=factor(gsub('LJ','PT',tab$POP),ordered=TRUE,levels=pops)
	tab=transform(tab,SP=ifelse(sample.id %in% c(zs),"DQ",ifelse(sample.id %in% c(xw, zj, ds, xm, lj),"NH","MD")))
	popColors=c('XW'='#FE4365','ZJ'='#FC9D9A', 'DS'='#EDE574', 'PT'='#F9CDAD', 'FF'='#C06C84', 'DY'='#C8C8A9', 'FD'='#45ADA8', 'ZS'='#9DE0AD')
   	stockColors=c('NH'='#FE4365', 'MD'='#F9CDAD', 'DQ'='#83AF9B')
	p = ggplot()
	p = p+stat_ellipse(data=tab, aes(x=EV1, y=EV2, fill=SP), geom='polygon', type='norm', alpha=0.5, level=0.95)
	p = p+scale_fill_manual('Stocks', values=stockColors)+new_scale('fill')
	p = p+geom_point(data=tab, aes(x=EV1,y=EV2,fill=POP), color='black', size=0.5*n, shape=21)
	p = p+scale_fill_manual('Sites', values=popColors)+new_scale('fill')
	p = p+theme_bw()+theme(text = element_text(family = 'simheiArial'))
	p = p+theme(axis.text=element_text(size=2*n),axis.title=element_text(size=2.5*n,face="bold"),legend.text=element_text(size=2*n),legend.title=element_text(size=2.5*n))
	p = p+theme(legend.position=c(0.1,0.25))
	p = p+xlab(paste('PC1 (', 2, '%)', sep=''))
	p = p+ylab(paste('PC2 (', 1, '%)', sep=''))
	ggsave(f,p,width=1200*n,height=1200*n,units="px", limitsize = FALSE, dpi=1200)
}
indvLst()
vcf2gds()
run()
tab=read.table('pca.txt')
calEllipse()
plot(10)
