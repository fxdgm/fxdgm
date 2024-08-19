'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to compare the convergence of the DGM model 
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
from scipy.interpolate import interp1d

# Define the parameters and boundary conditions
z_A, z_C = -1.0, 1.0
y_A_right, y_C_right = 1/3, 1/3
phi_left = 6.0
phi_right = 0.0
p_right = 0.0
Lambda2 = 8.553e-6
a2 = 7.5412e-4
K = 'incompressible'
rtol = 1e-8

# Define grid-sizes
number_cells_vec = [10, 100, 1_000, 10_000, 100_000, 1_000_000]
refinement_style = 'uniform'

y_A, y_C, y_S, phi, p, x = [], [], [], [], [], []
for number_cells in number_cells_vec:
    y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_right, y_C_right, K, Lambda2, a2, number_cells, refinement_style=refinement_style, rtol=rtol, max_iter=1000, return_type='Vector')
    y_A.append(y_A_)
    y_C.append(y_C_)
    y_S.append(1 - y_A_ - y_C_)
    phi.append(phi_)
    p.append(p_)
    x.append(x_)

# Interpolate solution vector
y_A_interp1d = [interp1d(x[i], y_A[i]) for i in range(len(number_cells_vec))]
y_C_interp1d = [interp1d(x[i], y_C[i]) for i in range(len(number_cells_vec))]
y_S_interp1d = [interp1d(x[i], y_S[i]) for i in range(len(number_cells_vec))]
phi_interp1d = [interp1d(x[i], phi[i]) for i in range(len(number_cells_vec))]
p_interp1d = [interp1d(x[i], p[i]) for i in range(len(number_cells_vec))]

# Calculate L2-error
y_A_error_L2, y_C_error_L2, y_S_error_L2, phi_error_L2, p_error_L2 = [], [], [], [], []
for i in range(len(number_cells_vec)-1):
    y_A_error_L2.append(np.trapz((y_A_interp1d[i](x[i]) - y_A_interp1d[-1](x[i]))**2, x[i]))
    y_C_error_L2.append(np.trapz((y_C_interp1d[i](x[i]) - y_C_interp1d[-1](x[i]))**2, x[i]))
    y_S_error_L2.append(np.trapz((y_S_interp1d[i](x[i]) - y_S_interp1d[-1](x[i]))**2, x[i]))
    phi_error_L2.append(np.trapz((phi_interp1d[i](x[i]) - phi_interp1d[-1](x[i]))**2, x[i]))
    p_error_L2.append(np.trapz((p_interp1d[i](x[i]) - p_interp1d[-1](x[i]))**2, x[i]))
    
# Log-log plot of L2-error
plt.figure()
plt.loglog(number_cells_vec[:-1], y_A_error_L2, 'o-', label='$y_A$')
plt.loglog(number_cells_vec[:-1], y_C_error_L2, 'o-', label='$y_C$')
plt.loglog(number_cells_vec[:-1], y_S_error_L2, 'o-', label='$y_S$')
plt.loglog(number_cells_vec[:-1], phi_error_L2, 'o-', label='$\\varphi$')
plt.loglog(number_cells_vec[:-1], p_error_L2, 'o-', label='$p$')
plt.legend()
plt.xlabel('log(nx)')
plt.ylabel('log($L_2$)')
plt.grid()
plt.tight_layout()
plt.show()

# Calculate infinity error
y_A_error_inf, y_C_error_inf, y_S_error_inf, phi_error_inf, p_error_inf = [], [], [], [], []
for i in range(len(number_cells_vec)-1):
    y_A_error_inf.append(np.max(np.abs(y_A_interp1d[i](x[i]) - y_A_interp1d[-1](x[i]))))
    y_C_error_inf.append(np.max(np.abs(y_C_interp1d[i](x[i]) - y_C_interp1d[-1](x[i]))))
    y_S_error_inf.append(np.max(np.abs(y_S_interp1d[i](x[i]) - y_S_interp1d[-1](x[i]))))
    phi_error_inf.append(np.max(np.abs(phi_interp1d[i](x[i]) - phi_interp1d[-1](x[i]))))
    p_error_inf.append(np.max(np.abs(p_interp1d[i](x[i]) - p_interp1d[-1](x[i]))))
    
# Log-log plot of infinity error
plt.figure()
plt.loglog(number_cells_vec[:-1], y_A_error_inf, 'o-', label='$y_A$')
plt.loglog(number_cells_vec[:-1], y_C_error_inf, 'o-', label='$y_C$')
plt.loglog(number_cells_vec[:-1], y_S_error_inf, 'o-', label='$y_S$')
plt.loglog(number_cells_vec[:-1], phi_error_inf, 'o-', label='$\\varphi$')
plt.loglog(number_cells_vec[:-1], p_error_inf, 'o-', label='$p$')
plt.legend()
plt.xlabel('log(nx)')
plt.ylabel('log($L_\infty$)')
plt.grid()
plt.tight_layout()
plt.show()
