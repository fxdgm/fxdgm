'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

# import the needed functions from the fxdgm module
from fxdgm import solve_System_4eq

# Import plotting library
import matplotlib.pyplot as plt
import numpy as np

# Define Parameter and buondary conditions
phi_right = 0.0
p_right = 0.0
z_A, z_C = -1.0, 1.0
K = 'incompressible'
a2 = 7.5412e-4
nR_mol = 55
number_cells = 1024*4
refinement_style = 'hard_log'
rtol = 1e-8
max_iter = 10_000

Molarity = np.array([0.01, 0.1, 1.0]) # 10
y_A_L = Molarity / nR_mol

# Define left values of electric potential and values for lambda^2
phi_left = 16.0
Lambda2 = 8.553e-6
y_A, y_C, y_S, phi, p, x = [], [], [], [], [], []

# Solve the system for different values of phi_left
for y_alpha_L_ in y_A_L:
    y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_alpha_L_, y_alpha_L_, K, Lambda2, a2, number_cells, relax_param=0.05, x0=0, x1=1, refinement_style=refinement_style, return_type='Vector', max_iter=max_iter, rtol=rtol)
    y_A.append(y_A_)
    y_C.append(y_C_)
    y_S.append(1 - y_A_ - y_C_)
    phi.append(phi_)
    p.append(p_)
    x.append(x_)
    
# Visualize the results
fig, axs = plt.subplots(ncols=3, figsize=(10, 5))
xlim = 0.1
markers = ['--', '-', ':']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

for i in range(len(Molarity)):
    clr = colors[i]
    axs[0].plot(x[i], y_A[i], color=clr)#, lw=lw)
    axs[1].plot(x[i], y_C[i], color=clr)#, lw=lw)
    axs[2].plot(x[i], y_S[i], color=clr)#, lw=lw)
[axs[i].grid() for i in range(3)]
[axs[i].set_xlim(0,xlim) for i in range(3)]
axs[0].set_ylim(0, 1)
axs[1].set_ylim(0, np.max(y_C))
axs[2].set_ylim(0, 1)
[axs[i].set_xlabel('$x$ [-]') for i in range(3)]#, fontsize=labelsize)
# axs.set_ylabel('$y_\\alpha$ [-]')#, fontsize=labelsize)
axs[0].set_ylabel('$y_A$ [-]')#, fontsize=labelsize)
axs[1].set_ylabel('$y_C$ [-]')#, fontsize=labelsize)
axs[2].set_ylabel('$y_S$ [-]')#, fontsize=labelsize)
# axs.tick_params(axis='both')#, labelsize=labelsize)

# dummy, = axs.plot(2, 0, color='grey', linestyle='--', label='$y_A$')
# dummy, = axs.plot(2, 2, color='grey', linestyle='-', label='$y_C$')
# dummy, = axs.plot(2, 2, color='grey', linestyle=':', label='$y_S$')
for i in range(len(Molarity)):
    dummy, = axs[0].plot(2, 0, color=colors[i], linestyle='-', label=f'$M$: {Molarity[i]}')

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

# Finally, the legend (that maybe you'll customize differently)
lgnd = fig.legend(lines, labels, bbox_to_anchor=(0.7,1.05), ncol=4)
fig.tight_layout()
fig.savefig('../../Figures/ParameterAnalysis/Molarity.svg', bbox_inches='tight')
fig.show()

# Save the Results
np.savez('../../Data/ParameterAnalysis/Molarity.npz', phi_right=phi_right, p_right = p_right, y_alpha_L = y_alpha_L_, z_A = z_A, z_C = z_C, number_cells=number_cells, a2=a2, phi_left=phi_left, Lambda2=Lambda2, x=x, phi=phi, y_A=y_A, y_C=y_C, y_S=y_S, p=p)