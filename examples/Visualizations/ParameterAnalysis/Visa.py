'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import matplotlib.pyplot as plt
import numpy as np

# Load data
df = np.load('../../Data/ParameterAnalysis/a.npz')

phi_left_vec = df['phi_left_vec']
a2_vec = df['a2_vec']
x = df['x']
phi = df['phi']
y_A = df['y_A']
y_C = df['y_C']
y_S = df['y_S']
p = df['p']

xlim = 0.08

fig, axs = plt.subplots(figsize=(15,10))
labelsize = 30
lw = 4
for j in range(len(a2_vec)):
    axs.plot(x[-1][j], p[-1][j], label=r'$a^2 = {:.4e}$'.format(a2_vec[j]), lw=lw)
axs.grid()
axs.set_ylim(0.0, np.max(p[-1][0]))
axs.set_xlim(0,xlim)
axs.set_xlabel('$x$ [-]', fontsize=labelsize)
axs.set_ylabel('$p$ [-]', fontsize=labelsize)
axs.tick_params(axis='both', labelsize=labelsize)
axs.legend(loc='best', fontsize=labelsize)
fig.tight_layout()
fig.show()
input("Press Enter to continue...")
