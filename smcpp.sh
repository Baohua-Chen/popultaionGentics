#!/bin/bash

pre=/public/data/chenbh/lc_reseq/pop/smcpp
vcf=/public/data/chenbh/lc_reseq/gt/vcfs/split/snp.HiC_scaffold_4.vcf.gz
pop=../pop.txt
refdict=/public/data/chenbh/lc_reseq/gt/ref/3d.dict

for i in inputs outputs logs
do
	if [[ ! -d $pre/$i ]]
	then
		mkdir $pre/$i
	fi
done

#plink --vcf $vcf --recode vcf --allow-extra-chr --out $pre/input && bgzip $pre/input.vcf

#awk '{a[$2]=a[$2]","$1}END{for (i in a){print i,a[i]}}' $pop |sed 's/ ,/ /' |sed 's/PT/LJ/g' > list

vcf2smc(){
#	chrs=$(cut -f 2,3 $refdict |sed 's/.N://g'|sort -k 2,2nr|head -n 24|cut -f 1)
	chrs=('HiC_scaffold_4')
	n=1
	cat $pre/list | while read p indvs
	do
		for i in $(echo $indvs|sed 's/,/ /g' )
		do
			for c in $chrs
			do
				if [[ $n -gt 6 ]]
				then
					echo wait
					n=1
				fi
				smc++ vcf2smc -c 5000 -d $i $i $pre/input.vcf.gz $pre/inputs/${p}.${c}.${i}.txt $c ${p}:$indvs 2>&1 >/dev/null &
				n=$((n+1))
			done
		done
	done
	wait
}

estimates(){
	for pop in `cut -d ' ' -f 1 list|grep -v LP`
	do
		smc++ estimate --knots 150 --em-iteration 200 -o $pre/outputs --cores 20 --base ${pop}.esti 2e-9 inputs/${pop}.*.*.txt 1>logs/${pop}.log 2>logs/${pop}.err &
	done
}

#vcf2smc
estimates
