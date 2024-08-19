'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script visualizes the incompressible solutions for the charge of the systema and the double layer capacity.
'''

import matplotlib.pyplot as plt
import numpy as np


# Molarity

# Load data
data = np.load('../../Data/DoubleLayerCapacity/Compressibility.npz')

Q = data['Q']
C_DL = data['C_DL']
y_A = data['y_A']
y_C = data['y_C']
y_S = data['y_S']
phi_left = data['phi_left']
phi_left_center = data['phi_left_center']
n_sol = data['n_sol']
K_vec = data['K_vec']


# Charge
plt.figure()
[plt.plot(phi_left, Q[i], label=f'K = {K_vec[i]}') for i in range(len(K_vec))]
plt.grid()
plt.legend()
plt.xlabel('$\delta \\varphi$ [-]')
plt.ylabel('Q $[-]$')
plt.tight_layout()
plt.show()   

# Double layer capacity
plt.figure()
[plt.plot(phi_left_center, C_DL[i], label=f'K = {K_vec[i]}') for i in range(len(K_vec))]
plt.grid()
plt.legend()
plt.xlabel('$\delta \\varphi$ [-]')
plt.ylabel('$C_{dl} [-]$')
plt.tight_layout()
plt.show()

# y_alpha_L
y_A_np, y_C_np, y_S_np = np.array(y_A), np.array(y_C), np.array(y_S)
markers = ['--', '-', ':']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

n_sol_np = np.array(n_sol)
n_A_np, n_C_np, n_S_np = y_A_np * n_sol_np, y_C_np * n_sol_np, y_S_np * n_sol_np
plt.figure()
clr = colors[0]
for i in range(len(K_vec)):
    clr = colors[i]
    plt.plot(phi_left, n_A_np[i,:,0], '--', color=clr)
    plt.plot(phi_left, n_C_np[i,:,0], '-', color=clr)
    plt.plot(phi_left, n_S_np[i,:,0], ':', color=clr)
dummy, = plt.plot(0, 0, color='grey', linestyle='--', label='$n_A$')
dummy, = plt.plot(0, 0, color='grey', linestyle='-', label='$n_C$')
dummy, = plt.plot(0, 0, color='grey', linestyle=':', label='$n_S$')
for index, K_ in enumerate(K_vec):
    dummy, = plt.plot(0, 0, color=colors[index], linestyle='-', label=f'K = {K_}')
plt.grid()
plt.legend()
plt.xlabel('$\delta \\varphi$ [-]')
plt.ylabel('$n_\\alpha^L [-]$')
plt.tight_layout()
plt.show()