'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to validate the simplification of the system of four equations to a system of two equations in the one-dimensional equilibrium case.
'''

# import the src file needed to solve the system of equations
import sys
import os

# Add the src directory to the sys.path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'src')
sys.path.insert(0, src_path)

from Eq04 import solve_System_4eq
from Eq02 import solve_System_2eq

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
y_A_R = 0.01
y_C_R = 0.01
z_A = -1.0
z_C = 1.0
K = 'incompressible'
Lambda2 = 8.553e-6
a2 = 7.5412e-4
solvation = 15
number_cells = 1024#*4
refinement_style = 'log'
rtol = 1e-8

# solve the complete system
y_A_4eq, y_C_4eq, phi_4eq, p_4eq, x_4eq = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation, relax_param=0.05, refinement_style='hard_log', return_type='Vector', max_iter=1_000, rtol=rtol)

# solve the simplified system
y_A_2eq, y_C_2eq, phi_2eq, p_2eq, x_2eq = solve_System_2eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation, relax_param=0.05, refinement_style='hard_log', return_type='Vector', max_iter=1_000, rtol=rtol)

# Evaluate the difference
plt.figure()
# plt.plot(x_4eq, y_A_4eq, label='y_A_4eq')
# plt.plot(x_2eq, y_A_2eq, label='y_A_2eq')
plt.plot(x_4eq, y_A_4eq - y_A_2eq, label='y_A_4eq - y_A_2eq')
plt.grid()
plt.xlim(0, 0.05)
plt.legend()
plt.show()

plt.figure()
# plt.plot(x_4eq, y_C_4eq, label='y_C_4eq')
# plt.plot(x_2eq, y_C_2eq, label='y_C_2eq')
plt.plot(x_4eq, y_C_4eq - y_C_2eq, label='y_C_4eq - y_C_2eq')
plt.grid()
plt.xlim(0, 0.05)
plt.legend()
plt.show()

plt.figure()
# plt.plot(x_4eq, phi_4eq, label='phi_4eq')
# plt.plot(x_2eq, phi_2eq, label='phi_2eq')
plt.plot(x_4eq, phi_4eq - phi_2eq, label='phi_4eq - phi_2eq')
plt.grid()
plt.xlim(0, 0.05)
plt.legend()
plt.show()

plt.figure()
# plt.plot(x_4eq, p_4eq, label='p_4eq')
# plt.plot(x_2eq, p_2eq, label='p_2eq')
plt.plot(x_4eq, p_4eq - p_2eq, label='p_4eq - p_2eq')
plt.grid()
plt.xlim(0, 0.05)
plt.legend()
plt.show()