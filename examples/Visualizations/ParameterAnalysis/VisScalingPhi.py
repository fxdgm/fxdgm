'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import numpy as np

# Load data
df = np.load('../../Data/ParameterAnalysis/ScalingPhi.npz')

phi_left_vector = df['phi_left_vector']
phi = np.array(df['phi'])
phi_scaled = np.array(df['phi_scaled'])
x = np.array(df['x'])

# Normalize the electric potentials
fig, axs = plt.subplots(1, 2, figsize=(30,10))
labelsize = 40
lw = 4
legend_width = 8
xlim = 0.08

for i, phi_L in enumerate(phi_left_vector):
    axs[0].plot(x[i], phi[i], lw=lw, label='$\delta \\varphi$ = ' + str(phi_L))
# axs[0].legend()
axs[0].set_xlabel('$x$ [-]', fontsize=labelsize)
axs[0].set_ylabel('$\\varphi$ [-]', fontsize=labelsize)
axs[0].set_ylim(0, max(phi_left_vector) + 0.1)
axs[0].set_xlim(0,xlim)
axs[0].tick_params(axis='both', labelsize=labelsize)
axs[0].grid()

for i, phi_L in enumerate(phi_left_vector):
    axs[1].plot(x[i], phi_scaled[i], lw=lw)
axs[1].legend()
axs[1].set_xlabel('$x$ [-]', fontsize=labelsize)
axs[1].set_ylabel('$\\varphi/\delta \\varphi$ [-]', fontsize=labelsize)
axs[1].set_ylim(0, 1.05)
axs[1].set_xlim(0,xlim)
axs[1].grid()
axs[1].tick_params(axis='both', labelsize=labelsize)

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

# Finally, the legend (that maybe you'll customize differently)
lgnd = fig.legend(lines, labels, bbox_to_anchor=(0.805,1.12), ncol=4, fontsize=labelsize)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)
fig.tight_layout()

fig.savefig('../../Figures/Parameteranalysis/ScalingPhi.svg', bbox_inches='tight')
fig.show()