'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import numpy as np


# Load data
data_4_1 = np.load('../Data/NConstituentsMixture/Mixture_4_1.npz')
data_4_2 = np.load('../Data/NConstituentsMixture/Mixture_4_2.npz')
data_5 = np.load('../Data/NConstituentsMixture/Mixture_5.npz')
data_6 = np.load('../Data/NConstituentsMixture/Mixture_6.npz')

x, phi, p, y, z = [], [], [], [], []
for data in [data_4_1, data_4_2, data_5, data_6]:
    x.append(data['x'])
    phi.append(data['phi'])
    p.append(data['p'])
    y.append(data['y_alpha'])
    z.append(data['z_alpha'])

xlim = 0.05
labelsize = 30
lw = 4
legend_width = 8
subtitles_long = ['Mixture $4_1$', 'Mixture $4_2$', 'Mixture $5$', 'Mixture $6$']
subtitles_short = ['$4_1$', '$4_2$', '$5$', '$6$']
# Visualize the concentrations and pressure
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(30,20))
plotting_index = 0
color_p = 'tab:red'
colors = ['tab:green', 'tab:orange', 'tab:purple', 'tab:pink', 'tab:olive', 'tab:cyan']
for i in range(2):
    for j in range(2):
            # Concentrations
            for species in range(len(z[plotting_index])):
                axs[i,j].plot(x[plotting_index], y[plotting_index][species], label=f'z = {z[plotting_index][species]}', lw=lw, color=colors[species])
            y_S_ = 1 - np.sum(y[plotting_index], axis=0)
            axs[i,j].plot(x[plotting_index], y_S_, label=f'z = {0}', lw=lw, color=colors[-1])
            lgnd = axs[i,j].legend(fontsize=labelsize)
            for line in lgnd.get_lines():
                line.set_linewidth(legend_width)
            axs[i,j].set_xlim(0,xlim)
            axs[i,j].grid()
            axs[i,j].set_xlabel('$x$ [-]', fontsize=labelsize)
            axs[i,j].set_ylabel('$y_\\alpha$ [-]', fontsize=labelsize)
            axs[i,j].tick_params(axis='both', labelsize=labelsize)

            # Pressure
            axs_twin = axs[i,j].twinx()
            axs_twin.plot(x[plotting_index], p[plotting_index], color=color_p, lw=lw)
            axs_twin.set_xlim(0,xlim)
            axs_twin.grid()
            axs_twin.set_xlabel('$x$ [-]', fontsize=labelsize)
            axs_twin.set_ylabel('$p$ [-]', color=color_p, fontsize=labelsize)
            axs_twin.tick_params(axis='y', labelcolor=color_p, labelsize=labelsize)
            axs_twin.tick_params(axis='x', labelsize=labelsize)

            axs[i,j].set_title(subtitles_long[plotting_index], fontsize=labelsize)

            # Next mixture
            plotting_index += 1
fig.tight_layout()
fig.savefig('../Figures/NConstituentMixture_Concentrations_Pressure.svg')
fig.show()



# Visualize the electric potential
fig, axs = plt.subplots(layout='constrained', figsize=(15, 10))

for i in range(4):
    axs.plot(x[i], phi[i], label=subtitles_short[i], lw=lw)
# axs.plot(x[0], phi[0], label='$4_1$', lw=lw)
# axs.plot(x[1], phi[1], label='$4_2$', lw=lw)
# axs.plot(x[2], phi[2], label='$5$', lw=lw)
# axs.plot(x[3], phi[3], label='$6$', lw=lw)
axs.set_xlim(0,xlim)
axs.set_xlabel('x [-]', fontsize=labelsize)
axs.set_ylabel('$\\varphi$ [-]', fontsize=labelsize)
axs.tick_params(axis='both', labelsize=labelsize)
axs.grid()

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

lgnd = fig.legend(lines, labels, bbox_to_anchor=(0.84,1.1), ncol=4, fontsize=labelsize)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)

fig.show()
fig.savefig('../Figures/NConstituentMixture_ElectricPotential.svg', bbox_inches='tight')

for p_ in p:
    print(np.max(p_))