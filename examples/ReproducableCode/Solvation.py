'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to analyze the solvation effect of an incomressible, ternary electrolyte.
'''

# import the needed functions from the fxdgm module
from fxdgm import solve_System_4eq

# Further imports
import matplotlib.pyplot as plt
import numpy as np

# Define the parameters and boundary conditions
phi_left = 10.0
phi_right = 0.0
p_right = 0.0
y_A_R, y_C_R = 0.01, 0.01
z_A, z_C = -1.0, 1.0
number_cells = 1024
K = 'incompressible'
Lambda2 = 8.553e-6
a2 = 7.5412e-4
Solvation_vec = [0, 5, 10, 15]
refinement_style = 'hard_log'
relax_param=0.05
rtol = 1e-8
xlim = 0.1

# Solve the system
y_A, y_C, y_S, phi, p, x = [], [], [], [], [], []
for solvation_ in Solvation_vec:
    y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation_, relax_param=relax_param, refinement_style=refinement_style, return_type='Vector', rtol=rtol)
    y_A.append(y_A_)
    y_C.append(y_C_)
    y_S.append(1 - y_A_ - y_C_)
    phi.append(phi_)
    p.append(p_)
    x.append(x_)
    
# Visualize the results
fig, axs = plt.subplots(ncols=2, figsize=(10,5))
markers = ['-', '-.', ':', '--']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

# Electric potential
[axs[0].plot(x[i], phi[i], markers[i], color=colors[0]) for i in range(len(Solvation_vec))]
axs[0].set_xlim(0,xlim)
axs[0].grid()
axs[0].set_xlabel('x [-]')
axs[0].set_ylabel('$\\varphi$ [-]', color=colors[0])
axs[0].tick_params(axis='y', labelcolor=colors[0])
axs[0].tick_params(axis='x')

# Pressure
axs1 = axs[0].twinx()
[axs1.plot(x[i], p[i], markers[i], color=colors[3]) for i in range(len(Solvation_vec))]
axs1.set_xlim(0,xlim)
axs1.grid()
axs1.set_ylabel('$p$ [-]', color=colors[3])
axs1.tick_params(axis='y', labelcolor=colors[3])

# Concentrations for A and S
[axs[1].plot(x[i], y_A[i], markers[i], color=colors[1]) for i in range(len(Solvation_vec))]
[axs[1].plot(x[i], y_S[i], markers[i], color=colors[2]) for i in range(len(Solvation_vec))]
axs[1].set_xlim(0,xlim)
axs[1].grid()
axs[1].set_xlabel('x [-]')
axs[1].set_ylabel('$y_A, y_S$ [-]')
axs[1].tick_params(axis='y')
axs[1].tick_params(axis='x')

# Concentration for C
axs2 = axs[1].twinx()
[axs2.plot(x[i], y_C[i], markers[i], color=colors[4]) for i in range(len(Solvation_vec))]
axs2.set_xlim(0,xlim)
axs2.grid()
axs2.set_ylabel('$y_C$ [-]', color=colors[4])
axs2.tick_params(axis='y', labelcolor=colors[4])
axs2.grid()

# Add legend
[axs[1].plot(0, 0, markers[i], color='grey', label=f'$\kappa$ = {Solvation_vec[i]}') for i in range(len(Solvation_vec))]
axs[1].plot(0, 0, color=colors[1], label='$y_A$')
axs[1].plot(0, 0, color=colors[2], label='$y_S$')

lgnd = fig.legend(bbox_to_anchor=(0.785, 1.1), ncol=6)
fig.tight_layout()
fig.show()



# Save the data
np.savez('../Data/Solvation.npz', phi_left=phi_left, phi_right=phi_right, p_right=p_right, y_A_R=y_A_R, y_C_R=y_C_R, z_A=z_A, z_C=z_C, number_cells=number_cells, a2=a2, Solvation_vec=Solvation_vec, Lambda2=Lambda2, x=x, phi=phi, p=p, y_A=y_A, y_C=y_C, y_S=y_S)