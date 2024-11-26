'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

# import the needed functions from the fxdgm module
from fxdgm import solve_System_2eq

# Import plotting library
import matplotlib.pyplot as plt
import numpy as np

# Define Parameter and boundary conditions
phi_right = 0.0
p_right = 0.0
y_A_R, y_C_R = 1/3, 1/3
z_A, z_C = -1.0, 1.0
K = 'incompressible'
Lambda2 = 8.553e-6
a2 = 7.5412e-4
number_cells = 1024*4
refinement_style = 'hard_log'
rtol = 1e-8
max_iter = 10_000
relax_param = 0.05

phi_left_vec = np.linspace(-10, 10, 201)
y_A, y_C, y_S, phi, p, x = [], [], [], [], [], []
for phi_left_ in phi_left_vec:
    y_A_, y_C_, phi_, p_, x_ = solve_System_2eq(phi_left_, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, relax_param=relax_param, refinement_style=refinement_style, return_type='Vector', max_iter=max_iter, rtol=rtol)
    y_S_ = 1 - y_A_ - y_C_
    y_A.append(y_A_)
    y_C.append(y_C_)
    y_S.append(y_S_)
    phi.append(phi_)
    p.append(p_)
    x.append(x_)
        
# Save the data
np.savez('../../Data/ParameterAnalysis/FractionsHeightLeft.npz', phi_right=phi_right, p_right = p_right, y_A_R = y_A_R, y_C_R=y_C_R, z_A = z_A, z_C = z_C, number_cells=number_cells, a2=a2, phi_left_vec=phi_left_vec, Lambda2=Lambda2, x=x, phi=phi, y_A=y_A, y_C=y_C, y_S=y_S, p=p)
    
# Visualizations
y_A_np, y_C_np, y_S_np = np.array(y_A), np.array(y_C), np.array(y_S)
fig, axs = plt.subplots()
axs.plot(phi_left_vec, y_A_np[:,0], label='$y_A$')
axs.plot(phi_left_vec, y_C_np[:,0], label='$y_C$')
axs.plot(phi_left_vec, y_S_np[:,0], label='$y_S$')
axs.grid()
axs.set_xlabel('$\delta \\varphi$ [-]')
axs.set_ylabel('$y_\\alpha$ [-]')
axs.legend()
fig.tight_layout()
fig.show()
