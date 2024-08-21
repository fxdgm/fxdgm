'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import numpy as np

# Load data
df = np.load('../../Data/ParameterAnalysis/FractionsHeightLeft.npz')

phi_left_vec = df['phi_left_vec']
y_A = df['y_A']
y_C = df['y_C']
y_S = df['y_S']

# Visualize the results
labelsize = 30
lw = 4
legend_width = 8

y_A_np, y_C_np, y_S_np = np.array(y_A), np.array(y_C), np.array(y_S)
fig, axs = plt.subplots(figsize=(15, 10))
axs.plot(phi_left_vec, y_A_np[:,0], label='$y_A$', lw=lw)
axs.plot(phi_left_vec, y_C_np[:,0], label='$y_C$', lw=lw)
axs.plot(phi_left_vec, y_S_np[:,0], label='$y_S$', lw=lw)
axs.grid()
axs.set_xlabel('$\delta \\varphi$ [-]', fontsize=labelsize)
axs.set_ylabel('$y_\\alpha^L$ [-]', fontsize=labelsize)
axs.tick_params(axis='both', labelsize=labelsize)

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

# Finally, the legend (that maybe you'll customize differently)
lgnd = fig.legend(lines, labels, bbox_to_anchor=(0.75,1.1), ncol=6, fontsize=labelsize)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)
fig.tight_layout()
fig.savefig('../../Figures/ParameterAnalysis/FractionsHeightLeft.svg', bbox_inches='tight')
fig.show()