'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to analyze the influence of the molarity on the charge of the system and the double-layer capacity.
'''

# import the needed functions from the FENICSxDGM module
from FENICSxDGM import Q_DL_dimless_ana, Q_DL_dim_ana, C_DL_dimless_ana, C_DL_dim_ana

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

# phi^L domain
Vol_start = -1.0
Volt_end = 1.0
n_Volts = 5_000

Phi_Pot_Diff_dim = np.linspace(Vol_start, Volt_end, n_Volts)
Phi_Pot_Diff_dimless = Phi_Pot_Diff_dim * e0/(k*T)




# Molarity
Molarity = np.array([0.01, 0.1, 1, 10]) # [mol/m^3]

Q_DL_dim_ = []
Q_DL_dimless_ = []
for mol in Molarity:
    y_A_R, y_C_R = mol / nR_mol, mol / nR_mol
    y_N_R = 1 - y_A_R - y_C_R
    Q_DL_dimless_.append(Q_DL_dimless_ana(y_A_R, y_C_R, y_N_R, z_A, z_C, Phi_Pot_Diff_dimless, phi_R, p_R, K, Lambda2, a2, kappa))
    Q_DL_dim_.append(Q_DL_dim_ana(y_A_R, y_C_R, y_N_R, z_A, z_C, Phi_Pot_Diff_dimless, phi_R, p_R, K, Lambda2, a2, nR_m, e0, LR, kappa))
    
# Double layer capacity
C_DL_dim_ = []
C_DL_dimless_ = []
for mol in Molarity:
    y_A_R, y_C_R = mol / nR_mol, mol / nR_mol
    y_N_R = 1 - y_A_R - y_C_R
    C_DL_dim_.append(C_DL_dim_ana(y_A_R, y_C_R, 1-y_A_R-y_C_R, z_A, z_C, Phi_Pot_Diff_dimless, phi_R, p_R, K, Lambda2, a2, nR_m, e0, LR, k, T, kappa))
    C_DL_dimless_.append(C_DL_dimless_ana(y_A_R, y_C_R, 1-y_A_R-y_C_R, z_A, z_C, Phi_Pot_Diff_dimless, phi_R, p_R, K, Lambda2, a2, kappa))




# Charge
fig = plt.figure()
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:cyan']
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensional data
for i, q_dl in enumerate(Q_DL_dim_):
    ax.plot(Phi_Pot_Diff_dim, q_dl, color=colors[i], label=f'M: {Molarity[i]}')
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
    ax.plot(Phi_Pot_Diff_dim, c_dl, color=colors[i], label=f'M: {Molarity[i]}')
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

# Save the results
np.savez('../../Data/DoubleLayerCapacity/Molarity.npz', Lambda2=Lambda2, a2=a2, K=K, kappa=kappa, z_A=z_A, z_C=z_C, phi_R=phi_R, p_R=p_R, Vol_start=Vol_start, Volt_end=Volt_end, n_Volts=n_Volts, Phi_Pot_Diff_dim=Phi_Pot_Diff_dim, Phi_Pot_Diff_dimless=Phi_Pot_Diff_dimless, C_DL_dim=C_DL_dim_, C_DL_dimless=C_DL_dimless_, Q_DL_dim_=Q_DL_dim_, Q_DL_dimless_=Q_DL_dimless_, Molarity=Molarity)
