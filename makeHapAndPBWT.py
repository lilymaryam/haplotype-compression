import msprime
import pbwt
import numpy as np
import sys


mut_rates = np.linspace(1e-6, 1e-3, num=30)

for n in range(50, 1000, 50):
    print(f"=={n}==", flush=True)
    for i,m in enumerate(mut_rates):
        ts = msprime.sim_ancestry(n, ploidy=1, sequence_length=1e6)
        mts = msprime.sim_mutations(ts, rate=m, random_seed=1)
        mts.write_vcf(open(f'vcf/pop_{n}_fixed_len_1e6_var_mutrate_{i}.vcf', 'w'))

        # make pbwt
        haps = {}
        for var in mts.variants():
            for i, g in enumerate(var.genotypes):
                if i in haps:
                    haps[i].append(var.alleles[g])
                else:
                    haps[i] = [var.alleles[g]]
        X = [''.join(haps[i]) for i in haps]

        #print("X is", X)

        conversionAlph = {'A':'0', 'C':'1', 'G':'2', 'T':'3'}
        alph = ['0','1', '2', '3']
        X = pbwt.convertXtoInts(X, conversionAlph)
        Y = pbwt.constructYFromX(X, alph)

        #print(pbwt.compressYMat(Y,conversionAlph))


        output_pbwt = ','.join(pbwt.compressYMat(Y,conversionAlph))


        #print(output_pbwt)
        print(f'{len(list(mts.variants()))}\t{m}\t{len(output_pbwt)}', flush=True)
