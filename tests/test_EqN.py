''' 
Tests the EqN implementation in src.EqN.py
'''

# from src.EqN import solve_System_Neq
from FENICSxDGM import solve_System_Neq
import numpy as np

# Define the testing tolerance
rtol = 1e-10
atol = 1e-10

# Define parameter to use in the test
phi_left = 10.0
phi_right = 0.0
p_right = 0.0
y_R = [3/6, 1/6, 1/6]
z_alpha = [-1.0, 1.0, 2.0]
K = 'incompressible'
Lambda2 = 8.553e-6
a2 = 7.5412e-4
solvation = 0
number_cells = 32
relax_param = .1
rtol = 1e-4
max_iter = 500

data_comparison = np.load('tests/TestData/EqN.npz')

def test_1():
    y_alpha, phi, p, x = solve_System_Neq(phi_left, phi_right, p_right, z_alpha, y_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, x0=0, x1=1, refinement_style='uniform', return_type='Vector', max_iter=max_iter, rtol=rtol)

    # test grid generation with no refinement
    assert np.allclose(data_comparison['x'], x,\
                        rtol=rtol, atol=atol),\
                        'Uniform grid not generated correctly'
    # test solution vector
    assert np.allclose(data_comparison['y_alpha'], y_alpha,\
                        rtol=rtol, atol=atol),\
                        'y_alpha not calculated correctly'
    assert np.allclose(data_comparison['phi'], phi,\
                        rtol=rtol, atol=atol),\
                        'phi not calculated correctly'
    assert np.allclose(data_comparison['p'], p,\
                        rtol=rtol, atol=atol),\
                        'p not calculated correctly'
    
def test_2():
    y_R = [1/23, 1/23, 1/23, 1/23, 10/23]
    z_alpha = [-4.0, -3.0, -2.0, -1.0, 1.0]
    relax_param = 0.01
    max_iter = 10_000

    y_alpha_2, phi_2, p_2, x_2 = solve_System_Neq(phi_left, phi_right, p_right, z_alpha, y_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, x0=0, x1=1, refinement_style='log', return_type='Vector', max_iter=max_iter, rtol=rtol)

    # test grid generation with no refinement
    assert np.allclose(data_comparison['x_2'], x_2,\
                        rtol=rtol, atol=atol),\
                        'Log grid not generated correctly'
    # test solution vector
    assert np.allclose(data_comparison['y_alpha_2'], y_alpha_2,\
                        rtol=rtol, atol=atol),\
                        'y_alpha_2 not calculated correctly'
    assert np.allclose(data_comparison['phi_2'], phi_2,\
                        rtol=rtol, atol=atol),\
                        'phi_2 not calculated correctly'
    assert np.allclose(data_comparison['p_2'], p_2,\
                        rtol=rtol, atol=atol),\
                        'p_2 not calculated correctly'
    