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
phi_left = 4.0
phi_right = 0.0
p_right = 0.0
y_A_R_1, y_C_R_1 = 1/6, 2/6
y_A_R_2, y_C_R_2 = 2/6, 1/6
z_A_1, z_C_1 = -2.0, 1.0
z_A_2, z_C_2 = -1.0, 2.0
K = 'incompressible'
a2 = 7.5412e-4
number_cells = 1024*8
refinement_style = 'hard_log'
rtol = 1e-8
max_iter = 10_000

# Define left values of electric potential and values for lambda^2
Lambda2 = 8.553e-6

# Solve the system
y_A_1, y_C_1, phi_1, p_1, x_1 = solve_System_4eq(phi_left, phi_right, p_right, z_A_1, z_C_2, y_A_R_1, y_C_R_1, K, Lambda2, a2, number_cells, relax_param=0.05, x0=0, x1=1, refinement_style=refinement_style, return_type='Vector', max_iter=max_iter, rtol=rtol)

y_A_2, y_C_2, phi_2, p_2, x_2 = solve_System_4eq(phi_left, phi_right, p_right, z_A_2, z_C_2, y_A_R_2, y_C_R_2, K, Lambda2, a2, number_cells, relax_param=0.05, x0=0, x1=1, refinement_style=refinement_style, return_type='Vector', max_iter=max_iter, rtol=rtol)


# Visualize the results
plt.figure()
plt.plot(x_1, phi_1, label='z_A = -2, z_C = 1')
plt.plot(x_2, phi_2, label='z_A = -1, z_C = 2')
plt.legend()
plt.xlabel('x')
plt.ylabel('$\\varphi$')
plt.grid()
plt.show()

plt.figure()
plt.plot(x_1, y_A_1, label='z_A = -2, z_C = 1')
plt.plot(x_2, y_A_2, label='z_A = -1, z_C = 2')
plt.legend()
plt.xlabel('x')
plt.ylabel('$y_A$')
plt.grid()
plt.show()

plt.figure()
plt.plot(x_1, y_C_1, label='z_A = -2, z_C = 1')
plt.plot(x_2, y_C_2, label='z_A = -1, z_C = 2')
plt.legend()
plt.xlabel('x')
plt.ylabel('$y_C$')
plt.grid()
plt.show()

plt.figure()
plt.plot(x_1, p_1, label='z_A = -2, z_C = 1')
plt.plot(x_2, p_2, label='z_A = -1, z_C = 2')
plt.legend()
plt.xlabel('x')
plt.ylabel('p')
plt.grid()
plt.show()

