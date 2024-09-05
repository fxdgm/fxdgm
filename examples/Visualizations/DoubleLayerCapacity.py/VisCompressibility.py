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
Phi_Pot_Diff_dim = data['Phi_Pot_Diff_dim']
Phi_Pot_Diff_dimless = data['Phi_Pot_Diff_dimless']
K_vec = data['K_vec']



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
# Extra label for incompressible
ax1_dimless.plot(Phi_Pot_Diff_dimless, Q_DL_dimless_[0], color=colors[0], label='incompressible', lw=lw)
for i, q_dl in enumerate(Q_DL_dimless_[1:]):
    ax1_dimless.plot(Phi_Pot_Diff_dimless, q_dl, color=colors[i+1], label=f'K: {K_vec[i+1]}', lw=lw)
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
# Plot dimensional data
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
fig.legend(lines, labels, bbox_to_anchor=(0.86,1.05), ncol=6, fontsize=labelsize)
fig.tight_layout()
fig.savefig('../../Figures/DoubleLayerCapacity/DLKap_Compressibility.svg', bbox_inches='tight')
fig.show()
