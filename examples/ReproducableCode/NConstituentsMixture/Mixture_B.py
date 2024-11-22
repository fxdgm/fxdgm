'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script simulates mixture B from the thesis
'''

# import the needed functions from the FENICSxDGM module
from FENICSxDGM import solve_System_Neq

# Further imports
import matplotlib.pyplot as plt
import numpy as np

# Define Parameter and solver settings
phi_left = 8.0
phi_right = 0.0
p_right = 0.0
y_alpha_R = [1/6, 1/6, 3/6]
z_alpha = [-2.0, -1.0, 1.0]
K = 'incompressible'
Lambda2 = 8.553e-6
a2 = 7.5412e-4
number_cells = 1024*4
refinement_style = 'hard_log'
rtol = 1e-8
return_type = 'Vector'
relax_param = 0.05
max_iter = 2_500

y_alpha_n, phi_n, p_n, x_n = solve_System_Neq(phi_left, phi_right, p_right, z_alpha, y_alpha_R, K, Lambda2, a2, number_cells, return_type=return_type, relax_param=relax_param, max_iter=max_iter, rtol=rtol, refinement_style=refinement_style)

np.savez('../../Data/NConstituentsMixture/Mixture_B.npz', x=x_n, phi=phi_n, p=p_n, y_alpha=y_alpha_n, z_alpha=z_alpha, y_alpha_R=y_alpha_R, phi_left=phi_left, phi_right=phi_right, p_right=p_right, K=K, Lambda2=Lambda2, a2=a2, number_cells=number_cells)

plt.figure()
plt.plot(x_n, phi_n)
plt.xlim(0,0.05)
plt.grid()
plt.xlabel('$x$ [-]')
plt.ylabel('$\\varphi$ [-]')
plt.show()

plt.figure
plt.plot(x_n, p_n)
plt.xlim(0,0.05)
plt.grid()
plt.xlabel('$x$ [-]')
plt.ylabel('$p$ [-]')
plt.show()

plt.figure()
for i in range(len(z_alpha)):
    plt.plot(x_n, y_alpha_n[i], label=f'z = {z_alpha[i]}')
y_S = 1.0 - y_alpha_n[0] - y_alpha_n[1] - y_alpha_n[2]
plt.plot(x_n, y_S, label=f'z = 0')
plt.legend()
plt.grid()
plt.xlim(0,0.05)
plt.xlabel('x [-]')
plt.ylabel('$y_\\alpha$ [-]')
plt.show()
