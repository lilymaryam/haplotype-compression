import matplotlib.pyplot as plt

pbwt = {}
mat = {}

curr_pop = 0
with open('pbwt_results_var_mutrate.txt', 'r') as f:
    for line in f:
        if line[0] == '=':
            curr_pop = int(line.replace('=', '').strip())
            continue
        nsites = int(line.split()[0])
        size = int(line.split()[2])
        if curr_pop not in pbwt:
            pbwt[curr_pop] = [(nsites, size)]
        else:
            pbwt[curr_pop].append((nsites, size))

curr_pop = 0
mat = {}
with open('mat_results_filtered.txt', 'r') as f:
    for line in f:
        if line[0] == '=':
            curr_pop = int(line.replace('=', '').strip())
            counter = 0
            continue
        size = int(line.split()[1])
        nsites = pbwt[curr_pop][counter][0]
        if curr_pop not in mat:
            mat[curr_pop] = [(nsites, size)]
        else:
            mat[curr_pop].append((nsites, size))
        counter += 1

for pop in mat:
    print(pop)
    plt.plot([x[0] for x in mat[pop]], [x[1] for x in mat[pop]], lw=0, marker='o', ms=1)
    plt.plot([x[0] for x in pbwt[pop]], [x[1] for x in pbwt[pop]], lw=0, marker='o', ms=1)
    plt.savefig(f'test_{pop}.png', dpi=600)