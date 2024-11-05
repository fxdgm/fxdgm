''' 
Tests the Eq02 implementation in src.Eq02.py
'''


from src.Eq02 import solve_System_2eq
import numpy as np

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

data_comparison = np.load('tests/TestData/Eq02.npz')

def test_standard():
    y_A, y_C, phi, p, x = solve_System_2eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, x0=0, x1=1, refinement_style='uniform', return_type='Vector', max_iter=max_iter, rtol=rtol)

    # test grid generation with no refinement
    assert np.allclose(data_comparison['x'], x,\
                        rtol=1e-15, atol=1e-15),\
                        'Uniform grid not generated correctly'
    # test solution vector
    assert np.allclose(data_comparison['y_A'], y_A,\
                        rtol=1e-15, atol=1e-15),\
                        'y_A not calculated correctly'
    assert np.allclose(data_comparison['y_C'], y_C,\
                        rtol=1e-15, atol=1e-15),\
                        'y_C not calculated correctly'
    assert np.allclose(data_comparison['phi'], phi,\
                        rtol=1e-15, atol=1e-15),\
                        'phi not calculated correctly'
    assert np.allclose(data_comparison['p'], p,\
                        rtol=1e-15, atol=1e-15),\
                        'p not calculated correctly'


def test_solvation():
    solvation = 5
    y_A_solvation, y_C_solvation, phi_solvation, p_solvation, x_solvation = solve_System_2eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, x0=0, x1=1, refinement_style='log', return_type='Vector', max_iter=max_iter, rtol=rtol)

    # test grid generation with logarithmic refinement
    assert np.allclose(data_comparison['x_solvation'], x_solvation,\
                        rtol=1e-15, atol=1e-15),\
                        'log grid not generated correctly'
    # test solution vector
    assert np.allclose(data_comparison['y_A_solvation'], y_A_solvation,\
                        rtol=1e-15, atol=1e-15),\
                        'y_A with solvation not calculated correctly'
    assert np.allclose(data_comparison['y_C_solvation'], y_C_solvation,\
                        rtol=1e-15, atol=1e-15),\
                        'y_C with solvation not calculated correctly'
    assert np.allclose(data_comparison['phi_solvation'], phi_solvation,\
                        rtol=1e-15, atol=1e-15),\
                        'phi with solvation not calculated correctly'
    assert np.allclose(data_comparison['p_solvation'], p_solvation,\
                        rtol=1e-15, atol=1e-15),\
                        'p with solvation not calculated correctly'

def test_compressibility():
    solvation = 0
    K = 5_000
    y_A_compressible, y_C_compressible, phi_compressible, p_compressible, x_compressible = solve_System_2eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=solvation,  relax_param=relax_param, x0=0, x1=1, refinement_style='hard_log', return_type='Vector', max_iter=max_iter, rtol=rtol)

    # test grid generation with hard-logarithmic refinement
    assert np.allclose(data_comparison['x_compressible'], x_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'hard-log grid not generated correctly'
    # test solution vector
    assert np.allclose(data_comparison['y_A_compressible'], y_A_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'y_A with compressible not calculated correctly'
    assert np.allclose(data_comparison['y_C_compressible'], y_C_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'y_C with compressible not calculated correctly'
    assert np.allclose(data_comparison['phi_compressible'], phi_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'phi with compressible not calculated correctly'
    assert np.allclose(data_comparison['p_compressible'], p_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'p with compressible not calculated correctly'
    