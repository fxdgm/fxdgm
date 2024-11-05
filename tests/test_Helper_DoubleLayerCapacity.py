''' 
Tests the Helpfer functions implemented in src.Helper_DoubleLayerCapacity.py
'''


from src.Helper_DoubleLayerCapacity import Phi_pot_center, dx, C_dl, n, Q_num_, Q_num_dim, Q_DL_dimless_ana, Q_DL_dim_ana, C_DL_dimless_ana, C_DL_dim_ana
from src.Eq04 import solve_System_4eq
from src.Eq02 import solve_System_2eq
import numpy as np

# Define Parameter
e0 = 1.602e-19 # [As]
k = 1.381e-23 # [J/K]
T = 293.75 # [K]
epsilon0 = 8.85e-12 #[F/m]
F = 9.65e+4 # [As/mol]
NA = 6.022e+23 # [1/mol] - Avogadro constant
nR_mol = 55
nR_m = nR_mol * NA * 1/(1e-3)# [1/m^3]
pR = 1.01325 * 1e+5 # [Pa]
LR = 20e-9
chi = 80 # [-]

# Parameter and bcs for the electrolyte
Lambda2 = (k*T*epsilon0*(1+chi))/(e0**2 * nR_m * (LR)**2)
a2 = (pR)/(nR_m * k * T)
K_incompresible = 'incompressible'
K_compressible = 20_000
kappa = 0
Molarity = 0.01
y_R = Molarity / nR_mol
z_A, z_C = -1.0, 1.0
phi_right = 0.0
p_right = 0

# Solver settings
number_cells = 128
relax_param = 0.03
p_right = 0
rtol = 1e-4 # ! Change back to 1e-8


# phi^L domain
Vol_start = 0.05 # ! Change back to 0
Volt_end = 0.75
n_Volts = 10#0

phi_left_dim = np.linspace(Vol_start, Volt_end, n_Volts)
phi_left = phi_left_dim * e0/(k*T)

data_comparison = np.load('tests/TestData/DLKap.npz')



# Incompressible tests
def test_incompressible():
    # Calculate the numerical solution
    y_A_num, y_C_num, y_S_num, phi_num, p_num, x_num = [], [], [], [], [], []
    for i, phi_bcs in enumerate(phi_left):
        y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_bcs, phi_right, p_right, z_A, z_C, y_R, y_R, K_incompresible, Lambda2, a2, number_cells, solvation=kappa, refinement_style='hard_log', rtol=rtol, max_iter=2500, return_type='Vector', relax_param=relax_param)
        y_S_ = 1 - y_A_ - y_C_
        y_A_num.append(y_A_)
        y_C_num.append(y_C_)
        y_S_num.append(y_S_)
        phi_num.append(phi_)
        p_num.append(p_)
        x_num.append(x_)

    # Calculate the numerical charge and capacity with finite differences and numerical integration
    Q_num = []
    Q_num_dim_ = []
    for j in range(len(phi_left)):
        Q_num.append(Q_num_(y_A_num[j], y_C_num[j], n(p_num[j], K_incompresible), x_num[j]))
        Q_num_dim_.append(Q_num_dim(y_A_num[j], y_C_num[j], n(p_num[j], K_incompresible), x_num[j], z_A, z_C, nR_m, e0, LR))
    Q_num = np.array(Q_num)
    Q_num_dim_ = np.array(Q_num_dim_)

    dx_ = phi_left[1] - phi_left[0] # [1/V], Assumption: phi^L is uniformly distributed
    C_dl_num = C_dl(Q_num, phi_left)

    dx_dim = phi_left_dim[1] - phi_left_dim[0] 
    C_dl_num_dim_ = C_dl(Q_num_dim_, phi_left_dim)


    # Calculate the analytical charge and capacity
    Q_ana = Q_DL_dimless_ana(y_R, y_R, 1-2*y_R, z_A, z_C, phi_left, phi_right, p_right, K_incompresible, Lambda2, a2, kappa)
    Q_ana_dim_ = Q_DL_dim_ana(y_R, y_R, 1-2*y_R, z_A, z_C, phi_left, phi_right, p_right, K_incompresible, Lambda2, a2, nR_m, e0, LR, kappa)
    C_dl_ana = C_DL_dimless_ana(y_R, y_R, 1-2*y_R, z_A, z_C, Phi_pot_center(phi_left), phi_right, p_right, K_incompresible, Lambda2, a2, kappa)
    C_dl_ana_dim = C_DL_dim_ana(y_R, y_R, 1-2*y_R, z_A, z_C, Phi_pot_center(phi_left), phi_right, p_right, K_incompresible, Lambda2, a2, nR_m, e0, LR, k, T, kappa)

    # Test the numerical charge and capacity
    assert np.allclose(data_comparison['Q_num'], Q_num,\
                        rtol=1e-15, atol=1e-15),\
                        'Incompressible: Numerical charge not calculated correctly for dimensions'
    assert np.allclose(data_comparison['Q_num_dim_'], Q_num_dim_,\
                        rtol=1e-15, atol=1e-15),\
                        'Incompressible: Numerical charge not calculated correctly for dimensionless'
    assert np.allclose(data_comparison['C_dl_num'], C_dl_num,\
                        rtol=1e-15, atol=1e-15),\
                        'Incompressible: Numerical capacity not calculated correctly for dimensions'
    assert np.allclose(data_comparison['C_dl_num_dim_'], C_dl_num_dim_,\
                        rtol=1e-15, atol=1e-15),\
                        'Incompressible: Numerical capacity not calculated correctly for dimensionless'
    
    # Test the analytical charge and capacity
    assert np.allclose(data_comparison['Q_ana'], Q_ana,\
                        rtol=1e-15, atol=1e-15),\
                        'Incompressible: Analytical charge not calculated correctly for dimensions'
    assert np.allclose(data_comparison['Q_ana_dim_'], Q_ana_dim_,\
                        rtol=1e-15, atol=1e-15),\
                        'Incompressible: Analytical charge not calculated correctly for dimensionless'
    assert np.allclose(data_comparison['C_dl_ana'], C_dl_ana,\
                        rtol=1e-15, atol=1e-15),\
                        'Incompressible: Analytical capacity not calculated correctly for dimensions'
    assert np.allclose(data_comparison['C_dl_ana_dim'], C_dl_ana_dim,\
                        rtol=1e-15, atol=1e-15),\
                        'Incompressible: Analytical capacity not calculated correctly for dimensionless'
    
# Compressible tests
def test_compressible():
    # Calculate the numerical solution
    y_A_num_compressible, y_C_num_compressible, y_S_num_compressible, phi_num_compressible, p_num_compressible, x_num_compressible = [], [], [], [], [], []
    for i, phi_bcs in enumerate(phi_left):
        y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_bcs, phi_right, p_right, z_A, z_C, y_R, y_R, K_compressible, Lambda2, a2, number_cells, solvation=kappa, refinement_style='hard_log', rtol=1e-4, max_iter=2500, return_type='Vector', relax_param=relax_param)
        y_S_ = 1 - y_A_ - y_C_
        y_A_num_compressible.append(y_A_)
        y_C_num_compressible.append(y_C_)
        y_S_num_compressible.append(y_S_)
        phi_num_compressible.append(phi_)
        p_num_compressible.append(p_)
        x_num_compressible.append(x_)

    # Calculate the numerical charge and capacity with finite differences and numerical integration
    Q_num_compressible = []
    Q_num_dim_compressible = []
    for j in range(len(phi_left)):
        Q_num_compressible.append(Q_num_(y_A_num_compressible[j], y_C_num_compressible[j], n(p_num_compressible[j], K_compressible), x_num_compressible[j]))
        Q_num_dim_compressible.append(Q_num_dim(y_A_num_compressible[j], y_C_num_compressible[j], n(p_num_compressible[j], K_compressible), x_num_compressible[j], z_A, z_C, nR_m, e0, LR))
    Q_num_compressible = np.array(Q_num_compressible)
    Q_num_dim_compressible = np.array(Q_num_dim_compressible)

    dx__compressible = phi_left[1] - phi_left[0] # [1/V], Assumption: phi^L is uniformly distributed
    C_dl_num_compressible = C_dl(Q_num_compressible, phi_left)

    dx_dim_compressible = phi_left_dim[1] - phi_left_dim[0] 
    C_dl_num_dim_compressible = C_dl(Q_num_dim_compressible, phi_left_dim)

    # Calculate the analytical charge and capacity
    Q_ana_compressible = Q_DL_dimless_ana(y_R, y_R, 1-2*y_R, z_A, z_C, phi_left, phi_right, p_right, K_compressible, Lambda2, a2, kappa)
    Q_ana_dim__compressible = Q_DL_dim_ana(y_R, y_R, 1-2*y_R, z_A, z_C, phi_left, phi_right, p_right, K_compressible, Lambda2, a2, nR_m, e0, LR, kappa)
    C_dl_ana_compressible = C_DL_dimless_ana(y_R, y_R, 1-2*y_R, z_A, z_C, Phi_pot_center(phi_left), phi_right, p_right, K_compressible, Lambda2, a2, kappa)
    C_dl_ana_dim_compressible = C_DL_dim_ana(y_R, y_R, 1-2*y_R, z_A, z_C, Phi_pot_center(phi_left), phi_right, p_right, K_compressible, Lambda2, a2, nR_m, e0, LR, k, T, kappa)

    # Test the numerical charge and capacity
    assert np.allclose(data_comparison['Q_num_compressible'], Q_num_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'Compressible: Numerical charge not calculated correctly for dimensions'
    assert np.allclose(data_comparison['Q_num_dim_compressible'], Q_num_dim_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'Compressible: Numerical charge not calculated correctly for dimensionless'
    assert np.allclose(data_comparison['C_dl_num_compressible'], C_dl_num_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'Compressible: Numerical capacity not calculated correctly for dimensions'
    assert np.allclose(data_comparison['C_dl_num_dim_compressible'], C_dl_num_dim_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'Compressible: Numerical capacity not calculated correctly for dimensionless'
    
    # Test the analytical charge and capacity
    assert np.allclose(data_comparison['Q_ana_compressible'], Q_ana_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'Compressible: Analytical charge not calculated correctly for dimensions'
    assert np.allclose(data_comparison['Q_ana_dim__compressible'], Q_ana_dim__compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'Compressible: Analytical charge not calculated correctly for dimensionless'
    assert np.allclose(data_comparison['C_dl_ana_compressible'], C_dl_ana_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'Compressible: Analytical capacity not calculated correctly for dimensions'
    assert np.allclose(data_comparison['C_dl_ana_dim_compressible'], C_dl_ana_dim_compressible,\
                        rtol=1e-15, atol=1e-15),\
                        'Compressible: Analytical capacity not calculated correctly for dimensionless'
    
# Test the functions
def test_Phi_pot_center():
    assert np.allclose(Phi_pot_center(phi_left), data_comparison['Phi_pot_center'],\
                        rtol=1e-15, atol=1e-15),\
                        'Phi_pot_center not calculated correctly'
    
def test_dx():
    assert np.allclose(dx(phi_left), data_comparison['dx'],\
                        rtol=1e-15, atol=1e-15),\
                        'dx not calculated correctly'
def test_n():
    assert np.allclose(n(data_comparison['p_num_compressible'][0], K_compressible), data_comparison['n'], rtol=1e-15, atol=1e-15),\
                        'n not calculated correctly'
    