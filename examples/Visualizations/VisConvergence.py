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

# Reference order
x_ref = [1e+1, 1e+5]
O1_2_ref = [10e+4, 10e+0]
O2_2_ref = [10e-3, 10e-11]
# O3_2_ref = [10e-8, 10e-20]
O1_inf_ref = [10e+4, 10e+0]
O2_inf_ref = [10e-4, 10e-12]
# O3_inf_ref = [10e-1, 10e-13]
Ref_Ord_marker = ['--', ':', '-.']


# Plot the results
fig, axs = plt.subplots(ncols=2, figsize=(30, 10))
labelsize = 35
lw = 6
legend_width = 5
ms = 25
axs[0].loglog(number_cells_vec[:-1], y_A_error_L2, 'o-', label='$y_A$', lw=lw, ms=ms)
axs[0].loglog(number_cells_vec[:-1], y_C_error_L2, 'o-', label='$y_C$', lw=lw, ms=ms)
axs[0].loglog(number_cells_vec[:-1], y_S_error_L2, 'o-', label='$y_S$', lw=lw, ms=ms)
axs[0].loglog(number_cells_vec[:-1], phi_error_L2, 'o-', label='$\\varphi$', lw=lw, ms=ms)
axs[0].loglog(number_cells_vec[:-1], p_error_L2, 'o-', label='$p$', lw=lw, ms=ms)
axs[0].loglog(x_ref, O1_2_ref, Ref_Ord_marker[0], color='tab:gray', label='$O(nx)^1$', lw=lw, ms=ms)
axs[0].loglog(x_ref, O2_2_ref, Ref_Ord_marker[1], color='tab:gray', label='$O(nx)^2$', lw=lw, ms=ms)
# axs[0].loglog(x_ref, O3_2_ref, Ref_Ord_marker[2], color='tab:gray', label='$O(nx)^3$', lw=lw, ms=ms)
axs[0].set_xlabel('log(nx)', fontsize=labelsize)
axs[0].set_ylabel('log($L_2$)', fontsize=labelsize)
axs[0].grid()
axs[0].tick_params(axis='both', labelsize=labelsize)

axs[1].loglog(number_cells_vec[:-1], y_A_error_inf, 'o-', lw=lw, ms=ms)
axs[1].loglog(number_cells_vec[:-1], y_C_error_inf, 'o-', lw=lw, ms=ms)
axs[1].loglog(number_cells_vec[:-1], y_S_error_inf, 'o-', lw=lw, ms=ms)
axs[1].loglog(number_cells_vec[:-1], phi_error_inf, 'o-', lw=lw, ms=ms)
axs[1].loglog(number_cells_vec[:-1], p_error_inf, 'o-', lw=lw, ms=ms)
axs[1].loglog(x_ref, O1_inf_ref, Ref_Ord_marker[0], color='tab:gray', lw=lw, ms=ms)
axs[1].loglog(x_ref, O2_inf_ref, Ref_Ord_marker[1], color='tab:gray', label='$O(nx)^2$', lw=lw, ms=ms)
# axs[1].loglog(x_ref, O3_inf_ref, Ref_Ord_marker[2], color='tab:gray', lw=lw, ms=ms)
axs[1].set_xlabel('log(nx)', fontsize=labelsize)
axs[1].set_ylabel('log($L_\infty$)', fontsize=labelsize)
axs[1].grid()
axs[1].tick_params(axis='both', labelsize=labelsize)

# order = [0, 5, 1, 7, 2, 6, 3, 4] 
order = [0, 5, 1, 6, 2, 3, 4] 
lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
lgnd = fig.legend([lines[i] for i in order], [labels[i] for i in order], bbox_to_anchor=(0.81,1.2), ncol=5, fontsize=labelsize)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)

fig.tight_layout()
fig.savefig('../Figures/Convergence.svg', bbox_inches='tight')
fig.show()