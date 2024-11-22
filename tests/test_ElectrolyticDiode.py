''' 
Tests the ElectrolyticDiode implementation in src.ElectrolyticDiode.py
'''

# from src.ElectrolyticDiode import ElectrolyticDiode
from FENICSxDGM import ElectrolyticDiode
import numpy as np

# Define the testing tolerance
rtol = 1e-10
atol = 1e-10

# Define parameter to use in the test
phi_bias = 10
g_phi = 350
y_fixed = 0.01
z_A = -1.0
z_C = 1.0
K = 'incompressible'
Lambda2 = 8.553e-6
a2 = 7.5412e-4
number_cells = [10, 64]
Lx = 0.02
Ly = 0.1
x0 = np.array([0, 0])
x1 = np.array([Lx, Ly])
refinement_style = 'uniform'
solvation = 5
PoissonBoltzmann = False
rtol = 1e-3 
relax_param = 0.1
max_iter = 100
    

data_comparison = np.load('tests/TestData/ElectrolyticDiode.npz')

def test_ForwardBias():
    y_A_ForwardBias, y_C_ForwardBias, phi_ForwardBias, p_ForwardBias, x_ForwardBias = ElectrolyticDiode('ForwardBias', phi_bias, g_phi, z_A, z_C, y_fixed, y_fixed, K, Lambda2, a2, number_cells, solvation, PoissonBoltzmann, relax_param, Lx, Ly, rtol, max_iter, return_type='Vector')

    # test grid generation with no refinement
    assert np.allclose(data_comparison['x_ForwardBias'], x_ForwardBias,\
                        rtol=rtol, atol=atol),\
                        'ForwardBias grid not generated correctly'
    # test solution vector
    assert np.allclose(data_comparison['y_A_ForwardBias'], y_A_ForwardBias,\
                        rtol=rtol, atol=atol),\
                        'y_A_ForwardBias not calculated correctly'
    assert np.allclose(data_comparison['y_C_ForwardBias'], y_C_ForwardBias,\
                        rtol=rtol, atol=atol),\
                        'y_C_ForwardBias not calculated correctly'
    assert np.allclose(data_comparison['phi_ForwardBias'], phi_ForwardBias,\
                        rtol=rtol, atol=atol),\
                        'phi_ForwardBias not calculated correctly'
    assert np.allclose(data_comparison['p_ForwardBias'], p_ForwardBias,\
                        rtol=rtol, atol=atol),\
                        'p_ForwardBias not calculated correctly'
