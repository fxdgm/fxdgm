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

# Import plotting library
import matplotlib.pyplot as plt
import numpy as np

# Define Parameter and buondary conditions
phi_right = 0.0
p_right = 0.0
y_A_R, y_C_R = 1/3, 1/3
z_A, z_C = -1.0, 1.0
K = 'incompressible'
Lambda2 = 8.553e-6
number_cells = 1024*4
refinement_style = 'hard_log'
rtol = 1e-8
max_iter = 10_000

phi_left_vec = [0.1, 1.0, 4.0, 8.0]
a2_vec = [7.5412e-3, 7.5412e-4, 7.5412e-5]
y_A, y_C, y_S, phi, p, x = [], [], [], [], [], []
for phi_left_ in phi_left_vec:
    y_A_bcs, y_C_bcs, y_S_bcs, phi_bcs, p_bcs, x_bcs = [], [], [], [], [], []
    for a2 in a2_vec:
        y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_left_, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, relax_param=0.05, x0=0, x1=1, refinement_style=refinement_style, return_type='Vector', max_iter=max_iter, rtol=rtol)
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

p = np.array(p)

plt.figure()
for j in range(len(a2_vec)):
    plt.plot(x[-1][j], p[-1][j], label='$a^2$ = {}'.format(a2_vec[j]))
plt.grid()
plt.ylim(0.0, np.max(p[-1][0]))
plt.xlim(0,0.08)
plt.xlabel('$x$ [-]')
plt.ylabel('$p$ [-]')
plt.tick_params(axis='both')
plt.legend(loc='best')
plt.tight_layout()
plt.show()