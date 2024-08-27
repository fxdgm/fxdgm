'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to validate the implemetation with:
Wolfgang Dreyer, Clemens Guhlke, and Rüdiger Müller. Bulk-surface electrothermodynamics and applications to electrochemistry. Entropy, 20(12), 2018
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
import matplotlib.ticker as ticker
import numpy as np

# Define the parameters and boundary conditions
e0 = 1.602e-19 # [As]
k = 1.381e-23 # [J/K]
T = 293.75#298#293.15 # [K]
epsilon0 = 8.85e-12 #[F/m]
F = 9.65e+4 # [As/mol]
NA = 6.022e+23 # [1/mol] - Avogadro constant
p_ref = 1.01325 * 1e+5 # [Pa]
L_ref = 10e-9#20e-9#20e-9 # [m]
chi = 80 # [-]

# BCS according to Dreyer
nRef = 55.4 # [mol/L]
Molarity = 0.5
y_A_R, y_C_R = Molarity / nRef, Molarity / nRef #0.01, 0.01
pR = 0
z_A, z_C = -1.0, 1.0
nR_m = nRef * NA * 1/(1e-3) # [1/m^3]
phi_L_dim = 0.6 # [V] ->  600 mV
phi_R_dim = 0.0 # [V]
phi_L_dimless = phi_L_dim * e0 / (k * T)
phi_R_dimless = phi_R_dim * e0 / (k * T)
phi_L_dimless, phi_R_dimless

# Parameters
K = 'incompressible'
Lambda2 = (k*T*epsilon0*(1+chi))/(e0**2 * nR_m * (L_ref)**2)
a2 = (p_ref)/(nR_m * k * T)
Lambda2, a2 # values not sure, as T, chi and L_ref not given in Dreyer paper

# Solver parameters
number_cells = 1028*32
relax_param = 0.005
refinement_style = 'log'
max_iter = 100_000
return_type = 'Vector'
rtol = 1e-7


y_A_dimless, y_C_dimless, y_S_dimless, phi_dimless, p_dimless, x_dimless = [], [], [], [], [], []
y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_L_dimless, phi_R_dimless, pR, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=0, PoissonBoltzmann=True, relax_param=relax_param, refinement_style=refinement_style, return_type=return_type, max_iter=max_iter, rtol=rtol)
y_A_dimless.append(y_A_)
y_C_dimless.append(y_C_)
y_S_dimless.append(1 - y_A_ - y_C_)
phi_dimless.append(phi_)
p_dimless.append(p_)
x_dimless.append(x_)

y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_L_dimless, phi_R_dimless, pR, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells=number_cells, solvation=0, PoissonBoltzmann=False, relax_param=relax_param, refinement_style=refinement_style, return_type=return_type, max_iter=max_iter, rtol=rtol)
y_A_dimless.append(y_A_)
y_C_dimless.append(y_C_)
y_S_dimless.append(1 - y_A_ - y_C_)
phi_dimless.append(phi_)
p_dimless.append(p_)
x_dimless.append(x_)

y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_L_dimless, phi_R_dimless, pR, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells=number_cells, solvation=8, PoissonBoltzmann=False, relax_param=relax_param, refinement_style=refinement_style, return_type=return_type, max_iter=max_iter, rtol=rtol)
y_A_dimless.append(y_A_)
y_C_dimless.append(y_C_)
y_S_dimless.append(1 - y_A_ - y_C_)
phi_dimless.append(phi_)
p_dimless.append(p_)
x_dimless.append(x_)

# Rescale to physical values
y_A_dimless, y_C_dimless, y_S_dimless, phi_dimless, p_dimless, x_dimless = np.array(y_A_dimless), np.array(y_C_dimless), np.array(y_S_dimless), np.array(phi_dimless), np.array(p_dimless), np.array(x_dimless)
phi_dim = phi_dimless * k * T / e0
p_dim = p_dimless * p_ref
x_dim = x_dimless * L_ref
y_A_dim = y_A_dimless
y_C_dim = y_C_dimless
y_S_dim = y_S_dimless
n_A_dim = y_A_dim * nRef
n_C_dim = y_C_dim * nRef
n_S_dim = y_S_dim * nRef

# Store the results
np.savez('../Data/Validation_Dreyer_BulkSurface.npz', y_A_dimless=y_A_dimless, y_C_dimless=y_C_dimless, y_S_dimless=y_S_dimless, phi_dimless=phi_dimless, p_dimless=p_dimless, x_dimless=x_dimless, y_A_dim=y_A_dim, y_C_dim=y_C_dim, y_S_dim=y_S_dim, n_A_dim=n_A_dim, n_C_dim=n_C_dim, n_S_dim=n_S_dim, phi_dim=phi_dim, p_dim=p_dim, x_dim=x_dim)