# This script performs the following steps:
# 1. Read in a haplotype panel
# 2. Infer a maximum-parsimony tree for the panel using UShER+matOptimize
# 3. Encode a mutation-annotated tree in the format described in the manuscript

python3 make_mat.py -t tree.nwk -m mutations.tsv -o tree.mat