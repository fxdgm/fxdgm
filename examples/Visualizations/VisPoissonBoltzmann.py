'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import numpy as np


# Comparison for different delta phi
# Load data
df_10 = np.load('../Data/PoissonBoltzmann_10.npz')

x_DGM_10 = df_10['x_DGM_10']
phi_DGM_10 = df_10['phi_DGM_10']
y_A_DGM_10 = df_10['y_A_DGM_10']
y_C_DGM_10 = df_10['y_C_DGM_10']
y_S_DGM_10 = df_10['y_S_DGM_10']
p_DGM_10 = df_10['p_DGM_10']
x_PB_10 = df_10['x_PB_10']
phi_PB_10 = df_10['phi_PB_10']
y_A_PB_10 = df_10['y_A_PB_10']
y_C_PB_10 = df_10['y_C_PB_10']
y_S_PB_10 = df_10['y_S_PB_10']
p_PB_10 = df_10['p_PB_10']

df_1 = np.load('../Data/PoissonBoltzmann_1.npz')

x_DGM_1 = df_1['x_DGM_01']
phi_DGM_1 = df_1['phi_DGM_01']
y_A_DGM_1 = df_1['y_A_DGM_01']
y_C_DGM_1 = df_1['y_C_DGM_01']
y_S_DGM_1 = df_1['y_S_DGM_01']
p_DGM_1 = df_1['p_DGM_01']
x_PB_1 = df_1['x_PB_01']
phi_PB_1 = df_1['phi_PB_01']
y_A_PB_1 = df_1['y_A_PB_01']
y_C_PB_1 = df_1['y_C_PB_01']
y_S_PB_1 = df_1['y_S_PB_01']
p_PB_1 = df_1['p_PB_01']

xlim = 0.05


# Visualize the results
fig, axs = plt.subplots(2, 2, figsize=(30, 20))
labelsize = 40
lw = 4
legend_width = 8
markers = ['-', '--', '-.', ':']
colors = ['tab:blue', 'tab:orange', 'tab:green']

axs[0,1].set_title('$\delta \\varphi = 1$', fontsize=labelsize)
axs[0,1].plot(x_DGM_1, y_A_DGM_1, markers[0], color=colors[0], lw=lw)
axs[0,1].plot(x_PB_1, y_A_PB_1, markers[1], color=colors[0], lw=lw)
axs[0,1].plot(x_DGM_1, y_C_DGM_1, markers[0], color=colors[1], lw=lw)
axs[0,1].plot(x_PB_1, y_C_PB_1, markers[1], color=colors[1], lw=lw)
axs[0,1].plot(x_DGM_1, y_S_DGM_1, markers[0], color=colors[2], lw=lw)
axs[0,1].plot(x_PB_1, y_S_PB_1, markers[1], color=colors[2], lw=lw)
axs[0,1].set_xlim(0,xlim)
axs[0,1].set_ylim(-0.02, 1.02)
axs[0,1].grid()
axs[0,1].set_xlabel('x [-]', fontsize=labelsize)
axs[0,1].set_ylabel('$y_\\alpha$ [-]', fontsize=labelsize)
axs[0,1].tick_params(axis='both', labelsize=labelsize)


axs[1,1].set_title('$\delta \\varphi = 10$', fontsize=labelsize)
axs[1,1].plot(x_DGM_10, y_A_DGM_10, markers[0], color=colors[0], lw=lw)
axs[1,1].plot(x_PB_10, y_A_PB_10, markers[1], color=colors[0], lw=lw)
axs[1,1].plot(x_DGM_10, y_C_DGM_10, markers[0], color=colors[1], lw=lw)
axs[1,1].plot(x_PB_10, y_C_PB_10, markers[1], color=colors[1], lw=lw)
axs[1,1].plot(x_DGM_10, y_S_DGM_10, markers[0], color=colors[2], lw=lw)
axs[1,1].plot(x_PB_10, y_S_PB_10, markers[1], color=colors[2], lw=lw)
dummy, = axs[1,1].plot(10, 0.1, color=colors[0], linestyle='-', label='$y_A$')
dummy, = axs[1,1].plot(10, 0.1, color=colors[1], linestyle='-', label='$y_C$')
dummy, = axs[1,1].plot(10, 0.1, color=colors[2], linestyle='-', label='$y_S$')
dummy, = axs[1,1].plot(10, 0.1, color='grey', linestyle=markers[0], label='DGM')
dummy, = axs[1,1].plot(10, 0.1, color='grey', linestyle=markers[1], label='PB')
axs[1,1].set_xlim(0,xlim)
axs[1,1].set_ylim(-0.02, 1.02)
axs[1,1].grid()
axs[1,1].set_xlabel('x [-]', fontsize=labelsize)
axs[1,1].set_ylabel('$y_\\alpha$ [-]', fontsize=labelsize)
axs[1,1].tick_params(axis='both', labelsize=labelsize)



# Plot phi
color_phi = 'tab:blue'
color_p = 'tab:red'
ax1 = axs[1,0]
ax1.set_title('$\delta \\varphi = 10$', fontsize=labelsize)
ax1.tick_params(axis='y')#, labelcolor=color)
ax1.plot(x_DGM_10, phi_DGM_10, markers[0], color=color_phi, lw=lw)
ax1.plot(x_PB_10, phi_PB_10, markers[1], color=color_phi, lw=lw)
ax1.grid()
ax1.set_ylim(0.0, np.max(phi_DGM_10))
ax1.set_xlabel('$x$ [-]', fontsize=labelsize)
ax1.set_ylabel('$\\varphi$ [-]', fontsize=labelsize, color=color_phi)
ax1.set_xlim(0,xlim)
ax1.tick_params(axis='x', labelsize=labelsize)
ax1.tick_params(axis='y', labelcolor=color_phi, labelsize=labelsize)
ax1.legend()

# Create a second y-axis
ax2 = ax1.twinx()
# Plot p
color = 'tab:red'
ax2.set_ylabel('$p$ [-]', color=color)
ax2.plot(x_DGM_10, p_DGM_10, markers[0], color=color_p, lw=lw)
ax2.plot(x_PB_10, p_PB_10, markers[1], color=color_p, lw=lw)
ax2.grid()
ax2.set_ylim(0.0, np.max(p_DGM_10))
ax2.set_xlim(0,xlim)
ax2.set_xlabel('$x$ [-]', fontsize=labelsize)
ax2.set_ylabel('$p$ [-]', fontsize=labelsize)
ax2.legend()
ax2.tick_params(axis='x', labelsize=labelsize)
ax2.tick_params(axis='y', labelcolor=color_p, labelsize=labelsize)

# Plot phi
color_phi = 'tab:blue'
color_p = 'tab:red'
ax1 = axs[0,0]
ax1.set_title('$\delta \\varphi = 1$', fontsize=labelsize)
ax1.tick_params(axis='y')#, labelcolor=color)
ax1.plot(x_DGM_1, phi_DGM_1, markers[0], color=color_phi, lw=lw)
ax1.plot(x_PB_1, phi_PB_1, markers[1], color=color_phi, lw=lw)
ax1.grid()
ax1.set_ylim(0.0, np.max(phi_DGM_1))
ax1.set_xlabel('$x$ [-]', fontsize=labelsize)
ax1.set_ylabel('$\\varphi$ [-]', fontsize=labelsize, color=color_phi)
ax1.set_xlim(0,xlim)
ax1.tick_params(axis='x', labelsize=labelsize)
ax1.tick_params(axis='y', labelcolor=color_phi, labelsize=labelsize)
ax1.legend()

# Create a second y-axis
ax2 = ax1.twinx()
# Plot p
color = 'tab:red'
ax2.set_ylabel('$p$ [-]', color=color)
ax2.plot(x_DGM_1, p_DGM_1, markers[0], color=color_p, lw=lw)
ax2.plot(x_PB_1, p_PB_1, markers[1], color=color_p, lw=lw)
ax2.grid()
ax2.set_ylim(0.0, np.max(p_DGM_1))
ax2.set_xlim(0,xlim)
ax2.set_xlabel('$x$ [-]', fontsize=labelsize)
ax2.set_ylabel('$p$ [-]', fontsize=labelsize)
ax2.legend()
ax2.tick_params(axis='x', labelsize=labelsize)
ax2.tick_params(axis='y', labelcolor=color_p, labelsize=labelsize)

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

# Finally, the legend (that maybe you'll customize differently)
lgnd = fig.legend(lines, labels, bbox_to_anchor=(0.8    ,1.08), ncol=6, fontsize=labelsize)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)
fig.tight_layout()

fig.tight_layout()
# fig.savefig('../Figures/PoissonBoltzmann_Comparsion.svg', bbox_inches='tight')
fig.show()



# Convergence towards the DGM solution
data_convergence = np.load('../Data/PoissonBoltzmann_Convergence.npz')

phi_left_vec = data_convergence['phi_left_vec']
y_A_error_L2 = data_convergence['y_A_error_L2']
y_C_error_L2 = data_convergence['y_C_error_L2']
y_S_error_L2 = data_convergence['y_S_error_L2']
phi_error_L2 = data_convergence['phi_error_L2']
p_error_L2 = data_convergence['p_error_L2']
y_A_error_inf = data_convergence['y_A_error_inf']
y_C_error_inf = data_convergence['y_C_error_inf']
y_S_error_inf = data_convergence['y_S_error_inf']
phi_error_inf = data_convergence['phi_error_inf']
p_error_inf = data_convergence['p_error_inf']


# Visualize the results
fig, axs = plt.subplots(ncols=2, figsize=(30, 12))
labelsize = 40
lw = 6
ms=20
# Log-log plot of L2-error
axs[0].plot(phi_left_vec, y_A_error_L2, 'o-', label='$y_A$', lw=lw, ms=ms)
axs[0].plot(phi_left_vec, y_C_error_L2, 'o-', label='$y_C$', lw=lw, ms=ms)
axs[0].plot(phi_left_vec, y_S_error_L2, 'o-', label='$y_S$', lw=lw, ms=ms)
axs[0].set_yscale('log')
axs[0].set_xlabel('$\delta \\varphi [-]$', fontsize=labelsize)
axs[0].set_ylabel('log($L_2$) [-]', fontsize=labelsize)
axs[0].tick_params(axis='both', labelsize=labelsize)
axs[0].grid()

# Log-log plot of infinity error
axs[1].plot(phi_left_vec, y_A_error_inf, 'o-', lw=lw, ms=ms)
axs[1].plot(phi_left_vec, y_C_error_inf, 'o-', lw=lw, ms=ms)
axs[1].plot(phi_left_vec, y_S_error_inf, 'o-', lw=lw, ms=ms)
axs[1].set_yscale('log')
axs[1].set_xlabel('$\delta \\varphi [-]$', fontsize=labelsize)
axs[1].set_ylabel('log($L_\infty$) [-]', fontsize=labelsize)
axs[1].tick_params(axis='both', labelsize=labelsize)
axs[1].grid()

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

# Finally, the legend (that maybe you'll customize differently)
fig.legend(lines, labels, bbox_to_anchor=(0.69,1.1), ncol=6, fontsize=labelsize)

fig.tight_layout()
# fig.savefig('../Figures/PoissonBoltzmann_Convergence.svg', bbox_inches='tight')
fig.show()


# Visualize the results - rescale to physical values
''' 
The dimensionless parameter were chosen to:
Lambda2 = 8.553e-6
a2 = 7.5412e-4
with the following physical parameters:
T = 293.75 [K] - Temperature
nR = 55 [mol/l] - Reference number density
pR = 1 [atm] - Reference pressure
LR = 20e-9 [m] - Reference length
chi = 80 [-] - Dielectric permittivity
The constants:
e0 = 1.602e-19 [As] - Dielectric constant
k = 1.381e-23 [1/mol] - Avogadro constant
'''
e0 = 1.602e-19 # [As]
k = 1.381e-23 # [J/K]
T = 293.75 # [K]
phi_left_vec_physical = phi_left_vec * (k*T)/e0
fig, axs = plt.subplots(ncols=2, figsize=(30, 12))
labelsize = 40
lw = 6
ms=20
# Log-log plot of L2-error
axs[0].plot(phi_left_vec_physical, y_A_error_L2, 'o-', label='$y_A$', lw=lw, ms=ms)
axs[0].plot(phi_left_vec_physical, y_C_error_L2, 'o-', label='$y_C$', lw=lw, ms=ms)
axs[0].plot(phi_left_vec_physical, y_S_error_L2, 'o-', label='$y_S$', lw=lw, ms=ms)
axs[0].set_yscale('log')
axs[0].set_xlabel('$\delta \\varphi [V]$', fontsize=labelsize)
axs[0].set_ylabel('log($L_2$) [-]', fontsize=labelsize)
axs[0].tick_params(axis='both', labelsize=labelsize)
axs[0].grid()

# Log-log plot of infinity error
axs[1].plot(phi_left_vec_physical, y_A_error_inf, 'o-', lw=lw, ms=ms)
axs[1].plot(phi_left_vec_physical, y_C_error_inf, 'o-', lw=lw, ms=ms)
axs[1].plot(phi_left_vec_physical, y_S_error_inf, 'o-', lw=lw, ms=ms)
axs[1].set_yscale('log')
axs[1].set_xlabel('$\delta \\varphi [V]$', fontsize=labelsize)
axs[1].set_ylabel('log($L_\infty$) [-]', fontsize=labelsize)
axs[1].tick_params(axis='both', labelsize=labelsize)
axs[1].grid()

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

# Finally, the legend (that maybe you'll customize differently)
fig.legend(lines, labels, bbox_to_anchor=(0.69,1.1), ncol=6, fontsize=labelsize)

fig.tight_layout()
# fig.savefig('../Figures/PoissonBoltzmann_Convergence_Rescaled_Dimensions.svg', bbox_inches='tight')
fig.show()