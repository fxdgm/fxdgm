'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import numpy as np


# Load data
data_ForwardBias = np.load('../Data/ElectrolyticDiode/ForwardBias.npz')
y_A_Forward = data_ForwardBias['y_A']
y_C_Forward = data_ForwardBias['y_C']
y_S_Forward = data_ForwardBias['y_S']
phi_Forward = data_ForwardBias['phi']
p_Forward = data_ForwardBias['p']
x_Forward = data_ForwardBias['x']
y_Forward = data_ForwardBias['y']

data_BackwardBias = np.load('../Data/ElectrolyticDiode/BackwardBias.npz')
y_A_Backward = data_BackwardBias['y_A']
y_C_Backward = data_BackwardBias['y_C']
y_S_Backward = data_BackwardBias['y_S']
phi_Backward = data_BackwardBias['phi']
p_Backward = data_BackwardBias['p']
x_Backward = data_BackwardBias['x']
y_Backward = data_BackwardBias['y']

data_NoBias = np.load('../Data/ElectrolyticDiode/NoBias.npz')
y_A_NoBias = data_NoBias['y_A']
y_C_NoBias = data_NoBias['y_C']
y_S_NoBias = data_NoBias['y_S']
phi_NoBias = data_NoBias['phi']
p_NoBias = data_NoBias['p']
x_NoBias = data_NoBias['x']
y_NoBias = data_NoBias['y']

y_A_packed = [y_A_Forward, y_A_NoBias, y_A_Backward]
y_C_packed = [y_C_Forward, y_C_NoBias, y_C_Backward]
y_S_packed = [y_S_Forward, y_S_NoBias, y_S_Backward]
phi_packed = [phi_Forward, phi_NoBias, phi_Backward]
p_packed = [p_Forward, p_NoBias, p_Backward]
x_packed = [x_Forward, x_NoBias, x_Backward]
y_packed = [y_Forward, y_NoBias, y_Backward]

# Plot
color_theme_potential = 'coolwarm'
color_theme_concentration = 'viridis'
color_theme_pressure = 'cividis'

fig, axs = plt.subplots(nrows=3, ncols=5, figsize=(30, 30))
labelsize = 30
legend_width = 8
levels_colorbar = 20
levels_contour = 20

vmap_concentrations = np.linspace(0, 1, levels_colorbar)
vmap_potential = np.linspace(-20, 20, levels_colorbar)
vmap_pressure = np.linspace(np.min(p_packed), np.max(p_packed), levels_colorbar)

for bias, (y_A, y_C, y_S, phi, p, x, y) in enumerate(zip(y_A_packed, y_C_packed, y_S_packed, phi_packed, p_packed, x_packed, y_packed)): 
    c = axs[bias,0].tricontourf(x, y, phi, cmap=color_theme_potential, levels=vmap_potential)#, extend="both")
    # c.cmap.set_under('k')
    c.set_clim(-20, 20)
    cbar = fig.colorbar(c, ax=axs[bias,0])
    cbar.ax.tick_params(labelsize=labelsize)
    axs[bias,0].tricontour(x, y, phi, colors='black', levels=levels_contour)
    axs[bias,0].tick_params(axis='both', labelsize=labelsize)

    c = axs[bias,1].tricontourf(x, y, y_A, cmap=color_theme_concentration, vmin=np.min(y_A), vmax=np.max(y_A), levels=vmap_concentrations)#, extend='both')
    # cbar = fig.colorbar(c, ax=axs[bias,1], boundaries=np.linspace(0,1,5))
    # cbar.solids.set_edgecolor("face")
    # cbar.ax.tick_params(labelsize=labelsize)
    axs[bias,1].tricontour(x, y, y_A, colors='black', levels=levels_contour)
    axs[bias,1].tick_params(axis='both', labelsize=labelsize)

    c = axs[bias,2].tricontourf(x, y, y_C, cmap=color_theme_concentration, levels=vmap_concentrations)
    # cbar = fig.colorbar(c, ax=axs[bias,2])
    # cbar.ax.tick_params(labelsize=labelsize)
    axs[bias,2].tricontour(x, y, y_C, colors='black', levels=levels_contour)
    axs[bias,2].tick_params(axis='both', labelsize=labelsize)

    c = axs[bias,3].tricontourf(x, y, y_S, cmap=color_theme_concentration, levels=vmap_concentrations)
    c.set_clim(0, 1)
    cbar = fig.colorbar(c, ax=axs[bias,3])
    cbar.ax.tick_params(labelsize=labelsize)
    axs[bias,3].tricontour(x, y, y_S, colors='black', levels=levels_contour)
    axs[bias,3].tick_params(axis='both', labelsize=labelsize)

    c = axs[bias,4].tricontourf(x, y, p, cmap=color_theme_pressure, levels=vmap_pressure)
    c.set_clim(np.min(p_packed), np.max(p_packed))
    cbar = fig.colorbar(c, ax=axs[bias,4])
    cbar.ax.tick_params(labelsize=labelsize)
    axs[bias,4].tricontour(x, y, p, colors='black', levels=levels_contour)
    axs[bias,4].tick_params(axis='both', labelsize=labelsize)

axs[0,0].set_title('$\\varphi [-]$', fontsize=labelsize)
axs[0,1].set_title('$y_A [-]$', fontsize=labelsize)
axs[0,2].set_title('$y_C [-]$', fontsize=labelsize)
axs[0,3].set_title('$y_S [-]$', fontsize=labelsize)
axs[0,4].set_title('$p [-]$', fontsize=labelsize)
fig.tight_layout()
fig.savefig('../Figures/ElectrolyticDiode.svg')
fig.show()

print('np.max(y_A_Forward):', np.max(y_A_Forward))
print('np.max(y_A_NoBias):', np.max(y_A_NoBias))
print('np.max(y_A_Backward):', np.max(y_A_Backward))

print('np.max(y_C_Forward):', np.max(y_C_Forward))
print('np.max(y_C_NoBias):', np.max(y_C_NoBias))
print('np.max(y_C_Backward):', np.max(y_C_Backward))