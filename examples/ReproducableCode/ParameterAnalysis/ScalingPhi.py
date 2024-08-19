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
Lambda2 = 8.553e-6
a2 = 7.5412e-4
number_cells = 1024*4
refinement_style = 'hard_log'
rtol = 1e-8
max_iter = 10_000

phi_left_vector = [1,2,4,8]

phi, x = [], []
# Solve the system for different values of phi_left
for phi_L in phi_left_vector:
    y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_L, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, relax_param=0.05, x0=0, x1=1, refinement_style=refinement_style, return_type='Vector', rtol=rtol, max_iter=max_iter)
    phi.append(phi_)
    x.append(x_)
    
# Normalize the electric potentials
phi_scaled = []
for i, phi_L in enumerate(phi_left_vector):
    phi_scaled.append(phi[i]/phi_L)
    
# Visualize the results
# Non-normalized electric potential
for i, phi_L in enumerate(phi_left_vector):
    plt.plot(x[i], phi[i], label='$\delta \\varphi$ = ' + str(phi_L))
plt.legend()
plt.xlabel('$x$ [-]')
plt.ylabel('$\\varphi$ [-]')
plt.ylim(0, max(phi_left_vector) + 0.1)
plt.xlim(0,0.05)
plt.grid()
plt.tight_layout()
plt.show()

# Normalized electric potential
for i, phi_L in enumerate(phi_left_vector):
    plt.plot(x[i], phi_scaled[i], label='$\delta \\varphi$ = ' + str(phi_L))
plt.legend()
plt.xlabel('$x$ [-]')
plt.ylabel('$\\varphi/\delta \\varphi$ [-]')
plt.ylim(0, 1.05)
plt.xlim(0,0.05)
plt.grid()
plt.tight_layout()
plt.show()

# Save the results
np.savez('../../Data/ParameterAnalysis/ScalingPhi.npz', phi_right=phi_right, p_right=p_right, y_A_R=y_A_R, y_C_R=y_C_R, z_A=z_A, z_C=z_C, K=K, Lambda2=Lambda2, a2=a2, number_cells=number_cells, refinement_style=refinement_style, rtol=rtol, max_iter=max_iter, phi_left_vector=phi_left_vector, phi=phi, x=x, phi_scaled=phi_scaled)