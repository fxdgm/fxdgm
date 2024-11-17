''' 
Tests the Eq04 implementation in src.Eq04.py
'''

from src.Eq04 import solve_System_4eq
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

data_comparison = np.load('tests/TestData/Eq04.npz')

def test_standard():
    y_A, y_C, phi, p, x = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, x0=0, x1=1, refinement_style='uniform', return_type='Vector', max_iter=max_iter, rtol=rtol)

    # test grid generation with no refinement
    assert np.allclose(data_comparison['x'], x,\
                        rtol=rtol, atol=atol),\
                        'Uniform grid not generated correctly'
    # test solution vector
    assert np.allclose(data_comparison['y_A'], y_A,\
                        rtol=rtol, atol=atol),\
                        'y_A not calculated correctly'
    assert np.allclose(data_comparison['y_C'], y_C,\
                        rtol=rtol, atol=atol),\
                        'y_C not calculated correctly'
    assert np.allclose(data_comparison['phi'], phi,\
                        rtol=rtol, atol=atol),\
                        'phi not calculated correctly'
    assert np.allclose(data_comparison['p'], p,\
                        rtol=rtol, atol=atol),\
                        'p not calculated correctly'
    
def test_NerstPlanck():
    y_A_NP, y_C_NP, phi_NP, p_NP, x_NP = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, PoissonBoltzmann=True, x0=0, x1=1, refinement_style='uniform', return_type='Vector', max_iter=max_iter, rtol=rtol)

    # test grid generation with no refinement
    assert np.allclose(data_comparison['x_NP'], x_NP,\
                        rtol=rtol, atol=atol),\
                        'Uniform grid not generated correctly'
    # test solution vector
    assert np.allclose(data_comparison['y_A_NP'], y_A_NP,\
                        rtol=rtol, atol=atol),\
                        'y_A with NP not calculated correctly'
    assert np.allclose(data_comparison['y_C_NP'], y_C_NP,\
                        rtol=rtol, atol=atol),\
                        'y_C with NP not calculated correctly'
    assert np.allclose(data_comparison['phi_NP'], phi_NP,\
                        rtol=rtol, atol=atol),\
                        'phi with NP not calculated correctly'
    assert np.allclose(data_comparison['p_NP'], p_NP,\
                        rtol=rtol, atol=atol),\
                        'p with NP not calculated correctly'

def test_solvation():
    solvation = 5
    y_A_solvation, y_C_solvation, phi_solvation, p_solvation, x_solvation = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, x0=0, x1=1, refinement_style='log', return_type='Vector', max_iter=max_iter, rtol=rtol)

    # test grid generation with logarithmic refinement
    assert np.allclose(data_comparison['x_solvation'], x_solvation,\
                        rtol=rtol, atol=atol),\
                        'log grid not generated correctly'
    # test solution vector
    assert np.allclose(data_comparison['y_A_solvation'], y_A_solvation,\
                        rtol=rtol, atol=atol),\
                        'y_A with solvation not calculated correctly'
    assert np.allclose(data_comparison['y_C_solvation'], y_C_solvation,\
                        rtol=rtol, atol=atol),\
                        'y_C with solvation not calculated correctly'
    assert np.allclose(data_comparison['phi_solvation'], phi_solvation,\
                        rtol=rtol, atol=atol),\
                        'phi with solvation not calculated correctly'
    assert np.allclose(data_comparison['p_solvation'], p_solvation,\
                        rtol=rtol, atol=atol),\
                        'p with solvation not calculated correctly'

def test_compressibility():
    solvation = 0
    K = 5_000
    y_A_compressible, y_C_compressible, phi_compressible, p_compressible, x_compressible = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, x0=0, x1=1, refinement_style='hard_log', return_type='Vector', max_iter=max_iter, rtol=rtol)

    # test grid generation with hard-logarithmic refinement
    assert np.allclose(data_comparison['x_compressible'], x_compressible,\
                        rtol=rtol, atol=atol),\
                        'hard-log grid not generated correctly'
    # test solution vector
    assert np.allclose(data_comparison['y_A_compressible'], y_A_compressible,\
                        rtol=rtol, atol=atol),\
                        'y_A with compressible not calculated correctly'
    assert np.allclose(data_comparison['y_C_compressible'], y_C_compressible,\
                        rtol=rtol, atol=atol),\
                        'y_C with compressible not calculated correctly'
    assert np.allclose(data_comparison['phi_compressible'], phi_compressible,\
                        rtol=rtol, atol=atol),\
                        'phi with compressible not calculated correctly'
    assert np.allclose(data_comparison['p_compressible'], p_compressible,\
                        rtol=rtol, atol=atol),\
                        'p with compressible not calculated correctly'
    