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

plt.figure(figsize=(15,10))
labelsize = 30
lw = 4
for j in range(len(a2_vec)):
    plt.plot(x[-1][j], p[-1][j], label='$a^2 = {:.4e}$'.format(a2_vec[j]), lw=lw)
plt.grid()
plt.ylim(0.0, np.max(p[-1][0]))
plt.xlim(0,xlim)
plt.xlabel('$x$ [-]', fontsize=labelsize)
plt.ylabel('$p$ [-]', fontsize=labelsize)
plt.tick_params(axis='both', labelsize=labelsize)
plt.legend(loc='best', fontsize=labelsize)
plt.tight_layout()
plt.savefig('../../Figures/ParameterAnalysis/a2.svg')
plt.show()