'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to analyze the influence of the molarity on the charge of the system and the double-layer capacity.
'''

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
nR_mol = 55
nR_m = nR_mol * NA * 1/(1e-3)# [1/m^3]
pR = 1.01325 * 1e+5 # [Pa]
LR = 20e-9
chi = 80 # [-]

# Parameter and bcs for the electrolyte
Lambda2 = (k*T*epsilon0*(1+chi))/(e0**2 * nR_m * (LR)**2)
a2 = (pR)/(nR_m * k * T)
K = 'incompressible'
Molarity = 0.01
y_R = Molarity / nR_mol
z_A, z_C = -1.0, 1.0
phi_R = 0.0
p_R = 0

# Solver settings
number_cells = 1024
relax_param = 0.3
rtol = 1e-2 # ! 1e-8
refinement_style = 'hard_log'
max_iter = 10_000
return_type = 'Vector'

# phi^L domain
Volt_start = -0.35
Volt_end = 0.35
n_Volts = 25 # ! 75

Phi_Pot_Diff_dim_PB = np.linspace(Volt_start, Volt_end, n_Volts)
Phi_Pot_Diff_dimless_PB = Phi_Pot_Diff_dim_PB * e0/(k*T)

phi_PB, y_A_PB, y_C_PB, y_S_PB, p_PB,x_PB = [], [], [], [], [], []
for i, phi_bcs in enumerate(Phi_Pot_Diff_dimless_PB):
    y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_bcs, phi_R, p_R, z_A, z_C, y_R, y_R, K, Lambda2, a2, number_cells, solvation=0, PoissonBoltzmann=True, refinement_style='hard_log', rtol=rtol, max_iter=max_iter, relax_param=0.01, return_type=return_type)
    y_A_PB.append(y_A_)
    y_C_PB.append(y_C_)
    y_S_PB.append(1 - y_A_ - y_C_)
    phi_PB.append(phi_)
    p_PB.append(p_)
    x_PB.append(x_)


# Charge
Q_DL_dimless_PB_ = []
Q_DL_dim_PB_ = []
for j in range(len(Phi_Pot_Diff_dimless_PB)):
    Q_DL_dimless_PB_.append(Q_num_(y_A_PB[j], y_C_PB[j], n(p_PB[j], K), x_PB[j], z_A, z_C))
    Q_DL_dim_PB_.append(Q_num_dim(y_A_PB[j], y_C_PB[j], n(p_PB[j], K), x_PB[j], z_A, z_C, nR_m, e0, LR))
Q_DL_dimless_PB_ = np.array(Q_DL_dimless_PB_)
Q_DL_dim_PB_ = np.array(Q_DL_dim_PB_)

# Double-layer capacity
C_DL_dimless_PB = C_dl(Q_DL_dimless_PB_, Phi_Pot_Diff_dimless_PB)
C_DL_dim_PB = C_dl(Q_DL_dim_PB_, Phi_Pot_Diff_dim_PB)

Phi_pot_center_array_dimless_PB = Phi_pot_center(Phi_Pot_Diff_dimless_PB)
Phi_pot_center_array_dim_PB = Phi_pot_center(Phi_Pot_Diff_dim_PB)

# Plotting
# Charge
fig, axs = plt.subplots()
axs.plot(Phi_Pot_Diff_dim_PB, Q_DL_dim_PB_)
axs.grid()
axs.set_xlabel('$\delta \\varphi [nm]$')
axs.set_ylabel('$Q$ [\u03bc$F/cm^3]$')
fig.tight_layout()
fig.show()

# Double-layer capacity
fig, axs = plt.subplots()
axs.plot(Phi_pot_center_array_dimless_PB, C_DL_dimless_PB)
axs.grid()
axs.set_xlabel('$\delta \\varphi [-]$') 
axs.set_ylabel('$Q [-]$')
fig.tight_layout()
fig.show()

# Store results
np.savez('../../Data/DoubleLayerCapacity/PB.npz', Lambda2=Lambda2, a2=a2, K=K, Molarity=Molarity, y_R=y_R, z_A=z_A, z_C=z_C, phi_R=phi_R, p_R=p_R, number_cells=number_cells, relax_param=relax_param, rtol=rtol, refinement_style=refinement_style, max_iter=max_iter, return_type=return_type, Volt_start=Volt_start, Volt_end=Volt_end, n_Volts=n_Volts, Phi_Pot_Diff_dim_PB=Phi_Pot_Diff_dim_PB, Phi_Pot_Diff_dimless_PB=Phi_Pot_Diff_dimless_PB, Q_DL_dimless_PB_=Q_DL_dimless_PB_, Q_DL_dim_PB_=Q_DL_dim_PB_, C_DL_dimless_PB=C_DL_dimless_PB, C_DL_dim_PB=C_DL_dim_PB, Phi_pot_center_array_dimless_PB=Phi_pot_center_array_dimless_PB, Phi_pot_center_array_dim_PB=Phi_pot_center_array_dim_PB)