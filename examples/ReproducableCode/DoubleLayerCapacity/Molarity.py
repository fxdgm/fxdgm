'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to analyze the influence of the molarity on the charge of the system and the double-layer capacity.
'''

# import the src file needed to solve the system of equations
import sys
import os

# Add the src directory to the sys.path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'src')
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
T = 293.15 # [K]
epsilon0 = 8.85e-12 #[F/m]
F = 9.65e+4 # [As/mol]
NA = 6.022e+23 # [1/mol] - Avogadro constant
nR_mol = 55
nR_m = nR_mol * NA * 1/(1e-3)# [1/m^3]
pR = 1.01325 * 1e+5 # [Pa]
LR = 20e-8
chi = 80 # [-]

# Parameter and bcs for the electrolyte
Lambda2 = (k*T*epsilon0*(1+chi))/(e0**2 * nR_m * (LR)**2)
a2 = (pR)/(nR_m * k * T)
K = 'incompressible'
kappa = 0
Molarity = 0.01
y_R = Molarity / nR_mol
z_A, z_C = -1.0, 1.0
phi_R = 0.0
p_R = 0

# Solver settings
number_cells = 1024
relax_param = 0.03
p_right = 0

# phi^L domain
Vol_start = -1.0
Volt_end = 1.0
n_Volts = 5_000

Phi_Pot_Diff_dim = np.linspace(Vol_start, Volt_end, n_Volts)
Phi_Pot_Diff_dimless = Phi_Pot_Diff_dim * e0/(k*T)




# Molarity
Molarity = np.array([0.01, 0.1, 1])

Q_DL_dim_ = []
Q_DL_dimless_ = []
for mol in Molarity:
    y_A_R, y_C_R = mol / nR_mol, mol / nR_mol
    y_N_R = 1 - y_A_R - y_C_R
    Q_DL_dimless_.append(Q_DL_dimless_ana(y_A_R, y_C_R, y_N_R, z_A, z_C, Phi_Pot_Diff_dimless, phi_R, p_R, Lambda2, a2, kappa))
    Q_DL_dim_.append(Q_DL_dim_ana(y_A_R, y_C_R, y_N_R, z_A, z_C, Phi_Pot_Diff_dimless, phi_R, p_R, Lambda2, a2, nR_m, e0, LR, kappa))
    
C_DL_dim = [C_dl(q_dl, Phi_Pot_Diff_dim) for q_dl in Q_DL_dim_]
C_DL_dimless = [C_dl(q_dl, Phi_Pot_Diff_dimless) for q_dl in Q_DL_dimless_]



# fig, axs = plt.subplots(ncols=2, figsize=(10, 5))
# ax1 = axs[0]
# ax2 = axs[1]

# # Plot the first set of data on the primary y-axis
# colors = ['tab:blue', 'tab:orange', 'tab:green']
# ax1.set_xlabel('Phi_Pot_Diff')
# ax1.set_ylabel('$Q$ [\u03bc$F/cm^3]$')#, color=color)
# for i, q_dl in enumerate(Q_DL_dim_):
#     ax1.plot(Phi_Pot_Diff_dim, q_dl, color=colors[i], label=f'Molarity: {Molarity[i]}')
# ax1.tick_params(axis='y')#, labelcolor=color)
# ax1.grid()

# # Create a secondary y-axis
# ax1_twin = ax1.twinx()
# ax1_twin.set_ylabel('$Q [-]$')#, color=color)
# for i, q_dl in enumerate(Q_DL_dimless_):
#     ax1_twin.plot(Phi_Pot_Diff_dimless, q_dl, color=colors[i])
# ax1_twin.tick_params(axis='y')#, labelcolor=color2)
# ax1_twin.grid()

# ax2.set_xlabel('Phi_Pot_Diff')
# ax2.set_ylabel('$C_{dl}$ [\u03bc$F/cm^2]$')#, color=color)
# for i, c_dl in enumerate(C_DL_dim):
#     ax2.plot(Phi_pot_center(Phi_Pot_Diff_dim), c_dl, color=colors[i])
# ax2.tick_params(axis='y')#, labelcolor=color)
# ax2.grid()

# # Create a secondary y-axis
# ax2_twin = ax2.twinx()
# ax2_twin.set_ylabel('$C_{dl} [-]$')#, color=color)
# for i, c_dl in enumerate(C_DL_dimless):
#     ax2_twin.plot(Phi_pot_center(Phi_Pot_Diff_dimless), c_dl, color=colors[i])
# ax2_twin.tick_params(axis='y')#, labelcolor=color2)
# ax2_twin.grid()


# fig.tight_layout()  # Adjust layout to prevent overlap
# fig.legend()
# fig.show()

# # plt.figure()
# # [plt.plot(Phi_pot_center(Phi_Pot_Diff_dim), c_dl) for c_dl in C_DL_dim]
# # plt.show()

# # plt.figure()
# # [plt.plot(Phi_pot_center(Phi_Pot_Diff_dimless), c_dl) for c_dl in C_DL_dimless]
# # plt.show()


# Charge
fig = plt.figure()
colors = ['tab:blue', 'tab:orange', 'tab:green']
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
for i, c_dl in enumerate(C_DL_dim):
    ax.plot(Phi_pot_center(Phi_Pot_Diff_dim), c_dl, color=colors[i], label=f'M: {Molarity[i]}')
ax.grid()
ax.set_xlabel('$\delta \\varphi [nm]$', color=color_dim)
ax.set_ylabel('$C_{dl}$ [\u03bc$F/cm^2]$', color=color_dim)
ax.tick_params(axis='x', colors=color_dim)
ax.tick_params(axis='y', colors=color_dim)

for i, c_dl in enumerate(C_DL_dimless):
    ax2.plot(Phi_pot_center(Phi_Pot_Diff_dimless), c_dl, color=colors[i])
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