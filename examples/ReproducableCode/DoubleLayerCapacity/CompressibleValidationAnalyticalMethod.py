'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to validate the analytical method for the calculation of the double layer capacity.

# ! Problems, if solvation != 0. Further investigation is needed.
'''

# import the needed functions from the fxdgm module
from fxdgm import solve_System_4eq, Phi_pot_center, C_dl, n, Q_num_, Q_num_dim, Q_DL_dimless_ana, Q_DL_dim_ana, C_DL_dimless_ana, C_DL_dim_ana

# Import plotting library
import matplotlib.pyplot as plt
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
K_vec = ['incompressible', 50_000, 15_000, 1_500, 500]
# Parameter and bcs for the electrolyte
Lambda2 = (k*T*epsilon0*(1+chi))/(e0**2 * nR_m * (LR)**2)
a2 = (pR)/(nR_m * k * T)
kappa = 0
K = 50_000
Molarity = 0.01
y_R = Molarity / nR_mol
z_A, z_C = -1.0, 1.0
phi_right = 0.0
p_right = 0

# Solver settings
number_cells = 1024
relax_param = 0.03
p_right = 0


# phi^L domain
Vol_start = 0
Volt_end = 0.75
n_Volts = 25#0

phi_left_dim = np.linspace(Vol_start, Volt_end, n_Volts) 
phi_left_dimless = phi_left_dim * e0/(k*T)


# Numerical calculations
# Solution vectors
y_A_num, y_C_num, y_S_num, phi_num, p_num, x_num = [], [], [], [], [], []
for i, phi_bcs in enumerate(phi_left_dimless):
    y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_bcs, phi_right, p_right, z_A, z_C, y_R, y_R, K, Lambda2, a2, number_cells, solvation=kappa, refinement_style='hard_log', rtol=1e-4, max_iter=2500, return_type='Vector', relax_param=relax_param)
    y_S_ = 1 - y_A_ - y_C_
    y_A_num.append(y_A_)
    y_C_num.append(y_C_)
    y_S_num.append(y_S_)
    phi_num.append(phi_)
    p_num.append(p_)
    x_num.append(x_)
    
Q_num = []
Q_num_dim_ = []
for j in range(len(phi_left_dimless)):
    Q_num.append(Q_num_(y_A_num[j], y_C_num[j], n(p_num[j], K), x_num[j]))
    Q_num_dim_.append(Q_num_dim(y_A_num[j], y_C_num[j], n(p_num[j], K), x_num[j], z_A, z_C, nR_m, e0, LR))
Q_num = np.array(Q_num)
Q_num_dim_ = np.array(Q_num_dim_)

dx_ = phi_left_dimless[1] - phi_left_dimless[0] # [1/V], Assumption: phi^L is uniformly distributed
C_dl_num = C_dl(Q_num, phi_left_dimless)

dx_dim = phi_left_dim[1] - phi_left_dim[0] 
C_dl_num_dim_ = C_dl(Q_num_dim_, phi_left_dim)

# Analytical calculations
Q_ana = Q_DL_dimless_ana(y_R, y_R, 1-2*y_R, z_A, z_C, phi_left_dimless, phi_right, p_right, K, Lambda2, a2, kappa)
Q_ana_dim_ = Q_DL_dim_ana(y_R, y_R, 1-2*y_R, z_A, z_C, phi_left_dimless, phi_right, p_right, K, Lambda2, a2, nR_m, e0, LR, kappa)
C_dl_ana = C_DL_dimless_ana(y_R, y_R, 1-2*y_R, z_A, z_C, Phi_pot_center(phi_left_dimless), phi_right, p_right, K, Lambda2, a2, kappa)
C_dl_ana_dim = C_DL_dim_ana(y_R, y_R, 1-2*y_R, z_A, z_C, Phi_pot_center(phi_left_dimless), phi_right, p_right, K, Lambda2, a2, nR_m, e0, LR, k, T, kappa)


# Plotting
plt.figure()
plt.title('Charge (dimensionless)')
plt.plot(phi_left_dimless, Q_num, label='Numerical')
plt.plot(phi_left_dimless, Q_ana, label='Analytical')
plt.grid()
plt.legend()
plt.xlabel('$\delta \\varphi$ [-]')
plt.ylabel('$Q[-]$')
plt.tight_layout()
plt.savefig('../../Figures/DoubleLayerCapacity_Validation_Compressible.pdf')
plt.show()    

plt.figure()
# Use Center points to evaluate on same x-points
plt.title('Charge (dimensionless)')
plt.plot(Phi_pot_center(phi_left_dimless), C_dl_num, label='Numerical')
plt.plot(Phi_pot_center(phi_left_dimless), C_dl_ana, label='Analytical')
plt.grid()
plt.legend()
plt.xlabel('$\delta \\varphi$ [-]')
plt.ylabel('$C_{dl}[-]$')
plt.tight_layout()
plt.savefig('../../Figures/DoubleLayerCharge_Validation_Compressible.pdf')
plt.show()
