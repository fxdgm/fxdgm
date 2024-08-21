'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Load data
data = np.load('../Data/Convergence.npz')

# Extract data
number_cells_vec = data['number_cells_vec']
y_A_error_L2 = data['y_A_error_L2']
y_C_error_L2 = data['y_C_error_L2']
y_S_error_L2 = data['y_S_error_L2']
phi_error_L2 = data['phi_error_L2']
p_error_L2 = data['p_error_L2']
y_A_error_inf = data['y_A_error_inf']
y_C_error_inf = data['y_C_error_inf']
y_S_error_inf = data['y_S_error_inf']
phi_error_inf = data['phi_error_inf']
p_error_inf = data['p_error_inf']

# Plot the results
fig, axs = plt.subplots(ncols=2, figsize=(30, 10))
labelsize = 30
lw = 6
legend_width = 8
ms = 25
axs[0].loglog(number_cells_vec[:-1], y_A_error_L2, 'o-', label='$y_A$', lw=lw, ms=ms)
axs[0].loglog(number_cells_vec[:-1], y_C_error_L2, 'o-', label='$y_C$', lw=lw, ms=ms)
axs[0].loglog(number_cells_vec[:-1], y_S_error_L2, 'o-', label='$y_S$', lw=lw, ms=ms)
axs[0].loglog(number_cells_vec[:-1], phi_error_L2, 'o-', label='$\\varphi$', lw=lw, ms=ms)
axs[0].loglog(number_cells_vec[:-1], p_error_L2, 'o-', label='$p$', lw=lw, ms=ms)
axs[0].set_xlabel('log(nx)', fontsize=labelsize)
axs[0].set_ylabel('log($L_2$)', fontsize=labelsize)
axs[0].grid()
axs[0].tick_params(axis='both', labelsize=labelsize)

axs[1].loglog(number_cells_vec[:-1], y_A_error_inf, 'o-', lw=lw, ms=ms)
axs[1].loglog(number_cells_vec[:-1], y_C_error_inf, 'o-', lw=lw, ms=ms)
axs[1].loglog(number_cells_vec[:-1], y_S_error_inf, 'o-', lw=lw, ms=ms)
axs[1].loglog(number_cells_vec[:-1], phi_error_inf, 'o-', lw=lw, ms=ms)
axs[1].loglog(number_cells_vec[:-1], p_error_inf, 'o-', lw=lw, ms=ms)
axs[1].set_xlabel('log(nx)', fontsize=labelsize)
axs[1].set_ylabel('log($L_\infty$)', fontsize=labelsize)
axs[1].grid()
axs[1].tick_params(axis='both', labelsize=labelsize)

lgnd = fig.legend(bbox_to_anchor=(0.72, 1.1), fontsize=labelsize, ncol=7, markerscale=1.)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)

fig.tight_layout()
fig.savefig('../Figures/Convergence.svg', bbox_inches='tight')
fig.show()