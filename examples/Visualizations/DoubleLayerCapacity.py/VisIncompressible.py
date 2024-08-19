'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script visualizes the incompressible solutions for the charge of the systema and the double layer capacity.
'''

import matplotlib.pyplot as plt
import numpy as np


# Molarity

# Load data
data_Molarity = np.load('../../Data/DoubleLayerCapacity/Molarity.npz')

Q_DL_dim_ = data_Molarity['Q_DL_dim_']
Phi_Pot_Diff_dim = data_Molarity['Phi_Pot_Diff_dim']
Molarity = data_Molarity['Molarity']
Q_DL_dimless_ = data_Molarity['Q_DL_dimless_']
Phi_Pot_Diff_dimless = data_Molarity['Phi_Pot_Diff_dimless']
C_DL_dim = data_Molarity['C_DL_dim']
Phi_pot_center_array_dimless = data_Molarity['Phi_pot_center_array_dimless']
Phi_pot_center_array_dim = data_Molarity['Phi_pot_center_array_dim']
C_DL_dimless = data_Molarity['C_DL_dimless']


# Plotting
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
fig.savefig('../../Figures/DoubleLayerCapacity/Molarity_Charge.svg')
fig.show()


# Double Layer Capacity
fig = plt.figure()
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensional data
for i, c_dl in enumerate(C_DL_dim):
    ax.plot(Phi_pot_center_array_dim, c_dl, color=colors[i], label=f'M: {Molarity[i]}')
ax.grid()
ax.set_xlabel('$\delta \\varphi [nm]$', color=color_dim)
ax.set_ylabel('$C_{dl}$ [\u03bc$F/cm^2]$', color=color_dim)
ax.tick_params(axis='x', colors=color_dim)
ax.tick_params(axis='y', colors=color_dim)

for i, c_dl in enumerate(C_DL_dimless):
    ax2.plot(Phi_pot_center_array_dimless, c_dl, color=colors[i])
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
fig.savefig('../../Figures/DoubleLayerCapacity/Molarity_Capacity.svg')
fig.show()



# Solvation
# Load data
data_Solvation = np.load('../../Data/DoubleLayerCapacity/Solvation.npz')

Phi_Pot_Diff_dim = data_Solvation['Phi_Pot_Diff_dim']
Q_DL_dim_ = data_Solvation['Q_DL_dim_']
Q_DL_dimless_ = data_Solvation['Q_DL_dimless_']
Phi_Pot_Diff_dimless = data_Solvation['Phi_Pot_Diff_dimless']
C_DL_dim = data_Solvation['C_DL_dim']
Phi_pot_center_array_dim = data_Solvation['Phi_pot_center_array_dim']
Phi_pot_center_array_dimless = data_Solvation['Phi_pot_center_array_dimless']
C_DL_dimless = data_Solvation['C_DL_dimless']
kappa_vec = data_Solvation['kappa_vec']

# Plotting
# Charge
fig = plt.figure()
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:cyan']
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensional data
for i, q_dl in enumerate(Q_DL_dim_):
    ax.plot(Phi_Pot_Diff_dim, q_dl, color=colors[i], label=f'$\kappa$: {kappa_vec[i]}')
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
fig.savefig('../../Figures/DoubleLayerCapacity/Solvation_Charge.svg')
fig.show()


# Double Layer Capacity
fig = plt.figure()
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensional data
for i, c_dl in enumerate(C_DL_dim):
    ax.plot(Phi_pot_center_array_dim, c_dl, color=colors[i], label=f'$\kappa$: {kappa_vec[i]}')
ax.grid()
ax.set_xlabel('$\delta \\varphi [nm]$', color=color_dim)
ax.set_ylabel('$C_{dl}$ [\u03bc$F/cm^2]$', color=color_dim)
ax.tick_params(axis='x', colors=color_dim)
ax.tick_params(axis='y', colors=color_dim)

for i, c_dl in enumerate(C_DL_dimless):
    ax2.plot(Phi_pot_center_array_dimless, c_dl, color=colors[i])
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
fig.savefig('../../Figures/DoubleLayerCapacity/Solvation_Capacity.svg')
fig.show()



# λ
# Load data
data_Lambda = np.load('../../Data/DoubleLayerCapacity/Lambda.npz')

Q_DL_dim_ = data_Lambda['Q_DL_dim_']
Phi_Pot_Diff_dim = data_Lambda['Phi_Pot_Diff_dim']
Lambda2_vec = data_Lambda['Lambda2_vec']
Q_DL_dimless_ = data_Lambda['Q_DL_dimless_']
Phi_Pot_Diff_dimless = data_Lambda['Phi_Pot_Diff_dimless']
C_DL_dim = data_Lambda['C_DL_dim']
Phi_pot_center_array_dim = data_Lambda['Phi_pot_center_array_dim']
Phi_pot_center_array_dimless = data_Lambda['Phi_pot_center_array_dimless']
C_DL_dimless = data_Lambda['C_DL_dimless']

# Plotting
# Charge
fig = plt.figure()
colors = ['tab:blue', 'tab:orange', 'tab:green']
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensional data
for i, q_dl in enumerate(Q_DL_dim_):
    ax.plot(Phi_Pot_Diff_dim, q_dl, color=colors[i], label=f'$\lambda^2$: {Lambda2_vec[i]}')
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
fig.savefig('../../Figures/DoubleLayerCapacity/Lambda_Charge.svg')
fig.show()


# Double Layer Capacity
fig = plt.figure()
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensional data
for i, c_dl in enumerate(C_DL_dim):
    ax.plot(Phi_pot_center_array_dim, c_dl, color=colors[i], label=f'$\lambda^2$: {Lambda2_vec[i]}')
ax.grid()
ax.set_xlabel('$\delta \\varphi [nm]$', color=color_dim)
ax.set_ylabel('$C_{dl}$ [\u03bc$F/cm^2]$', color=color_dim)
ax.tick_params(axis='x', colors=color_dim)
ax.tick_params(axis='y', colors=color_dim)

for i, c_dl in enumerate(C_DL_dimless):
    ax2.plot(Phi_pot_center_array_dimless, c_dl, color=colors[i])
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
fig.savefig('../../Figures/DoubleLayerCapacity/Lambda_Capacity.svg')
fig.show()