'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to analyze the influence of the compressibility on the charge of the system and the double-layer capacity.

# ! Efforts were made to simplify this similar to the incompressible case. However, this seems not to be robust, yet. Further investigation is needed. This is why it is solved numerically for now.
'''

# import the src file needed to solve the system of equations
import sys
import os

# Add the src directory to the sys.path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..', 'src')
sys.path.insert(0, src_path)

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
LR = 20e-8
chi = 80 # [-]

# Parameter and bcs for the electrolyte
kappa = 0
Molarity = 0.01
y_R = Molarity / nR_mol
z_A, z_C = -1.0, 1.0

K_vec = ['incompressible', 100_000, 50_000, 20_000]
Lambda2 = (k*T*epsilon0*(1+chi))/(e0**2 * nR_m * (LR)**2)
a2 = (pR)/(nR_m * k * T)

# Solver settings
number_cells = 1024
p_right = 0
phi_right = 0
rtol = 1e-4 # ! Change back to 1e-8

# phi^L domain
Volt_start = 0
Volt_end = 0.75
n_Volts = 7 # ! Change back to 101

phi_left_dimless = np.linspace(Volt_start, Volt_end, n_Volts) * e0/(k*T)

y_A, y_C, y_S, phi, p, x, n_sol = [], [], [], [], [], [], []
for index, K_ in enumerate(K_vec):
    print('-------------------------------------------------------------------')
    print('K: ', str(K_))
    print('-------------------------------------------------------------------')
    phi_inner, y_A_inner, y_C_inner, y_S_inner, p_inner,x_inner, n_inner = [], [], [], [], [], [], []
    for i, phi_bcs in enumerate(phi_left_dimless):
        print('-------------------------------------------------------------------')
        print('K: ', str(K_))
        print('phi_bcs: ', phi_bcs)
        print('-------------------------------------------------------------------')
        relax_param = 0.05
        if phi_bcs > 20:
            relax_param = 0.02
        if phi_bcs > 25:
            relax_param = 0.01
        y_A_, y_C_, phi_, p_, x_ = solve_System_2eq(phi_bcs, phi_right, p_right, z_A, z_C, y_R, y_R, K_, Lambda2, a2, number_cells, relax_param=relax_param, refinement_style='hard_log', rtol=rtol, max_iter=10_000, return_type='Vector')
        y_A_inner.append(y_A_)
        y_C_inner.append(y_C_)
        y_S_inner.append(1 - y_A_ - y_C_)
        phi_inner.append(phi_*(k*T/e0))
        p_inner.append(p_)
        n_inner.append(n(p_, K_))
        x_inner.append(x_)
    y_A.append(y_A_inner)
    y_C.append(y_C_inner)
    y_S.append(y_S_inner)
    phi.append(phi_inner)
    p.append(p_inner)
    x.append(x_inner)
    n_sol.append(n_inner)
phi_left_dim = phi_left_dimless * (k*T)/e0
    


# Charge
Q = []
for i in range(len(K_vec)):
    Q_inner = []
    for j in range(len(phi_left_dimless)):
        # ToDo: nR_m -> n
        Q_inner.append(Q_num_(y_A[i][j], y_C[i][j], n_sol[i][j], x[i][j]))
    Q.append(Q_inner)
Q = np.array(Q)

# Double layer capacity
dx_ = phi_left_dimless[1] - phi_left_dimless[0] # [1/V], uniformly distributed
C_DL = (Q[:,1:] - Q[:,:-1])/dx_ # [µAs/cm³] # ? Right unit?
C_DL = np.array(C_DL)
phi_left_center = (phi_left_dimless[1:] + phi_left_dimless[:-1])/2 # Center points for plotting C_DL



# Visualizations
# Charge
plt.figure()
[plt.plot(phi_left_dimless, Q[i], label=f'K = {K_vec[i]}') for i in range(len(K_vec))]
plt.grid()
plt.legend()
plt.xlabel('$\delta \\varphi$ [-]')
plt.ylabel('Q $[-]$')
plt.tight_layout()
plt.show()   

# Double layer capacity
plt.figure()
[plt.plot(phi_left_center, C_DL[i], label=f'K = {K_vec[i]}') for i in range(len(K_vec))]
plt.grid()
plt.legend()
plt.xlabel('$\delta \\varphi$ [-]')
plt.ylabel('$C_{dl} [-]$')
plt.tight_layout()
plt.show()

# y_alpha_L
y_A_np, y_C_np, y_S_np = np.array(y_A), np.array(y_C), np.array(y_S)
markers = ['--', '-', ':']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
plt.figure()
for i in range(len(K_vec)):
    clr = colors[i]
    plt.plot(phi_left_dimless, y_A_np[i,:,0], '--', color=clr)
    plt.plot(phi_left_dimless, y_C_np[i,:,0], '-', color=clr)
    plt.plot(phi_left_dimless, y_S_np[i,:,0], ':', color=clr)
dummy, = plt.plot(0, 0, color='grey', linestyle='--', label='$y_A$')
dummy, = plt.plot(0, 0, color='grey', linestyle='-', label='$y_C$')
dummy, = plt.plot(0, 0, color='grey', linestyle=':', label='$y_S$')
for index, K_ in enumerate(K_vec):
    dummy, = plt.plot(0, 0, color=colors[index], linestyle='-', label=f'K = {K_}')
plt.grid()
plt.legend()
plt.xlabel('$\delta \\varphi$ [-]')
plt.ylabel('$y_\\alpha^L$')
plt.tight_layout()
plt.show()

n_sol_np = np.array(n_sol)
n_A_np, n_C_np, n_S_np = y_A_np * n_sol_np, y_C_np * n_sol_np, y_S_np * n_sol_np
plt.figure()
clr = colors[0]
for i in range(len(K_vec)):
    clr = colors[i]
    plt.plot(phi_left_dimless, n_A_np[i,:,0], '--', color=clr)
    plt.plot(phi_left_dimless, n_C_np[i,:,0], '-', color=clr)
    plt.plot(phi_left_dimless, n_S_np[i,:,0], ':', color=clr)
dummy, = plt.plot(0, 0, color='grey', linestyle='--', label='$n_A$')
dummy, = plt.plot(0, 0, color='grey', linestyle='-', label='$n_C$')
dummy, = plt.plot(0, 0, color='grey', linestyle=':', label='$n_S$')
for index, K_ in enumerate(K_vec):
    dummy, = plt.plot(0, 0, color=colors[index], linestyle='-', label=f'K = {K_}')
plt.grid()
plt.legend()
plt.xlabel('$\delta \\varphi$ [-]')
plt.ylabel('$n_\\alpha^L [-]$')
plt.tight_layout()
plt.show()



# Store data
np.savez('../../Data/DoubleLayerCapacity/Compressibility.npz', Lambda2=Lambda2, a2=a2, K_vec=K_vec, kappa=kappa, Molarity=Molarity, y_R=y_R, z_A=z_A, z_C=z_C, number_cells=number_cells, p_right=p_right, phi_right=phi_right, rtol=rtol, Volt_start=Volt_start, Volt_end=Volt_end, n_Volts=n_Volts, phi_left_dim=phi_left_dim, phi_left_dimless=phi_left_dimless, y_A=y_A, y_C=y_C, y_S=y_S, phi=phi, p=p, x=x, n_sol=n_sol, Q=Q, C_DL=C_DL, phi_left_center=phi_left_center, y_A_np=y_A_np, y_C_np=y_C_np, y_S_np=y_S_np, n_sol_np=n_sol_np, n_A_np=n_A_np, n_C_np=n_C_np, n_S_np=n_S_np)
