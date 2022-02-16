#!/bin/bash

pre=/public/data/chenbh/lc_reseq/gt/prune/snp.prune.noxm
#plink --file $pre --recode 12 --allow-extra-chr --out frappe
#sed 's/^[^\t]*\([0-9]\+\)\t/c\1\t/g' frappe.map -i
markers=`cat frappe.map|wc -l`
indvs=`cat frappe.nosex|wc -l`
runFrappe(){
for i in `seq 6 10`
do
	rm -fr ./k$i
	mkdir ./k$i
	sed 's/%K%/'$i'/g' ./parm_example.txt | sed 's/%M%/'$markers'/g' | sed 's/%I%/'$indvs'/g' > ./k$i/parm_k${i}.txt
	cd ./k$i
	sleep 0.1
	ln -s ../frappe.ped ./data.ped
	ln -s ../frappe.map ./data.map
	ln -s ../frappe.nosex ./data.nosex
	nohup frappe parm_k${i}.txt > frappe_k${i}.log 2>&1 &
	sleep 0.1
	cd ..
	sleep 0.1
done
wait
}

barplot(){
	./structruePlot.py
	./structruePlotK10.py
}

runFrappe
plot
