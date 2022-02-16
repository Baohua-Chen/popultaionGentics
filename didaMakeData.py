#!/home/bin/python3

import dadi

pop = ['GX','ND','DQ']
vcf = '../../../../gt/prune/snp.prune.noxm.vcf.gz'
pop_file = '../../../pop.txt'

dd = dadi.Misc.make_data_dict_vcf(vcf, pop_file)
fout=open('dadi.input.txt','w')
print('\t'.join(['Ingroup','Outgroup','Allele1']+pop+['Allele2']+pop+['Gene','Position']),file=fout)
for i in dd.keys():
    l1,l2=[],[]
    for p in pop:
        if p in dd[i]['calls'].keys():
            l1.append(dd[i]['calls'][p][0])
            l2.append(dd[i]['calls'][p][1])
        else:
            l1.append(0)
            l2.append(0)
    l=[dd[i]['context']]
    l.append(dd[i]['outgroup_context'])
    l.append(dd[i]['segregating'][0])
    l=l+l1
    l.append(dd[i]['segregating'][1])
    l=l+l2
    t=i.split('_')
    pos=t.pop(-1)
    gene='_'.join(t)
    l.append(gene)
    l.append(pos)
    l=[ str(i) for i in l ]
    print('\t'.join(l),file=fout)
fout.close()
