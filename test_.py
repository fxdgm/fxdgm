''' 
Tests the Eq02 implementation in src.Eq02.py
'''

from src.Eq02 import solve_System_2eq
import numpy as np

# Define the testing tolerance
rtol = 1e-10
atol = 1e-10

# Define parameter to use in the test
phi_left = 10.0
phi_right = 0.0
p_right = 0.0
y_A_R = 0.01
y_C_R = 0.01
z_A = -1.0
z_C = 1.0
K = 'incompressible'
Lambda2 = 8.553e-6
a2 = 7.5412e-4
solvation = 0
number_cells = 32
relax_param = .1
rtol = 1e-4
max_iter = 500

y_A, y_C, phi, p, x = solve_System_2eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, x0=0, x1=1, refinement_style='uniform', return_type='Vector', max_iter=max_iter, rtol=rtol)

y_A_NP, y_C_NP, phi_NP, p_NP, x_NP = solve_System_2eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, PoissonBoltzmann=True, x0=0, x1=1, refinement_style='uniform', return_type='Vector', max_iter=max_iter, rtol=rtol)

solvation = 5
y_A_solvation, y_C_solvation, phi_solvation, p_solvation, x_solvation = solve_System_2eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, x0=0, x1=1, refinement_style='log', return_type='Vector', max_iter=max_iter, rtol=rtol)

solvation = 0
K = 5_000
y_A_compressible, y_C_compressible, phi_compressible, p_compressible, x_compressible = solve_System_2eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, x0=0, x1=1, refinement_style='hard_log', return_type='Vector', max_iter=max_iter, rtol=rtol)

np.savez('tests/TestData/Eq02.npz', y_A=y_A, y_C=y_C, phi=phi, p=p, x=x, y_A_NP=y_A_NP, y_C_NP=y_C_NP, phi_NP=phi_NP, p_NP=p_NP, x_NP=x_NP, y_A_solvation=y_A_solvation, y_C_solvation=y_C_solvation, phi_solvation=phi_solvation, p_solvation=p_solvation, x_solvation=x_solvation, y_A_compressible=y_A_compressible, y_C_compressible=y_C_compressible, phi_compressible=phi_compressible, p_compressible=p_compressible, x_compressible=x_compressible)