'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import numpy as np


# Load data
data = np.load('../Data/Compressibility.npz')

x = data['x']
phi = data['phi']
y_A = data['y_A']
y_C = data['y_C']
y_S = data['y_S']
p = data['p']
K_vec = data['K_vec']
n = data['n']



# Plot
fig, axs = plt.subplots(2, 2, figsize=(30, 20))
labelsize = 40
lw = 4
legend_width = 6
xlim = 0.05
markers = ['--', ':', '-', '-.']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

axs[0,0].plot(0, 0, label='Incompressible', color=colors[0])
[axs[0,0].plot(0, 0, label=f'$\kappa$ = {K_vec[i]}', color=colors[i]) for i in range(1, len(K_vec))]

[axs[0,0].plot(x[i], phi[i], lw=lw, color=colors[i]) for i in range(len(K_vec))]
axs[0,0].set_xlim(0,xlim)
axs[0,0].grid()
axs[0,0].set_xlabel('x [-]', fontsize=labelsize)
axs[0,0].set_ylabel('$\\varphi$ [-]', fontsize=labelsize)
axs[0,0].tick_params(axis='both', labelsize=labelsize)


for i in range(len(K_vec)):
    clr = colors[i]
    axs[0,1].plot(x[i], y_A[i], markers[0], color=clr, lw=lw)
    axs[0,1].plot(x[i], y_C[i], markers[1], color=clr, lw=lw)
axs[0,1].plot(0, 0.1, color='grey', linestyle=markers[0], label='Anions')
axs[0,1].plot(0, 0.1, color='grey', linestyle=markers[1], label='Cations')
axs[0,1].set_xlim(0,xlim)
axs[0,1].grid()
axs[0,1].set_xlabel('x [-]', fontsize=labelsize)
axs[0,1].set_ylabel('$y_\\alpha$ [-]', fontsize=labelsize)
axs[0,1].tick_params(axis='both', labelsize=labelsize)

# a = plt.axes([.75, .77, .2, .2])
# for i in range(len(K_vec)):
#     clr = colors[i]
#     a.plot(x[i], y_S[i], markers[0], color=clr, lw=lw)
# axs[0,1].plot(0, 0.1, color='grey', linestyle='--', label='Solvent')
# a.set_xlim(0,xlim)
# a.grid()
# a.set_xlabel('$x [-]$', fontsize=labelsize)
# a.set_ylabel('$y_S$ [-]', fontsize=labelsize)
# a.tick_params(axis='both', labelsize=labelsize)


for i in range(len(K_vec)):
    clr = colors[i]
    axs[1,1].plot(x[i], y_A[i] * n[i], markers[0], color=clr, lw=lw)
    axs[1,1].plot(x[i], y_C[i] * n[i], markers[1], color=clr, lw=lw)
axs[1,1].set_xscale('log')
axs[1,1].set_yscale('log')
axs[1,1].set_xlim(0,xlim)
axs[1,1].grid()
axs[1,1].set_xlabel('log(x) [-]', fontsize=labelsize)
axs[1,1].set_ylabel('log($n_\\alpha$) [-]', fontsize=labelsize)
axs[1,1].tick_params(axis='both', labelsize=labelsize)

[axs[1,0].plot(x[i], p[i], lw=lw, color=colors[i]) for i in range(len(K_vec))]
axs[1,0].set_yscale('log')
axs[1,0].set_xlim(0,xlim)
axs[1,0].set_ylim(1e-9, np.max(p))
axs[1,0].grid()
axs[1,0].set_xlabel('x [-]', fontsize=labelsize)
axs[1,0].set_ylabel('log($p$) [-]', fontsize=labelsize)
axs[1,0].tick_params(axis='both', labelsize=labelsize)


# order = [0, 5, 1, 6, 2, 7, 3, 4] 
# order = [0, 5, 1, 6, 2, 3, 4] 
order = [0, 5, 1, 4, 2, 3] 
lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
# lgnd = fig.legend([lines[i] for i in order], [labels[i] for i in order], bbox_to_anchor=(0.84,1.08), ncol=5, fontsize=labelsize)
lgnd = fig.legend([lines[i] for i in order], [labels[i] for i in order], bbox_to_anchor=(0.89,1.12), ncol=4, fontsize=labelsize)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)
fig.tight_layout()
fig.savefig('../Figures/Compressibility.svg', bbox_inches='tight')
fig.show()