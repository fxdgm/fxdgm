'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

# import the src file needed to solve the system of equations
import sys
import os

# Add the src directory to the sys.path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'src')
sys.path.insert(0, src_path)

from Eq04 import solve_System_4eq

# Remove the src directory from sys.path after import
del sys.path[0]

import matplotlib.pyplot as plt
import numpy as np

# Parameter and solver settings
phi_R = 0.0
p_R = 0.0
y_A_R, y_C_R = 1/3, 1/3
K = 'incompressible'
Lambda2 = 8.553e-6
a2 = 7.5412e-4
number_cells = 1024
refinement_style = 'hard_log'
z_A, z_C = -1.0, 1.0
relax_param = 0.05

xlim = 0.025
DeltaPhi = np.linspace(0,5,6)

# Solve DGM 
y_A_Dreyer, x_Dreyer = [], []
for phi_L in DeltaPhi:
    y_A, y_C, phi, p, x = solve_System_4eq(phi_L, phi_R, p_R, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, relax_param=relax_param, return_type='Vector', refinement_style=refinement_style, max_iter=1_000)
    y_A_Dreyer.append(y_A)
    x_Dreyer.append(x)

# Solve Nernst-Planck
y_A_NP, x_NP = [], []
for phi_L in DeltaPhi:
    y_A, y_C, phi, p, x = solve_System_4eq(phi_L, phi_R, p_R, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, relax_param, return_type='Vector', PoissonBoltzmann=True, refinement_style=refinement_style)
    y_A_NP.append(y_A)
    x_NP.append(x)


# Plotting
labelsize = 30
lw = 4
legend_width = 8

# Nernst-Planck
fig, axs = plt.subplots(figsize=(15,20))
[axs.plot(x_NP[i], y_A_NP[i], lw=lw*2, label=f'$\delta \\varphi = {DeltaPhi[i]}$') for i in range(len(DeltaPhi))]
axs.set_xlim(0,xlim)
axs.set_ylim(10e-2, 1e+2)
axs.set_yscale('log')
axs.grid()
axs.set_xlabel('x [-]', fontsize=labelsize*2)
axs.set_ylabel('$y_A$ [-]', fontsize=labelsize*2)
axs.tick_params(axis='both', labelsize=labelsize*2)

lgnd = fig.legend(bbox_to_anchor=(0.97, 0.97), fontsize=labelsize, ncol=3)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)

fig.tight_layout()
fig.savefig('../Figures/Shortcomings_NP_NP.svg', bbox_inches='tight')
fig.show()


# DGM
fig, axs = plt.subplots(figsize=(15,10))
[axs.plot(x_Dreyer[i], y_A_Dreyer[i], lw=lw*2, label=f'$\delta \\varphi = {DeltaPhi[i]}$') for i in range(len(DeltaPhi))]
axs.set_xlim(0,xlim)
axs.set_ylim(10e-2, 1.05)
axs.set_yscale('log')
axs.grid()
axs.set_xlabel('x [-]', fontsize=labelsize*2)
axs.set_ylabel('$y_A$ [-]', fontsize=labelsize*2)
axs.tick_params(axis='both', labelsize=labelsize*2)

lgnd = fig.legend(bbox_to_anchor=(0.97, 1.16), fontsize=labelsize, ncol=3)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)

fig.tight_layout()
fig.savefig('../Figures/Shortcomings_NP_DGM.svg', bbox_inches='tight')
fig.show()