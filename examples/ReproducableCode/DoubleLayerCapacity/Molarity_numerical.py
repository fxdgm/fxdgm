'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to analyze the influence of the molarity on the charge of the system and the double-layer capacity.
'''

# import the needed functions from the fxdgm module
from fxdgm import solve_System_4eq, Phi_pot_center, C_dl, n, Q_num_, Q_num_dim

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
nR_mol = 55 # [mol/m^3] # ? m^3 or dm^3? Should be dm^3 and then we get 55 mol/dm^3 * 1e+3 = 55 mol/m^3
nR_m = nR_mol * NA * 1/(1e-3)# [1/m^3]
pR = 1.01325 * 1e+5 # [Pa]
LR = 20e-9
chi = 80 # [-]

# Parameter and bcs for the electrolyte
Lambda2 = (k*T*epsilon0*(1+chi))/(e0**2 * nR_m * (LR)**2)
a2 = (pR)/(nR_m * k * T)
K = 'incompressible'
kappa = 0
z_A, z_C = -1.0, 1.0
phi_R = 0.0
p_R = 0

# Solver settings
number_cells = 1024
relax_param = 0.01
p_right = 0
rtol = 1e-4 # ! Change back to 1e-8
max_iter = 2500

# phi^L domain
Vol_start = -1.0
Volt_end = 1.0
n_Volts = 300

Phi_Pot_Diff_dim = np.linspace(Vol_start, Volt_end, n_Volts)
Phi_Pot_Diff_dimless = Phi_Pot_Diff_dim * e0/(k*T)

# Molarity
Molarity = np.array([0.01, 0.1, 1, 10]) # [mol/m^3]

# Solution vectors
y_A, y_C, y_S, phi, p, x = [], [], [], [], [], []

for mol in Molarity:
    y_A_R, y_C_R = mol / nR_mol, mol / nR_mol
    y_N_R = 1 - y_A_R - y_C_R
    phi_inner, y_A_inner, y_C_inner, y_S_inner, p_inner,x_inner = [], [], [], [], [], []
    for i, phi_bcs in enumerate(Phi_Pot_Diff_dimless):
        y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_bcs, phi_R, p_R, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=kappa, refinement_style='hard_log', rtol=rtol, max_iter=max_iter, return_type='Vector', relax_param=relax_param)
        y_A_inner.append(y_A_)
        y_C_inner.append(y_C_)
        y_S_inner.append(1 - y_A_ - y_C_)
        phi_inner.append(phi_)
        p_inner.append(p_)
        x_inner.append(x_)
    y_A.append(y_A_inner)
    y_C.append(y_C_inner)
    y_S.append(y_S_inner)
    phi.append(phi_inner)
    p.append(p_inner)
    x.append(x_inner)


# Charge
Q_DL_dimless_ = []
Q_DL_dim_ = []
for i in range(len(Molarity)):
    Q_inner_dimless_ = []
    Q_inner_dim_ = []
    for j in range(len(Phi_Pot_Diff_dimless)):
        Q_inner_dimless_.append(Q_num_(y_A[i][j], y_C[i][j], n(p[i][j], K), x[i][j], z_A, z_C))
        Q_inner_dim_.append(Q_num_dim(y_A[i][j], y_C[i][j], n(p[i][j], K), x[i][j], z_A, z_C, nR_m, e0, LR))
    Q_DL_dimless_.append(Q_inner_dimless_)
    Q_DL_dim_.append(Q_inner_dim_)
Q_DL_dimless_ = np.array(Q_DL_dimless_)
Q_DL_dim_ = np.array(Q_DL_dim_)


# Double Layer Capacity
C_DL_dimless_ = [C_dl(q_dl, Phi_Pot_Diff_dimless) for q_dl in Q_DL_dimless_]
C_DL_dim_ = [C_dl(q_dl, Phi_Pot_Diff_dim) for q_dl in Q_DL_dim_]




# Charge
plt.figure()
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:cyan']
color_dimless = 'tab:purple'
color_dim = 'tab:red'

# Plot dimensional data
for i, q_dl in enumerate(Q_DL_dimless_):
    plt.plot(Phi_Pot_Diff_dimless, q_dl, color=colors[i], label=f'M: {Molarity[i]}')
plt.grid()
plt.xlabel('$\delta \\varphi []$', color=color_dim)
plt.ylabel('$Q$ []$', color=color_dim)
plt.legend()
plt.tight_layout()
plt.show()


# Double Layer Capacity
fig = plt.figure()
color_dimless = 'tab:purple'
color_dim = 'tab:red'
for i, c_dl in enumerate(C_DL_dimless_):
    plt.plot(Phi_pot_center(Phi_Pot_Diff_dimless), c_dl, color=colors[i])
# ax2.grid()
plt.xlabel('$\delta \\varphi [-]$', color=color_dimless) 
plt.ylabel('$Q [-]$', color=color_dimless)       
fig.legend()
fig.tight_layout()
fig.show()

# Save the results
np.savez('../../Data/DoubleLayerCapacity/Molarity_numerical.npz', Lambda2=Lambda2, a2=a2, K=K, kappa=kappa, z_A=z_A, z_C=z_C, phi_R=phi_R, p_R=p_R, Vol_start=Vol_start, Volt_end=Volt_end, n_Volts=n_Volts, Phi_Pot_Diff_dim=Phi_Pot_Diff_dim, Phi_Pot_Diff_dimless=Phi_Pot_Diff_dimless, C_DL_dim=C_DL_dim_, C_DL_dimless=C_DL_dimless_, Q_DL_dim_=Q_DL_dim_, Q_DL_dimless_=Q_DL_dimless_, Molarity=Molarity)
