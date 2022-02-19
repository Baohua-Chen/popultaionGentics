#!/usr/bin/python3

import os
import sys
from subprocess import Popen
import pandas as pd
import vcf2phy
from multiprocessing import Pool


def subVcf(i):
    try:
        os.mkdir(f'{pre}/sub{i:d}')
    except FileExistsError:
        pass
    sd = d.loc[d.index%n==i]
    sd[2].to_csv(f'{pre}/sub{i:d}/snps', sep='\t', header=None, index=None)
    log = open(f'{pre}/sub{i:d}/sub{i:d}.log', 'w')
    log.write(f'Spliting vcf file using bcftools.\n')
	log.flush()
    err = open(f'{pre}/sub{i:d}/sub{i:d}.err', 'w')
    p = Popen(f'bcftools view --include ID==@{pre}/sub{i:d}/snps {vcf} -O z -o {pre}/sub{i:d}/sub{i:d}.vcf.gz', shell=True, stdout=log, stderr=err)
    p.wait()
    sys.stdout, sys.stderr = log, err
    args = vcf2phy.args_parse()
    args.filename = f'{pre}/sub{i:d}/sub{i:d}.vcf.gz'
    args.folder = f'{pre}/sub{i:d}'
    args.prefix = f'sub{i:d}'
    log.write(f'Converting vcf file to phylip format.\n')
	log.flush()
    vcf2phy.convert(args)
    sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__

def runIqtree(i):
    cmd = f'iqtree2 -s {pre}/sub{i:d}/sub{i:d}.min4.phy --seqtype DNA --prefix {pre}/sub{i:d}/sub{i:d} --seed 100000 -B 1000 -nt 22 -bnni -cmax 15'
    log = open(f'{pre}/sub{i:d}/sub{i:d}.log', 'w')
    err = open(f'{pre}/sub{i:d}/sub{i:d}.err', 'w')
    log.write(f'Building subtree using iqtree2.\nCMD: {cmd}\n')
	log.flush()
    p = Popen(cmd, shell=True, stdout=log, stderr=err)
    p.wait()

def splitVcf(n1):

    def makeInfo():
        p = Popen(f'bcftools query -f"%CHROM\t%POS\t%ID\t%REF\t%ALT\n" {vcf} > {pre}/vcf.info', shell=True)
        p.wait()

    global d
    #makeInfo()
    d = pd.read_csv(f'{pre}/vcf.info', sep='\t', header=None)
    pool = Pool(n1)
    pool.map(subVcf, range(n1))
    pool.close()
    pool.join()

def buildTree(n1, n2):
    pool = Pool(n2)
    pool.map(runIqtree, range(n1))
    pool.close()
    pool.join()

def main(n1, n2):
#    splitVcf(n1)
    buildTree(n1, n2)

if __name__ == '__main__':
    vcf = 'snp.prune.noxm.vcf.gz'
    pre = '/homes/chenbh/lc_reseq/iqtree'
    main(10, 4)
