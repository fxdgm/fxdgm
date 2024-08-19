'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import numpy as np

# Load data
df = np.load('../Data/TernaryElectrolyte.npz')

z_A = df['z_A']
z_C = df['z_C']
y_A = np.array(df['y_A'])
y_C = np.array(df['y_C'])
phi = np.array(df['phi'])
p = np.array(df['p'])
x = np.array(df['x'])
index = np.array(df['index'])
nF = np.array(df['nF'])

# Visualize the results
fig, axs = plt.subplots(ncols=2, figsize=(30,10))
labelsize = 40
lw = 4
ax1 = axs[0]
color = 'tab:blue'
ax1.set_xlabel('x [-]', fontsize=labelsize)
ax1.set_ylabel('$\\varphi$  [-]', color=color, fontsize=labelsize)
ax1.set_xlim(0,0.05)
ax1.plot(x, phi, color=color, lw=lw, label='$\\varphi$')
ax1.tick_params(axis='x', labelsize=labelsize)
ax1.tick_params(axis='y', labelcolor=color, labelsize=labelsize)

# Create a second y-axis
ax2 = ax1.twinx()

# Plot nF
color = 'tab:red'
ax2.set_ylabel('$p$ [-]', color=color, fontsize=labelsize)
ax2.plot(x, p, color=color, lw=lw, label='$p$')
ax2.set_xlim(0,0.05)
ax2.tick_params(axis='y', labelcolor=color, labelsize=labelsize)

# Add grid and save the figure
ax1.grid()
ax2.grid()

ax1 = axs[1]
# Plot y_alpha
color = 'tab:blue'
ax1.set_xlabel('x [-]', fontsize=labelsize)
ax1.set_ylabel('$y_\\alpha$  [-]', color=color, fontsize=labelsize)
ax1.plot(x, y_A, '--', color='tab:blue', lw=lw, label='$y_A$')
ax1.plot(x, y_C, '-', color='tab:blue', lw=lw, label='$y_C$')
ax1.plot(x, 1 - y_A - y_C, ':', color='tab:blue', lw=lw, label='$y_S$')
ax1.set_xlim(0,0.05)
ax1.axvline(x[index], color='green', lw=lw, linestyle='--')
ax1.tick_params(axis='x', labelsize=labelsize)
ax1.tick_params(axis='y', labelcolor=color, labelsize=labelsize)

# Create a second y-axis
ax2 = ax1.twinx()

# Plot nF
color = 'tab:red'
ax2.set_ylabel('$n^F$ [-]', color=color, fontsize=labelsize)
ax2.plot(x, z_A * y_A + z_C * y_C, '-.', color='tab:red', lw=lw, label='$n^F$')
ax2.set_xlim(0,0.05)
ax2.tick_params(axis='y', labelcolor=color, labelsize=labelsize)

# Add grid and save the figure
ax1.grid()
ax2.grid()
lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

fig.legend(lines, labels, bbox_to_anchor=(0.8,1.13), ncol=6, fontsize=labelsize)
fig.tight_layout()
fig.savefig('../Figures/TernaryElectrolyte.svg', bbox_inches='tight')
fig.show()