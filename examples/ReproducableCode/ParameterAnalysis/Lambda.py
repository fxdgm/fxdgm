'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''
# import the src file needed to solve the system of equations
import sys
import os


# Add the src directory to the sys.path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..', 'src')
sys.path.insert(0, src_path)

from Eq04 import solve_System_4eq

# Remove the src directory from sys.path after import
del sys.path[0]

# Import plotting library
import matplotlib.pyplot as plt
import numpy as np

# Define Parameter and buondary conditions
phi_right = 0.0
p_right = 0.0
y_A_R, y_C_R = 1/3, 1/3
z_A, z_C = -1.0, 1.0
K = 'incompressible'
a2 = 7.5412e-4
number_cells = 1024*4
refinement_style = 'hard_log'
rtol = 1e-8
max_iter = 10_000

# Define left values of electric potential and values for lambda^2
phi_left_vec = [-1.0, 1.0, 4.0, 8.0]
Lambda2_vec = [8.553e-5, 8.553e-6, 8.553e-7]
y_A, y_C, y_S, phi, p, x = [], [], [], [], [], []

# Solve the system for different values of phi_left
for phi_left_ in phi_left_vec:
    y_A_bcs, y_C_bcs, y_S_bcs, phi_bcs, p_bcs, x_bcs = [], [], [], [], [], []
    for l2 in Lambda2_vec:
        y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_left_, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, l2, a2, number_cells, relax_param=0.05, x0=0, x1=1, refinement_style=refinement_style, return_type='Vector', max_iter=max_iter, rtol=rtol)
        y_A_bcs.append(y_A_)
        y_C_bcs.append(y_C_)
        y_S_bcs.append(1 - y_A_ - y_C_)
        phi_bcs.append(phi_)
        p_bcs.append(p_)
        x_bcs.append(x_)
    y_A.append(y_A_bcs)
    y_C.append(y_C_bcs)
    y_S.append(y_S_bcs)
    phi.append(phi_bcs)
    p.append(p_bcs)
    x.append(x_bcs)
    
# Visualize the results
fig, axs = plt.subplots(2, 2)
xlim = 0.08
markers = ['--', '-', ':']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
for i in range(len(phi_left_vec)):
    # Plot phi

    match i:
        case 0: 
            i_ = 0
            j_ = 0
        case 1: 
            i_ = 0
            j_ = 1
        case 2: 
            i_ = 1
            j_ = 0
        case 3: 
            i_ = 1
            j_ = 1
    axs[i_,j_].set_title(f'$\delta \\varphi$ = {phi_left_vec[i]}')#, fontsize=labelsize)
    for j in range(len(Lambda2_vec)):
        clr = colors[j]
        axs[i_,j_].plot(x[i][j], y_A[i][j], markers[0], color=clr)#, lw=lw)
        axs[i_,j_].plot(x[i][j], y_C[i][j], markers[1], color=clr)#, lw=lw)
        axs[i_,j_].plot(x[i][j], y_S[i][j], markers[2], color=clr)#, lw=lw)
    axs[i_,j_].grid()
    axs[i_,j_].set_xlim(0,xlim)
    axs[i_,j_].set_xlabel('$x$ [-]')#, fontsize=labelsize)
    axs[i_,j_].set_ylabel('$y_\\alpha$ [-]')#, fontsize=labelsize)
    axs[i_,j_].tick_params(axis='both')#, labelsize=labelsize)

dummy, = axs[i_,j_].plot(2, y_A_R, color='grey', linestyle='--', label='$y_A$')
dummy, = axs[i_,j_].plot(2, y_A_R, color='grey', linestyle='-', label='$y_C$')
dummy, = axs[i_,j_].plot(2, y_A_R, color='grey', linestyle=':', label='$y_S$')
for index, Lambda2_cur in enumerate(Lambda2_vec):
    dummy, = axs[i_,j_].plot(10, y_A_R, color=colors[index], linestyle='-', label=f'$\lambda^2$ = {Lambda2_cur}')

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

# Finally, the legend (that maybe you'll customize differently)
lgnd = fig.legend(lines, labels, bbox_to_anchor=(0.88,1.15), ncol=3)
fig.tight_layout()
fig.show()

# Save the Results
np.savez('../../Data/ParameterAnalysis/Lambda.npz', phi_right=phi_right, p_right = p_right, y_A_R = y_A_R, y_C_R=y_C_R, z_A = z_A, z_C = z_C, number_cells=number_cells, a2=a2, phi_left_vec=phi_left_vec, Lambda2_vec=Lambda2_vec, x=x, phi=phi, y_A=y_A, y_C=y_C, y_S=y_S, p=p)