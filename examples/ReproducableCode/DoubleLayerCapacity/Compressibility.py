'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to analyze the influence of the compressibility on the charge of the system and the double-layer capacity.

# ! Efforts were made to simplify this similar to the incompressible case. However, this seems not to be robust, yet. Further investigation is needed. This is why it is solved numerically for now.
'''

# import the needed functions from the fxdgm module
from fxdgm import Q_DL_dimless_ana, Q_DL_dim_ana, C_DL_dimless_ana, C_DL_dim_ana

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
z_A, z_C = -1.0, 1.0

Lambda2 = (k*T*epsilon0*(1+chi))/(e0**2 * nR_m * (LR)**2)
a2 = (pR)/(nR_m * k * T)

# Solver settings
p_R = 0
phi_R = 0

# phi^L domain
Volt_start = -1.0
Volt_end = 1.0
# Volt_start = -1.0
# Volt_end = 1.0
n_Volts = 10_001

Phi_Pot_Diff_dim = np.linspace(Volt_start, Volt_end, n_Volts) 
Phi_Pot_Diff_dimless = Phi_Pot_Diff_dim * e0/(k*T)

# K
K_vec = ['incompressible', 50_000, 40_000, 30_000, 20_000]

# Charge
Q_DL_dim_ = []
Q_DL_dimless_ = []
for K in K_vec:
    y_A_R, y_C_R = Molarity / nR_mol, Molarity / nR_mol
    y_N_R = 1 - y_A_R - y_C_R
    Q_DL_dimless_.append(Q_DL_dimless_ana(y_A_R, y_C_R, y_N_R, z_A, z_C, Phi_Pot_Diff_dimless, phi_R, p_R, K, Lambda2, a2, kappa))
    Q_DL_dim_.append(Q_DL_dim_ana(y_A_R, y_C_R, y_N_R, z_A, z_C, Phi_Pot_Diff_dimless, phi_R, p_R, K, Lambda2, a2, nR_m, e0, LR, kappa))

# Double layer capacity
C_DL_dim_ = []
C_DL_dimless_ = []
for K in K_vec:
    C_DL_dim_.append(C_DL_dim_ana(y_A_R, y_C_R, 1-y_A_R-y_C_R, z_A, z_C, Phi_Pot_Diff_dimless, phi_R, p_R, K, Lambda2, a2, nR_m, e0, LR, k, T, kappa))
    C_DL_dimless_.append(C_DL_dimless_ana(y_A_R, y_C_R, 1-y_A_R-y_C_R, z_A, z_C, Phi_Pot_Diff_dimless, phi_R, p_R, K, Lambda2, a2, kappa))


# Plotting
# Charge
fig = plt.figure()
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensional data
for i, q_dl in enumerate(Q_DL_dim_):
    ax.plot(Phi_Pot_Diff_dim, q_dl, color=colors[i], label=f'$K$: {K_vec[i]}')
ax.grid()
ax.set_xlabel('$\delta \\varphi [nm]$', color=color_dim)
ax.set_ylabel('$Q$ [\u03bc$F/cm^3]$', color=color_dim)
ax.tick_params(axis='x', colors=color_dim)
ax.tick_params(axis='y', colors=color_dim)

for i, q_dl in enumerate(Q_DL_dimless_):
    ax2.plot(Phi_Pot_Diff_dimless, q_dl, color=colors[i])
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('$\delta \\varphi [-]$', color=color_dimless) 
ax2.set_ylabel('$Q [-]$', color=color_dimless)       
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 
ax2.tick_params(axis='x', colors=color_dimless)
ax2.tick_params(axis='y', colors=color_dimless)

fig.legend()
fig.tight_layout()
fig.show()


# Double Layer Capacity
fig = plt.figure()
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensional data
for i, c_dl in enumerate(C_DL_dim_):
    ax.plot(Phi_Pot_Diff_dim, c_dl, color=colors[i], label=f'$K$: {K_vec[i]}')
ax.grid()
ax.set_xlabel('$\delta \\varphi [nm]$', color=color_dim)
ax.set_ylabel('$C_{dl}$ [\u03bc$F/cm^2]$', color=color_dim)
ax.tick_params(axis='x', colors=color_dim)
ax.tick_params(axis='y', colors=color_dim)

for i, c_dl in enumerate(C_DL_dimless_):
    ax2.plot(Phi_Pot_Diff_dimless, c_dl, color=colors[i])
# ax2.grid()
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('$\delta \\varphi [-]$', color=color_dimless) 
ax2.set_ylabel('$Q [-]$', color=color_dimless)       
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 
ax2.tick_params(axis='x', colors=color_dimless)
ax2.tick_params(axis='y', colors=color_dimless)

fig.legend()
fig.tight_layout()
fig.show()


# Store data
np.savez('../../Data/DoubleLayerCapacity/DLKap_Compressibility.npz', Lambda2=Lambda2, a2=a2, K_vec=K_vec, kappa=kappa, Molarity=Molarity, y_A_R=y_A_R, y_C_R=y_C_R, z_A=z_A, z_C=z_C, p_R=p_R, phi_R=phi_R, Volt_start=Volt_start, Volt_end=Volt_end, n_Volts=n_Volts, Phi_Pot_Diff_dimless=Phi_Pot_Diff_dimless, Phi_Pot_Diff_dim=Phi_Pot_Diff_dim, Q_DL_dimless_=Q_DL_dimless_, Q_DL_dim_ =Q_DL_dim_, C_DL_dimless=C_DL_dimless_, C_DL_dim=C_DL_dim_)
