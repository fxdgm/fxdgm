'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import numpy as np

# Load data
df = np.load('../../Data/ParameterAnalysis/Lambda.npz')

phi_left_vec = df['phi_left_vec']
Lambda2_vec = df['Lambda2_vec']
x = df['x']
phi = df['phi']
y_A = df['y_A']
y_C = df['y_C']
y_S = df['y_S']
p = df['p']
y_A_R = df['y_A_R']
y_C_R = df['y_C_R']

xlim = 0.08

# Visualize the results
fig, axs = plt.subplots(2, 2, figsize=(30,20))
labelsize = 40
lw = 4
legend_width = 5
markers = ['--', '-', ':']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
for i in range(len(phi_left_vec)):
    # Plot phi

    match i:
        case 0: 
            i_ = 0
            j_ = 0
        case 1: 
            i_ = 0
            j_ = 1
        case 2: 
            i_ = 1
            j_ = 0
        case 3: 
            i_ = 1
            j_ = 1
    axs[i_,j_].set_title(f'$\delta \\varphi$ = {phi_left_vec[i]}', fontsize=labelsize)
    for j in range(len(Lambda2_vec)):
        clr = colors[j]
        axs[i_,j_].plot(x[i][j], y_A[i][j], markers[0], color=clr, lw=lw)
        axs[i_,j_].plot(x[i][j], y_C[i][j], markers[1], color=clr, lw=lw)
        axs[i_,j_].plot(x[i][j], y_S[i][j], markers[2], color=clr, lw=lw)
    axs[i_,j_].grid()
    axs[i_,j_].set_xlim(0,xlim)
    axs[i_,j_].set_xlabel('$x$ [-]', fontsize=labelsize)
    axs[i_,j_].set_ylabel('$y_\\alpha$ [-]', fontsize=labelsize)
    axs[i_,j_].tick_params(axis='both', labelsize=labelsize)

dummy, = axs[i_,j_].plot(2, y_A_R, color='grey', linestyle='--', label='$y_A$')
dummy, = axs[i_,j_].plot(2, y_A_R, color='grey', linestyle='-', label='$y_C$')
dummy, = axs[i_,j_].plot(2, y_A_R, color='grey', linestyle=':', label='$y_S$')
for index, Lambda2_cur in enumerate(Lambda2_vec):
    dummy, = axs[i_,j_].plot(10, y_A_R, color=colors[index], linestyle='-', label=f'$\lambda^2$ = {Lambda2_cur}')

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

# Finally, the legend (that maybe you'll customize differently)
order = [0, 3, 1, 4, 2, 5] 
lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
lgnd = fig.legend([lines[i] for i in order], [labels[i] for i in order], bbox_to_anchor=(0.86,1.12), ncol=3, fontsize=labelsize)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)
fig.tight_layout()
# fig.savefig('../../Figures/ParameterAnalysis/Lambda_fractions.svg', bbox_inches='tight')
fig.show()



fig, axs = plt.subplots(2, 2, figsize=(30,20))
markers = ['--', '-.', ':']
colors = ['tab:blue', 'tab:red']
for i in range(len(phi_left_vec)):
    # Plot phi

    match i:
        case 0: 
            i_ = 0
            j_ = 0
        case 1: 
            i_ = 0
            j_ = 1
        case 2: 
            i_ = 1
            j_ = 0
        case 3: 
            i_ = 1
            j_ = 1
            
    axs[i_,j_].set_title('$\delta \\varphi$ = {}'.format(phi_left_vec[i]), fontsize=labelsize)
    axs[i_,j_].set_xlabel('x [-]', fontsize=labelsize)
    axs[i_,j_].set_ylabel('$\\varphi$  [-]', color=colors[0], fontsize=labelsize)
    axs[i_,j_].tick_params(axis='y', labelcolor=colors[0], labelsize=labelsize)
    for j in range(len(Lambda2_vec)):
        axs[i_,j_].plot(x[i][j], phi[i][j], markers[j], color=colors[0], lw=lw)
    axs[i_,j_].grid()
    axs[i_,j_].set_ylim(np.min(phi[i]), np.max(phi[i]))
    # axs[i_,j_].set_xlabel('$x$ [-]', fontsize=labelsize)
    # axs[i_,j_].set_ylabel('$\\varphi$ [-]', fontsize=labelsize)
    axs[i_,j_].set_xlim(0,xlim)
    axs[i_,j_].tick_params(axis='x', labelsize=labelsize)
    
    
    # Create a second y-axis
    ax2 = axs[i_,j_].twinx()

    # Plot p
    color = 'tab:red'
    ax2.set_ylabel('$p$ [-]', color=colors[1], fontsize=labelsize)
    for j in range(len(Lambda2_vec)):
        ax2.plot(x[i][j], p[i][j], markers[j], color=colors[1], lw=lw)
    ax2.grid()
    ax2.set_ylim(np.min(p[i]), np.max(p[i]))
    ax2.set_xlim(0,xlim)
    ax2.set_xlabel('$x$ [-]', fontsize=labelsize)
    ax2.set_ylabel('$p$ [-]', fontsize=labelsize)
    ax2.legend()
    ax2.tick_params(axis='y', labelcolor=colors[1], labelsize=labelsize)
    ax2.tick_params(axis='x', labelsize=labelsize)
    
for j in range(len(Lambda2_vec)):
    dummy = axs[i_,j_].plot(2, 1/3, color='grey', linestyle=markers[j], label='$\lambda^2$ = {}'.format(Lambda2_vec[j]))
# So far, nothing special except the managed prop_cycle. Now the trick:
lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

lgnd = fig.legend(lines, labels, bbox_to_anchor=(0.845,1.07), ncol=4, fontsize=labelsize)
for line in lgnd.get_lines():
    line.set_linewidth(legend_width)
    
fig.tight_layout()
# fig.savefig('../../Figures/ParameterAnalysis/Lambda2_pot_press.svg', bbox_inches='tight')
fig.show()