#!/bin/bash

#plink --file ../../../gt/prune/snp.prune.noxm --freq --out snp.prune.noxm --allow-extra-chr --within <( cut -f 1  ../../pop.txt |sed 's/\(.*\)_\(.*\)/\1\t\2\t\1/' )
#gzip -f snp.prune.noxm.frq.strat
#./plink2treemix.py snp.prune.noxm.frq.strat.gz /dev/stdout | gzip -c > treemix.input.txt.gz
if [[ ! -d m0 ]]
then
	mkdir m0
fi
treemix -i snp.prune.noxm.txt.gz -o m0/treemix.m0 -root ZS -noss -global -se -tf /public/data/chenbh/lc_reseq/pop/snp/sambaR/SambaR_output/Divergence/lc.ds.nj.nwk 1> logs/m0.log 2>&1 &

for i in `seq 1 10`
do
	if [[ ! -d  $i ]]
	then
		mkdir m$i
	fi
	treemix -i snp.prune.noxm.txt.gz -o m$i/treemix.m$i -root ZS -noss -global -m $i -se -tf /public/data/chenbh/lc_reseq/pop/snp/sambaR/SambaR_output/Divergence/lc.ds.nj.nwk 1> logs/m${i}.log 2>&1 &
done
wait


