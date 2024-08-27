'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Load data
df = np.load('../Data/Validation_Dreyer_BulkSurface.npz')

x = df['x_dim']
n_A = df['n_A_dim']
n_C = df['n_C_dim']
phi = df['phi_dim']
p = df['p_dim']

# Plotting

# Options
markers = ['-', '-.', ':', '--']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
labelsize = 15
lw = 2
legend_width = 3

scale_x = 1e-9
ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))

# Figure
fig, axs = plt.subplots(ncols=2, figsize=(13,5))
axs[0].plot(x[0], n_A[0], markers[0], color=colors[0], lw=lw, label='Poisson-Boltzmann')
axs[0].plot(x[1], n_A[1], markers[1], color=colors[1], lw=lw, label=f'ideal mixture, $\kappa = 0$')
axs[0].plot(x[2], n_A[2], markers[2], color=colors[2], lw=lw, label=f'solvated ions, $\kappa = 8$')
axs[0].grid()
axs[0].xaxis.set_major_formatter(ticks_x)
axs[0].set_xlim(0, 2.5*scale_x)
axs[0].set_ylim(0, 60)
axs[0].set_xlabel('x [nm]', fontsize=labelsize)
axs[0].set_ylabel('$n_A$ [mol/m$^3$]', fontsize=labelsize)

a = plt.axes([.17, .4, .29, .5])
a.plot(x[0], n_C[0], markers[0], color=colors[0], lw=lw)
a.plot(x[1], n_C[1], markers[1], color=colors[1], lw=lw)
a.plot(x[2], n_C[2], markers[2], color=colors[2], lw=lw)
a.grid()
a.xaxis.set_major_formatter(ticks_x)
a.set_xlim(0, 4.5*scale_x)
a.set_xlabel('x [nm]', fontsize=labelsize)
a.set_ylabel('$n_C$ [mol/m$^3$]', fontsize=labelsize)



axs[1].plot(x[0], phi[0], markers[0], color=colors[0], lw=lw)
axs[1].plot(x[1], phi[1], markers[1], color=colors[1], lw=lw)
axs[1].plot(x[2], phi[2], markers[2], color=colors[2], lw=lw)
axs[1].grid()
axs[1].xaxis.set_major_formatter(ticks_x)
axs[1].set_xlim(0, 2.5*scale_x)
axs[1].set_xlabel('x [nm]', fontsize=labelsize)
axs[1].set_ylabel('$\\varphi [V]$', fontsize=labelsize)

a = plt.axes([.18+.5, .4, .29, .5])
a.plot(x[0], p[0]*1e-6, markers[0], color=colors[0], lw=lw)
a.plot(x[1], p[1]*1e-6, markers[1], color=colors[1], lw=lw)
a.plot(x[2], p[2]*1e-6, markers[2], color=colors[2], lw=lw)
a.grid()
a.xaxis.set_major_formatter(ticks_x)
a.set_xlim(0, 0.9*scale_x)
a.set_ylim(0, 2_700)
a.set_xlabel('x [nm]', fontsize=labelsize)
a.set_ylabel('$p [MPa]$', fontsize=labelsize)

lgnd = fig.legend(bbox_to_anchor=(0.85, 1.1), fontsize=labelsize, ncol=6)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)

fig.tight_layout()
fig.savefig('../Figures/Validation_Dreyer_BulkSurface.svg', bbox_inches='tight')
fig.show()