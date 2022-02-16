#!/usr/bin/Rscript

source('/home/softwares/treemix/src/plotting_funcs.R')
for (i in 0:10){
	jpeg(paste('plots/m',i,'.jpg',sep=''),height=1000, width=1000)
	print(paste('m',i,'/treemix.m',i,sep=''))
	plot_tree(paste('m',i,'/treemix.m',i,sep=''))
	dev.off()
}
