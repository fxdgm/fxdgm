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

# Further imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Define the parameters and boundary conditions
phi_left = 4.0
phi_right = 0.0
p_right = 0.0
y_A_R = 1/3
y_C_R = 1/3
z_A = -1.0
z_C = 1.0
K = 'incompressible'
Lambda2 = 8.553e-6
a2 = 7.5412e-4
number_cells = 1024#*4
refinement_style = 'log'
rtol = 1e-8

# solve the system
y_A, y_C, phi, p, x = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, relax_param=0.05, x0=0, x1=1, 
refinement_style='hard_log', return_type='Vector', max_iter=1_000, rtol=rtol)

# Fine point, where space charge starts to diverge from zero
index = 0
nF = z_C * y_C + z_A * y_A
for i, nF_ in enumerate(nF):
    if np.isclose(nF_, 0, atol=1e-3):
        index = i
        break


# Visualize the results
fig, axs = plt.subplots(ncols=2, figsize=(30,10))
labelsize = 30
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

fig.legend(lines, labels, bbox_to_anchor=(0.73,1.1), ncol=6, fontsize=labelsize)
fig.tight_layout()

fig.show()


# Save the data
np.savez('../Data/TernaryElectrolyte.npz', phi_left=phi_left, phi_right=phi_right, p_right=p_right, z_A=z_A, z_C=z_C, y_A_R=y_A_R, y_C_R=y_C_R, K=K, Lambda2=Lambda2, a2=a2, number_cells=number_cells, x=x, phi=phi, p=p, y_A=y_A, y_C=y_C, nF=nF, index=index)