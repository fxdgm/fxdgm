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
C_DL_dimless = data_Molarity['C_DL_dimless']

data_PB = np.load('../../Data/DoubleLayerCapacity/PB.npz')
Q_DL_dim_PB_ = data_PB['Q_DL_dim_PB_']
Phi_Pot_Diff_dim_PB = data_PB['Phi_Pot_Diff_dim_PB']
Q_DL_dimless_PB_ = data_PB['Q_DL_dimless_PB_']
Phi_Pot_Diff_dimless_PB = data_PB['Phi_Pot_Diff_dimless_PB']
C_DL_dim_PB = data_PB['C_DL_dim_PB']
Phi_pot_center_array_dim_PB = data_PB['Phi_pot_center_array_dim_PB']
Phi_pot_center_array_dimless_PB = data_PB['Phi_pot_center_array_dimless_PB']
C_DL_dimless_PB = data_PB['C_DL_dimless_PB']
Molarity_PB = data_PB['Molarity']


# Plotting
# Charge
fig = plt.figure(figsize=(30, 20))
labelsize = 30
lw = 6
legend_width = 8
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:cyan']
color_PB = 'tab:grey'
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax1_dimless = fig.add_subplot(2, 2, 1, label="1")
ax1_dim = fig.add_subplot(2, 2, 1, label="2", frame_on=False)
ax2_dimless = fig.add_subplot(2, 2, 2, label="1")
ax2_dim = fig.add_subplot(2, 2, 2, label="2", frame_on=False)

# Plot dimensionless data
ax1_dimless.plot(Phi_Pot_Diff_dimless_PB, Q_DL_dimless_PB_, '--', color=color_PB, label=f'PB(M={Molarity_PB})', lw=lw, alpha=0.5)
for i, q_dl in enumerate(Q_DL_dimless_):
    ax1_dimless.plot(Phi_Pot_Diff_dimless, q_dl, color=colors[i], label=f'M: {Molarity[i]}', lw=lw)
ax1_dimless.grid()
ax1_dimless.set_xlabel('$\delta \\varphi [-]$', color=color_dimless, fontsize=labelsize)
ax1_dimless.set_ylabel('$Q [-]$', color=color_dimless, fontsize=labelsize)
ax1_dimless.tick_params(axis='x', colors=color_dimless, labelsize=labelsize)
ax1_dimless.tick_params(axis='y', colors=color_dimless, labelsize=labelsize)
ax1_dimless.set_ylim(np.min(Q_DL_dimless_)*10/9, np.max(Q_DL_dimless_)*10/9)

# Plot dimensional data
for i, q_dl in enumerate(Q_DL_dim_):
    ax1_dim.plot(Phi_Pot_Diff_dim, q_dl, color=colors[i], lw=lw)
ax1_dim.xaxis.tick_top()
ax1_dim.yaxis.tick_right()
ax1_dim.set_xlabel('$\delta \\varphi [V]$', color=color_dim, fontsize=labelsize) 
ax1_dim.set_ylabel('$Q$ [\u03bc$C/cm^3]$', color=color_dim, fontsize=labelsize)       
ax1_dim.xaxis.set_label_position('top') 
ax1_dim.yaxis.set_label_position('right') 
ax1_dim.tick_params(axis='x', colors=color_dim, labelsize=labelsize)
ax1_dim.tick_params(axis='y', colors=color_dim, labelsize=labelsize)
ax1_dim.set_ylim(np.min(Q_DL_dim_)*10/9, np.max(Q_DL_dim_)*10/9)


# Double Layer Capacity
ax2_dimless.plot(Phi_pot_center_array_dimless_PB, C_DL_dimless_PB, '--', color=color_PB, lw=lw, alpha=0.5)
for i, c_dl in enumerate(C_DL_dimless):
    ax2_dimless.plot(Phi_Pot_Diff_dimless, c_dl, color=colors[i], lw=lw)
ax2_dimless.grid()
ax2_dimless.set_xlabel('$\delta \\varphi [-]$', color=color_dimless, fontsize=labelsize)
ax2_dimless.set_ylabel('$C_{dl} [-]$', color=color_dimless, fontsize=labelsize)
ax2_dimless.tick_params(axis='x', colors=color_dimless, labelsize=labelsize)
ax2_dimless.tick_params(axis='y', colors=color_dimless, labelsize=labelsize)
ax2_dimless.set_ylim(np.min(C_DL_dimless)*(-10/9), np.max(C_DL_dimless)*10/9)

for i, c_dl in enumerate(C_DL_dim):
    ax2_dim.plot(Phi_Pot_Diff_dim, c_dl, color=colors[i], lw=lw)
ax2_dim.xaxis.tick_top()
ax2_dim.yaxis.tick_right()
ax2_dim.set_xlabel('$\delta \\varphi [V]$', color=color_dim, fontsize=labelsize) 
ax2_dim.set_ylabel('$C_{dl}$ [\u03bc$F/cm^2]$', color=color_dim, fontsize=labelsize)       
ax2_dim.xaxis.set_label_position('top') 
ax2_dim.yaxis.set_label_position('right') 
ax2_dim.tick_params(axis='x', colors=color_dim, labelsize=labelsize)
ax2_dim.tick_params(axis='y', colors=color_dim, labelsize=labelsize)
ax2_dim.set_ylim(np.min(C_DL_dim)*(-10/9), np.max(C_DL_dim)*10/9)

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, bbox_to_anchor=(0.81,1.03), ncol=6, fontsize=labelsize)
fig.tight_layout()
fig.savefig('../../Figures/DoubleLayerCapacity/DLKap_Molarity.svg', bbox_inches='tight')
fig.show()


# Not working yet
# Solvation
# Load data
data_Solvation = np.load('../../Data/DoubleLayerCapacity/Solvation.npz')

Phi_Pot_Diff_dim = data_Solvation['Phi_Pot_Diff_dim']
Phi_Pot_Diff_dim_PB = data_Solvation['Phi_Pot_Diff_dim_PB']
Q_DL_dim_ = data_Solvation['Q_DL_dim_']
Q_DL_dim_PB_ = data_Solvation['Q_DL_dim_PB_']
Q_DL_dimless_ = data_Solvation['Q_DL_dimless_']
Q_DL_dimless_PB_ = data_Solvation['Q_DL_dimless_PB_']
Phi_Pot_Diff_dimless = data_Solvation['Phi_Pot_Diff_dimless']
Phi_Pot_Diff_dimless_PB = data_Solvation['Phi_Pot_Diff_dimless_PB']
C_DL_dim = data_Solvation['C_DL_dim']
C_DL_dim_PB = data_Solvation['C_DL_dim_PB']
Phi_pot_center_array_dim = data_Solvation['Phi_pot_center_array_dim']
Phi_pot_center_array_dim_PB = data_Solvation['Phi_pot_center_array_dim_PB']
Phi_pot_center_array_dimless = data_Solvation['Phi_pot_center_array_dimless']
Phi_pot_center_array_dimless_PB = data_Solvation['Phi_pot_center_array_dimless_PB']
C_DL_dimless = data_Solvation['C_DL_dimless']
C_DL_dimless_PB = data_Solvation['C_DL_dimless_PB']
kappa_vec = data_Solvation['kappa_vec']

# Plotting
# Charge
fig = plt.figure(figsize=(30, 20))
labelsize = 30
lw = 6
legend_width = 8
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax1_dimless = fig.add_subplot(2, 2, 1, label="1")
ax1_dim = fig.add_subplot(2, 2, 1, label="2", frame_on=False)
ax2_dimless = fig.add_subplot(2, 2, 2, label="1")
ax2_dim = fig.add_subplot(2, 2, 2, label="2", frame_on=False)

# Plot dimensionless data
ax1_dimless.plot(Phi_Pot_Diff_dimless_PB, Q_DL_dimless_PB_, '--', color=colors[0], label=f'PB', lw=lw)
for i, q_dl in enumerate(Q_DL_dimless_):
    ax1_dimless.plot(Phi_Pot_Diff_dimless, q_dl, color=colors[i+1], label=f'$\kappa$: {kappa_vec[i]}', lw=lw)
ax1_dimless.grid()
ax1_dimless.set_xlabel('$\delta \\varphi [-]$', color=color_dimless, fontsize=labelsize)
ax1_dimless.set_ylabel('$Q [-]$', color=color_dimless, fontsize=labelsize)
ax1_dimless.tick_params(axis='x', colors=color_dimless, labelsize=labelsize)
ax1_dimless.tick_params(axis='y', colors=color_dimless, labelsize=labelsize)
# ax1_dimless.set_ylim(-0.025, 0.025)
ax1_dimless.set_ylim(np.min(Q_DL_dimless_)*10/9, np.max(Q_DL_dimless_)*10/9)

# Plot dimensional data
ax1_dim.plot(Phi_Pot_Diff_dim_PB, Q_DL_dim_PB_, '--', color=colors[0], lw=lw)
for i, q_dl in enumerate(Q_DL_dim_):
    ax1_dim.plot(Phi_Pot_Diff_dim, q_dl, color=colors[i+1], lw=lw)
ax1_dim.xaxis.tick_top()
ax1_dim.yaxis.tick_right()
ax1_dim.set_xlabel('$\delta \\varphi [V]$', color=color_dim, fontsize=labelsize) 
ax1_dim.set_ylabel('$Q$ [\u03bc$C/cm^3]$', color=color_dim, fontsize=labelsize)       
ax1_dim.xaxis.set_label_position('top') 
ax1_dim.yaxis.set_label_position('right') 
ax1_dim.tick_params(axis='x', colors=color_dim, labelsize=labelsize)
ax1_dim.tick_params(axis='y', colors=color_dim, labelsize=labelsize)
plt.rc('font', size=30)
ax1_dim.set_ylim(np.min(Q_DL_dim_)*10/9, np.max(Q_DL_dim_)*10/9)

# Double Layer Capacity
ax2_dimless.plot(Phi_pot_center_array_dimless_PB, C_DL_dimless_PB, '--', color=colors[0], lw=lw)
for i, c_dl in enumerate(C_DL_dimless):
    ax2_dimless.plot(Phi_pot_center_array_dimless, c_dl, color=colors[i+1], lw=lw)
ax2_dimless.grid()
ax2_dimless.set_xlabel('$\delta \\varphi [-]$', color=color_dimless, fontsize=labelsize)
ax2_dimless.set_ylabel('$C_{dl} [-]$', color=color_dimless, fontsize=labelsize)
ax2_dimless.tick_params(axis='x', colors=color_dimless, labelsize=labelsize)
ax2_dimless.tick_params(axis='y', colors=color_dimless, labelsize=labelsize)
# ax2_dimless.set_ylim(-0.0001, 0.0015)
ax2_dimless.set_ylim(np.min(C_DL_dimless)*(-10/9), np.max(C_DL_dimless)*10/9)

# ax2_dim.plot(Phi_pot_center_array_dim_PB, C_DL_dim_PB, '--', color=colors[0], lw=lw) # commented, because hard to fit the y-scale
for i, c_dl in enumerate(C_DL_dim):
    ax2_dim.plot(Phi_pot_center_array_dim, c_dl, color=colors[i+1], lw=lw)
ax2_dim.xaxis.tick_top()
ax2_dim.yaxis.tick_right()
ax2_dim.set_xlabel('$\delta \\varphi [V]$', color=color_dim, fontsize=labelsize) 
ax2_dim.set_ylabel('$C_{dl}$ [\u03bc$F/cm^2]$', color=color_dim, fontsize=labelsize)
ax2_dim.xaxis.set_label_position('top') 
ax2_dim.yaxis.set_label_position('right') 
ax2_dim.tick_params(axis='x', colors=color_dim, labelsize=labelsize)
ax2_dim.tick_params(axis='y', colors=color_dim, labelsize=labelsize)
# ax2_dim.set_ylim(-25, 600)
ax2_dim.set_ylim(np.min(C_DL_dim)*(-10/9), np.max(C_DL_dim)*10/9)

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, bbox_to_anchor=(0.76,1.05), ncol=6, fontsize=labelsize)
fig.tight_layout()
fig.savefig('../../Figures/DoubleLayerCapacity/DLKap_Solvation.svg', bbox_inches='tight')
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
C_DL_dimless = data_Lambda['C_DL_dimless']

# Plotting
# Charge
fig = plt.figure(figsize=(30, 20))
labelsize = 30
lw = 6
legend_width = 8
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax1_dimless = fig.add_subplot(2, 2, 1, label="1")
ax1_dim = fig.add_subplot(2, 2, 1, label="2", frame_on=False)
ax2_dimless = fig.add_subplot(2, 2, 2, label="1")
ax2_dim = fig.add_subplot(2, 2, 2, label="2", frame_on=False)

# Plot dimensionless data
for i, q_dl in enumerate(Q_DL_dimless_):
    ax1_dimless.plot(Phi_Pot_Diff_dimless, q_dl, color=colors[i], label=f'$\lambda^2$: {Lambda2_vec[i]}', lw=lw)
ax1_dimless.grid()
ax1_dimless.set_xlabel('$\delta \\varphi [-]$', color=color_dimless, fontsize=labelsize)
ax1_dimless.set_ylabel('$Q [-]$', color=color_dimless, fontsize=labelsize)
ax1_dimless.tick_params(axis='x', colors=color_dimless, labelsize=labelsize)
ax1_dimless.tick_params(axis='y', colors=color_dimless, labelsize=labelsize)

# Plot dimensional data
for i, q_dl in enumerate(Q_DL_dim_):
    ax1_dim.plot(Phi_Pot_Diff_dim, q_dl, color=colors[i], lw=lw)
ax1_dim.xaxis.tick_top()
ax1_dim.yaxis.tick_right()
ax1_dim.set_xlabel('$\delta \\varphi [V]$', color=color_dim, fontsize=labelsize) 
ax1_dim.set_ylabel('$Q$ [\u03bc$C/cm^3]$', color=color_dim, fontsize=labelsize)
ax1_dim.xaxis.set_label_position('top') 
ax1_dim.yaxis.set_label_position('right') 
ax1_dim.tick_params(axis='x', colors=color_dim, labelsize=labelsize)
ax1_dim.tick_params(axis='y', colors=color_dim, labelsize=labelsize)

# Double Layer Capacity
for i, c_dl in enumerate(C_DL_dimless):
    ax2_dimless.plot(Phi_Pot_Diff_dimless, c_dl, color=colors[i], lw=lw)
ax2_dimless.grid()
ax2_dimless.set_xlabel('$\delta \\varphi [-]$', color=color_dimless, fontsize=labelsize)
ax2_dimless.set_ylabel('$C_{dl} [-]$', color=color_dimless, fontsize=labelsize)
ax2_dimless.tick_params(axis='x', colors=color_dimless, labelsize=labelsize)
ax2_dimless.tick_params(axis='y', colors=color_dimless, labelsize=labelsize)

for i, c_dl in enumerate(C_DL_dim):
    ax2_dim.plot(Phi_Pot_Diff_dim, c_dl, color=colors[i], lw=lw)
ax2_dim.xaxis.tick_top()
ax2_dim.yaxis.tick_right()
ax2_dim.set_xlabel('$\delta \\varphi [V]$', color=color_dim, fontsize=labelsize) 
ax2_dim.set_ylabel('$C_{dl}$ [\u03bc$F/cm^2]$', color=color_dim, fontsize=labelsize)
ax2_dim.xaxis.set_label_position('top') 
ax2_dim.yaxis.set_label_position('right') 
ax2_dim.tick_params(axis='x', colors=color_dim, labelsize=labelsize)
ax2_dim.tick_params(axis='y', colors=color_dim, labelsize=labelsize)

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, bbox_to_anchor=(0.74,1.03), ncol=6, fontsize=labelsize)
fig.tight_layout()
fig.savefig('../../Figures/DoubleLayerCapacity/DLKap_Lambda.svg', bbox_inches='tight')
fig.show()
