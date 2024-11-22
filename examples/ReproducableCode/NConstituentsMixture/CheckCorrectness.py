'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to validate the implementation of the generic function to solve an electrolyte of N-constituents with the implementation for a ternary electrolyte
'''

# import the needed functions from the FENICSxDGM module
from FENICSxDGM import solve_System_4eq, solve_System_Neq

# Further imports
import matplotlib.pyplot as plt

# Define the parameters and boundary conditions
phi_left = 8.0
phi_right = 0.0
p_right = 0.0
y_R = [1/5, 1/3-1/5, 1/5, 1/3-1/5, 1/6]
y_A_R, y_C_R = 1/3, 1/3
z_alpha = [-1.0, -1.0, 1.0, 1.0, 0.0]
z_A, z_C = -1.0, 1.0
Lambda2 = 8.553e-6
a2 = 7.5412e-4
K = 'incompressible'
number_cells = 1024
refinement_style = 'hard_log'
rtol = 1e-8

y_A_4, y_C_4, phi_4, p_4, x_4 = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, return_type='Vector', refinement_style=refinement_style, rtol=rtol)

y_alpha_n, phi_n, p_n, x_n = solve_System_Neq(phi_left, phi_right, p_right, z_alpha, y_R, K, Lambda2, a2, number_cells, return_type='Vector', refinement_style=refinement_style, rtol=rtol)

plt.figure()
# plt.plot(x_n, phi_n, label='n-constituent')
# plt.plot(x_4, phi_4, label='2-constituent')
plt.plot(x_n, phi_n - phi_4, label='Difference')
plt.grid()
plt.legend()
plt.xlabel('x [-]')
plt.ylabel('$\\varphi$ [-]')
plt.show()

plt.figure()
# plt.plot(x_n, p_n, label='n-constituent')
# plt.plot(x_4, p_4, label='2-constituent')
plt.plot(x_n, p_n - p_4, label='Difference')
plt.grid()
plt.legend()
plt.xlabel('x [-]')
plt.ylabel('$p$ [-]')
plt.show()

plt.figure()
# for i in range(len(z_alpha)):
#     plt.plot(x_n, y_alpha_n[i], label=f'$y_{i}$')
# plt.plot(x_n, y_alpha_n[0] + y_alpha_n[1], label='$y_{A,n}$')
# plt.plot(x_n, y_alpha_n[2] + y_alpha_n[3], label='$y_{C,n}$')
# plt.plot(x_n, 1-y_alpha_n[0]-y_alpha_n[1]-y_alpha_n[2]-y_alpha_n[3], label='$y_{S,n}$')
# plt.plot(x_4, y_A_4, label='$y_{A,2}$')
# plt.plot(x_4, y_C_4, label='$y_{C,2}$')
# plt.plot(x_4, 1-y_A_4-y_C_4, label='$y_{S,2}$')
plt.plot(x_n, y_alpha_n[0] + y_alpha_n[1] - y_A_4, label='Difference $y_{A}$')
plt.plot(x_n, y_alpha_n[2] + y_alpha_n[3] - y_C_4, label='Difference $y_{C}$')
plt.plot(x_n, 1-y_alpha_n[0]-y_alpha_n[1]-y_alpha_n[2]-y_alpha_n[3] - (1-y_A_4-y_C_4), label='Difference $y_{S}$')
plt.legend()
plt.grid()
plt.xlabel('x [-]')
plt.ylabel('$y_\\alpha$ [-]')
plt.show()
