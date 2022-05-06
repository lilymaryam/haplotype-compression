import bte
import subprocess

def encode_newick(nwk_str):
    """
    Encode a newick string into a compressed string with only '(' and ')'
    """
    return ''.join([x for x in nwk_str if x == '(' or x == ')'])

for n in range(50, 1000, 50):
    print(f"=={n}==", flush=True)
    for i in range(0, 30, 1):
        # make mat
        cmd = f'./makeMat.sh vcf/pop_{n}_fixed_len_1e6_var_mutrate_{i}.vcf'
        print("RUNNING", cmd, flush=True)
        subprocess.run(cmd, shell=True)
        tree = bte.MATree(f'vcf/pop_{n}_fixed_len_1e6_var_mutrate_{i}.vcf.optimized.pb')
        nwk_str = tree.write_newick()
        mut_sets_list = []
        for node in tree.depth_first_expansion():
            mut_set = []
            for mut in node.mutations:
                mut = mut[1:]
                nuc = mut[-1]
                pos = int(mut[:-1])
                mut_set.append((pos, nuc))
            mut_sets_list.append(mut_set)

        # These values fully describe the MAT. They are in an easy-to-use format
        # Next step is to encode them into a binary string for on-disk storage

        # We can reduce the size needed for the Newick by removing node labels and commas
        # The commas are not needed because the tree is assumed to be binary
        # E.g.    (A,(B,(C,D)internal_2)internal_1)root; 
        # becomes ((()))
        enc_nwk = encode_newick(nwk_str)

        mat_str = ''

        mat_str += enc_nwk

        enc_mutsets = ''
        for mut_set in mut_sets_list:
            for mut in mut_set:
                enc_mutsets += str(mut[0]) + str(mut[1])
            enc_mutsets += ','


        mat_str += enc_mutsets

        print(f'{i}\t{len(mat_str)}', flush=True)
        # Now we convert the string to actual bytes and write them to disk
        with open('test.mat', 'w') as f:
            f.write(mat_str)

