'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

# import the src file needed to solve the system of equations
import sys
import os

# Add the src directory to the sys.path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')
sys.path.insert(0, src_path)

from Eq04 import solve_System_4eq

# Remove the src directory from sys.path after import
del sys.path[0]

# Further imports
import matplotlib.pyplot as plt
import numpy as np

# Define the parameters and boundary conditions
phi_left = 6.0
phi_right = 0.0
p_right = 0.0
y_A_L, y_C_L = 1/3, 1/3
z_A, z_C = -1.0, 1.0
number_cells = 1024*8
K_vec = ['incompressible', 15_000, 5_000, 1_500, 500]
Lambda2 = 8.553e-6
a2 = 7.5412e-4
refinement_style = 'hard_hard_log'
rtol = 1e-7

relax_param = 0.08
max_iter = 10_000

# Calculate the total number density, based on the pressure
def n_expr(p, K):
    if K == 'incompressible':
        return np.ones_like(p)
    return (p-1) / K + 1  

# Solve the system
y_A, y_C, y_S, phi, p, n, x = [], [], [], [], [], [], []
for K in K_vec:
    y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_L, y_C_L, K, Lambda2, a2, number_cells, relax_param = relax_param, max_iter=max_iter, refinement_style=refinement_style, return_type='Vector', rtol=rtol)
    y_A.append(y_A_)
    y_C.append(y_C_)
    y_S.append(1 - y_A_ - y_C_)
    phi.append(phi_)
    p.append(p_)
    n.append(n_expr(p_, K))
    x.append(x_)
    

# Plot the results
fig, axs = plt.subplots(2, 2, figsize=(30, 20))
# Define plotting parameter
labelsize = 30
lw = 4
legend_width = 8
xlim = 0.05
markers = ['-.', '--', '-', ':']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

# Legend for compressibility scaling
axs[0,0].plot(0, 0, label='Incompressible', color=colors[0])
[axs[0,0].plot(0, 0, label=f'$\kappa$ = {K_vec[i]}', color=colors[i]) for i in range(1, len(K_vec))]

# Electric potential
[axs[0,0].plot(x[i], phi[i], lw=lw, color=colors[i]) for i in range(len(K_vec))]
axs[0,0].set_xlim(0,xlim)
axs[0,0].grid()
axs[0,0].set_xlabel('x [-]', fontsize=labelsize)
axs[0,0].set_ylabel('$\\varphi$ [-]', fontsize=labelsize)
axs[0,0].tick_params(axis='both', labelsize=labelsize)

# Concentrations
for i in range(len(K_vec)):
    clr = colors[i]
    axs[0,1].plot(x[i], y_A[i], markers[0], color=clr, lw=lw)
    axs[0,1].plot(x[i], y_C[i], markers[1], color=clr, lw=lw)
axs[0,1].plot(0, 0.1, color='grey', linestyle='--', label='Anions')
axs[0,1].plot(0, 0.1, color='grey', linestyle=':', label='Cations')
axs[0,1].set_xlim(0,xlim)
axs[0,1].grid()
axs[0,1].set_xlabel('x [-]', fontsize=labelsize)
axs[0,1].set_ylabel('$y_\\alpha$ [-]', fontsize=labelsize)
axs[0,1].tick_params(axis='both', labelsize=labelsize)

a = plt.axes([.75, .77, .2, .2])
for i in range(len(K_vec)):
    clr = colors[i]
    a.plot(x[i], y_S[i], markers[0], color=clr, lw=lw)
axs[0,1].plot(0, 0.1, color='grey', linestyle='--', label='Solvent')
a.set_xlim(0,xlim)
a.grid()
a.set_xlabel('$\delta \\varphi$ [-]', fontsize=labelsize)
a.set_ylabel('$y_S$ [-]', fontsize=labelsize)
a.tick_params(axis='both', labelsize=labelsize)

# Number densities
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

# Pressure
[axs[1,0].plot(x[i], p[i], lw=lw, color=colors[i]) for i in range(len(K_vec))]
axs[1,0].set_yscale('log')
axs[1,0].set_xlim(0,xlim)
axs[1,0].set_ylim(1e-9, np.max(p))
axs[1,0].grid()
axs[1,0].set_xlabel('x [-]', fontsize=labelsize)
axs[1,0].set_ylabel('log($p$) [-]', fontsize=labelsize)
axs[1,0].tick_params(axis='both', labelsize=labelsize)


lgnd = fig.legend(bbox_to_anchor=(0.98, 1.05), fontsize=labelsize, ncol=7, markerscale=60)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)
fig.tight_layout()
fig.show()