'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script visualizes the incompressible solutions for the charge of the systema and the double layer capacity.
'''

import matplotlib.pyplot as plt
import numpy as np


# Molarity

# Load data
data = np.load('../../Data/DoubleLayerCapacity/DLKap_Compressibility.npz')

Q_DL_dimless_ = data['Q_DL_dimless_']
Q_DL_dim_ = data['Q_DL_dim_']
C_DL_dim = data['C_DL_dim']
C_DL_dimless = data['C_DL_dimless']
# y_A = data['y_A']
# y_C = data['y_C']
# y_S = data['y_S']
Phi_Pot_Diff_dim = data['Phi_Pot_Diff_dim']
Phi_Pot_Diff_dimless = data['Phi_Pot_Diff_dimless']
Phi_pot_center_array_dim = data['Phi_pot_center_array_dim']
Phi_pot_center_array_dimless = data['Phi_pot_center_array_dimless']
# n_sol = data['n_sol']
K_vec = data['K_vec']



# Plotting
# Charge
fig = plt.figure()
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensionless data
for i, q_dl in enumerate(Q_DL_dimless_):
    ax.plot(Phi_Pot_Diff_dimless, q_dl, color=colors[i], label=f'K: {K_vec[i]}')
ax.grid()
ax.set_xlabel('$\delta \\varphi [-]$', color=color_dimless)
ax.set_ylabel('$Q [-]$', color=color_dimless)
ax.tick_params(axis='x', colors=color_dimless)
ax.tick_params(axis='y', colors=color_dimless)

# Plot dimensional data
for i, q_dl in enumerate(Q_DL_dim_):
    ax2.plot(Phi_Pot_Diff_dim, q_dl, color=colors[i])
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('$\delta \\varphi [nm]$', color=color_dim) 
ax2.set_ylabel('$Q$ [\u03bc$F/cm^3]$', color=color_dim)       
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 
ax2.tick_params(axis='x', colors=color_dim)
ax2.tick_params(axis='y', colors=color_dim)

fig.legend()
fig.tight_layout()
fig.savefig('../../Figures/DoubleLayerCapacity/Compressibility_Charge.svg')
fig.show()


# Double Layer Capacity
fig = plt.figure()
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensional data
for i, c_dl in enumerate(C_DL_dimless):
    ax.plot(Phi_pot_center_array_dimless, c_dl, color=colors[i], label=f'K: {K_vec[i]}')
ax.grid()
ax.set_xlabel('$\delta \\varphi [-]$', color=color_dimless)
ax.set_ylabel('$C_{dl} [-]$', color=color_dimless)
ax.tick_params(axis='x', colors=color_dimless)
ax.tick_params(axis='y', colors=color_dimless)

for i, c_dl in enumerate(C_DL_dim):
    ax2.plot(Phi_pot_center_array_dim, c_dl, color=colors[i])
# ax2.grid()
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('$\delta \\varphi [nm]$', color=color_dim) 
ax2.set_ylabel('$C_{dl}$ [\u03bc$F/cm^2]$', color=color_dim)       
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 
ax2.tick_params(axis='x', colors=color_dim)
ax2.tick_params(axis='y', colors=color_dim)

fig.legend()
fig.tight_layout()
fig.savefig('../../Figures/DoubleLayerCapacity/Compressibility_Capacity.svg')
fig.show()

# # Charge
# plt.figure()
# [plt.plot(phi_left, Q[i], label=f'K = {K_vec[i]}') for i in range(len(K_vec))]
# plt.grid()
# plt.legend()
# plt.xlabel('$\delta \\varphi$ [-]')
# plt.ylabel('Q $[-]$')
# plt.tight_layout()
# plt.show()   

# # Double layer capacity
# plt.figure()
# [plt.plot(phi_left_center, C_DL[i], label=f'K = {K_vec[i]}') for i in range(len(K_vec))]
# plt.grid()
# plt.legend()
# plt.xlabel('$\delta \\varphi$ [-]')
# plt.ylabel('$C_{dl} [-]$')
# plt.tight_layout()
# plt.show()

# # y_alpha_L
# y_A_np, y_C_np, y_S_np = np.array(y_A), np.array(y_C), np.array(y_S)
# markers = ['--', '-', ':']
# colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

# n_sol_np = np.array(n_sol)
# n_A_np, n_C_np, n_S_np = y_A_np * n_sol_np, y_C_np * n_sol_np, y_S_np * n_sol_np
# plt.figure()
# clr = colors[0]
# for i in range(len(K_vec)):
#     clr = colors[i]
#     plt.plot(phi_left, n_A_np[i,:,0], '--', color=clr)
#     plt.plot(phi_left, n_C_np[i,:,0], '-', color=clr)
#     plt.plot(phi_left, n_S_np[i,:,0], ':', color=clr)
# dummy, = plt.plot(0, 0, color='grey', linestyle='--', label='$n_A$')
# dummy, = plt.plot(0, 0, color='grey', linestyle='-', label='$n_C$')
# dummy, = plt.plot(0, 0, color='grey', linestyle=':', label='$n_S$')
# for index, K_ in enumerate(K_vec):
#     dummy, = plt.plot(0, 0, color=colors[index], linestyle='-', label=f'K = {K_}')
# plt.grid()
# plt.legend()
# plt.xlabel('$\delta \\varphi$ [-]')
# plt.ylabel('$n_\\alpha^L [-]$')
# plt.tight_layout()
# plt.show()