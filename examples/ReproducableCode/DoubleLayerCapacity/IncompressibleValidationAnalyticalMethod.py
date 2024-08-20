'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to validate the analytical method for the calculation of the double layer capacity.

# ! Problems, if solvation != 0. Further investigation is needed.
'''

# import the src file needed to solve the system of equations
import sys
import os

# Add the src directory to the sys.path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../', 'src')
sys.path.insert(0, src_path)

from Eq04 import solve_System_4eq
from Eq02 import solve_System_2eq
from Helper_DoubleLayerCapacity import Phi_pot_center, dx, C_dl, n, Q_num_, Q_DL_dimless_ana, Q_DL_dim_ana


# Remove the src directory from sys.path after import
del sys.path[0]

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

# Parameter and bcs for the electrolyte
Lambda2 = (k*T*epsilon0*(1+chi))/(e0**2 * nR_m * (LR)**2)
a2 = (pR)/(nR_m * k * T)
K = 'incompressible'
kappa = 0
Molarity = 0.01
y_R = Molarity / nR_mol
z_A, z_C = -1.0, 1.0
phi_right = 0.0
p_right = 0

# Solver settings
number_cells = 1024
relax_param = 0.03
p_right = 0
rtol = 1e-4 # ! Change back to 1e-8


# phi^L domain
Vol_start = 0.1 # ! Change back to 0
Volt_end = 0.75
n_Volts = 5#0

phi_left = np.linspace(Vol_start, Volt_end, n_Volts) * e0/(k*T)


# Numerical calculations
# Solution vectors
y_A_num, y_C_num, y_S_num, phi_num, p_num, x_num = [], [], [], [], [], []
for i, phi_bcs in enumerate(phi_left):
    y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_bcs, phi_right, p_right, z_A, z_C, y_R, y_R, K, Lambda2, a2, number_cells, solvation=kappa, refinement_style='hard_log', rtol=rtol, max_iter=2500, return_type='Vector', relax_param=relax_param)
    y_S_ = 1 - y_A_ - y_C_
    y_A_num.append(y_A_)
    y_C_num.append(y_C_)
    y_S_num.append(y_S_)
    phi_num.append(phi_)
    p_num.append(p_)
    x_num.append(x_)
    
Q_num = []
for j in range(len(phi_left)):
    Q_num.append(Q_num_(y_A_num[j], y_C_num[j], n(p_num[j], K), x_num[j]))
Q_num = np.array(Q_num)

dx_ = phi_left[1] - phi_left[0] # [1/V], Assumption: phi^L is uniformly distributed
C_DL_num = (Q_num[1:] - Q_num[:-1])/dx_ # [µAs/cm³]
C_DL_num = np.array(C_DL_num)
C_dl_num = C_dl(Q_num, phi_left)



# Analytical calculations
Q_ana = Q_DL_dimless_ana(y_R, y_R, 1-2*y_R, z_A, z_C, phi_left, phi_right, p_right, K, Lambda2, a2, kappa)
C_DL_ana = C_dl(Q_ana, phi_left)


# Plotting
plt.figure()
# plt.plot(phi_left, Q_num - Q_ana, label='Difference')
# plt.plot(phi_left, Q_num, label='Numerical')
plt.plot(phi_left, Q_ana, label='Analytical')
plt.grid()
plt.legend()
plt.xlabel('$\delta \\varphi$ [-]')
plt.ylabel('$Q_{num} - Q_{ana} [-]$')
plt.tight_layout()
plt.show()   

plt.figure()
# plt.plot(Phi_pot_center(phi_left), C_DL_num - C_DL_ana, label='Difference')
# plt.plot(Phi_pot_center(phi_left), C_dl_num, label='Numerical')
plt.plot(Phi_pot_center(phi_left), C_DL_ana, label='Analytical')
plt.grid()
plt.legend()
plt.xlabel('$\delta \\varphi$ [-]')
plt.ylabel('$C_{dl,num} - C_{dl,ana} [-]$')
plt.tight_layout()
plt.show()

print('phi_left:', phi_left)
print('Q_num:', Q_num)
print('Q_ana:', Q_ana)