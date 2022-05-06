from ete3 import Tree
import math
import sys

def encode_newick(nwk_str):
    """
    Encode a newick string into a compressed string with only '(' and ')'
    """
    return ''.join([x for x in nwk_str if x == '(' or x == ')'])

# def encode_mut_set(mut_set, m):
#     """
#     Encode a single set of mutations into a binary string
#     """
#     logm = math.ceil(math.log(m, 2))
#     enc = ''
#     for mut in mut_set:
#         pos = mut[0]
#         nuc = mut[1]
#         enc_pos = bin(pos)[2:].zfill(logm+1)
#         enc_nuc = bin(ord(nuc))[2:].zfill(8)
#         enc += enc_pos + enc_nuc
#     return enc

# def encode_mut_sets_list(mut_sets_list, m):
#     """
#     Encode a list of all sets of mutations into a binary string
#     """
#     enc = ''
#     for mut_set in mut_sets_list:
#        enc += encode_mut_set(mut_set, m) + '1'
#     return enc
    

# def decode_mut_sets_list(enc_mut_sets_list, m):
#     bin_str = ''.join([f'{x:0>8b}' for x in enc_mut_sets_list])
#     dec = ''
#     pointer = 0
#     logm = math.ceil(math.log(m, 2))
#     mut_sets_list = []
#     mut_set = []

#     while True:
#         chunksize = logm + 1
#         chunk = bin_str[pointer:pointer+chunksize]
#         if len(chunk) == 0 or chunk[0] == '0' and len(chunk) < chunksize:
#             break
#         if chunk[0] == '1':
#             mut_sets_list.append(mut_set)
#             mut_set = []
#             pointer += 1
#             continue
#         pointer += chunksize
#         pos = int(chunk, 2)
#         chunksize = 8
#         chunk = bin_str[pointer:pointer+chunksize]
#         nuc = chr(int(chunk, 2))
#         pointer += chunksize
#         mut_set.append((pos, nuc))
#     return mut_sets_list

########
# Main
########

# First we make a test MAT

# Create a dummy newick string
nwk_str = '(A,(B,(C,D)internal_2)internal_1)root;'
# 
#    /-A
# --|
#   |   /-B
#    \-|
#      |   /-C
#       \-|
#          \-D
#
# Annotate mutations along the edges by writing sets of mutations in postorder


mut_sets_list = [
    [ (35, 'C'), (444, 'G')], # e.g. these mutations are along the incoming edge to node A
    [ (352, 'A')], # B
    [ (1115, 'T'), (13415, 'A')], # C
    [ ], # D
    [ (3335, 'G'), (3523, 'A')], # E
    [ ], # internal_2
    [ (12345, 'C')], # internal_1
    [ ], # root
]
m = 13415 # max genomic coordinate

# These values fully describe the MAT. They are in an easy-to-use format
# Next step is to encode them into a binary string for on-disk storage
print("Unencoded newick", nwk_str)
print("Unencoded mutation sets", mut_sets_list)

# We can reduce the size needed for the Newick by removing node labels and commas
# The commas are not needed because the tree is assumed to be binary
# E.g.    (A,(B,(C,D)internal_2)internal_1)root; 
# becomes ((()))
enc_nwk = encode_newick(nwk_str)
print("Encoded newick", enc_nwk)

# Next we write the bytes for this encoded string to disk (1 byte per character)
with open('test.mat', 'w') as f:
    f.write(enc_nwk)

enc_mutsets = ''
for mut_set in mut_sets_list:
    for mut in mut_set:
        enc_mutsets += str(mut[0]) + str(mut[1])
    enc_mutsets += ','

print("Encoded mutation sets", enc_mutsets)

# Now we convert the string to actual bytes and write them to disk
with open('test.mat', 'a') as f:
    f.write(enc_mutsets)


# Read the encoded MAT from disk
# with open('test.bin', 'rb') as f:
#     counter = 1
#     enc_nwk = f.read(1)
#     while counter != 0:
#         c = f.read(1)
#         if c == b'(':
#             counter += 1
#         elif c == b')':
#             counter -= 1
#         enc_nwk += c
#     print("Recovered newick from file", enc_nwk)
#     enc_mut_sets_list = f.read()
#     mut_sets_list = decode_mut_sets_list(enc_mut_sets_list, m)
#     print("Recovered mutation sets from file", mut_sets_list)




# mat = Tree(nwk_str, format=1)
# i = 0
# for n in mat.traverse('postorder'):
#     n.mutations = mut_sets_list[i] # annotate the incoming edge to the node with mutations
#   i += 1