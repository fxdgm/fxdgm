'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import numpy as np


# Load data
data = np.load('../Data/Solvation.npz')

x = data['x']
phi = data['phi']
y_A = data['y_A']
y_C = data['y_C']
y_S = data['y_S']
p = data['p']
Solvation_vec = data['Solvation_vec']

# Visualize the results
xlim = 0.15
fig, axs = plt.subplots(ncols=2, figsize=(30, 10))
labelsize = 40
lw = 4
legend_width = 6
markers = ['-', '-.', ':', '--']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

[axs[0].plot(x[i], phi[i], markers[i], color=colors[0], lw=lw) for i in range(len(Solvation_vec))]
axs[0].set_xlim(0,xlim)
axs[0].grid()
axs[0].set_xlabel('x [-]', fontsize=labelsize)
axs[0].set_ylabel('$\\varphi$ [-]', color=colors[0], fontsize=labelsize)
axs[0].tick_params(axis='y', labelcolor=colors[0], labelsize=labelsize)
axs[0].tick_params(axis='x', labelsize=labelsize)

axs1 = axs[0].twinx()
[axs1.plot(x[i], p[i], markers[i], color=colors[3], lw=lw) for i in range(len(Solvation_vec))]
axs1.set_xlim(0,xlim)
axs1.grid()
axs1.set_ylabel('$p$ [-]', color=colors[3], fontsize=labelsize)
axs1.tick_params(axis='y', labelcolor=colors[3], labelsize=labelsize)

[axs[1].plot(x[i], y_A[i], markers[i], color=colors[1], lw=lw) for i in range(len(Solvation_vec))]
[axs[1].plot(x[i], y_S[i], markers[i], color=colors[2], lw=lw) for i in range(len(Solvation_vec))]
axs[1].set_xlim(0,xlim)
axs[1].grid()
axs[1].set_xlabel('x [-]', fontsize=labelsize)
axs[1].set_ylabel('$y_A, y_S$ [-]', fontsize=labelsize)
axs[1].tick_params(axis='y', labelsize=labelsize)
axs[1].tick_params(axis='x', labelsize=labelsize)

axs2 = axs[1].twinx()
[axs2.plot(x[i], y_C[i], markers[i], color=colors[4], lw=lw) for i in range(len(Solvation_vec))]
axs2.set_xlim(0,xlim)
axs2.grid()
axs2.set_ylabel('$y_C$ [-]', color=colors[4], fontsize=labelsize)
axs2.tick_params(axis='y', labelcolor=colors[4], labelsize=labelsize)
axs2.grid()

# Adding legend entries with explicit line styles
for i in range(len(Solvation_vec)):
    axs[1].plot(0, 0, markers[i], color='grey', label=rf'$\kappa$ = {Solvation_vec[i]}', lw=lw)
axs[1].plot(0, 0, color=colors[1], label='$y_A$')
axs[1].plot(0, 0, color=colors[2], label='$y_S$')
axs[1].plot(0, 0, color=colors[4], label='$y_C$')

order = [0, 4, 1, 5, 2, 6, 3] 
lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
lgnd = fig.legend([lines[i] for i in order], [labels[i] for i in order], bbox_to_anchor=(0.775,1.22), ncol=4, fontsize=labelsize)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)
fig.tight_layout()
fig.show()
input("Press Enter to continue...")
