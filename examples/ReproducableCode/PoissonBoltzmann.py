'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to compare the thermodynamically consistent model, proposed by Dreyer, Guhlke and Müller, against the classical Nernst-Plank model with the Poisson-Boltzmann formulation.
'''

# import the needed functions from the fxdgm module
from fxdgm import solve_System_4eq

# Further imports
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Define the parameters and boundary conditions
phi_left = 10.0
phi_right = 0.0
p_right = 0.0
y_A_R, y_C_R = 1/3, 1/3
z_A, z_C = -1.0, 1.0
number_cells = 1024*4
K = 'incompressible'
Lambda2 = 8.553e-6
a2 = 7.5412e-4
refinement_style = 'log'
rtol = 1e-8


# DGM calculations
y_A_DGM_10, y_C_DGM_10, phi_DGM_10, p_DGM_10, x_DGM_10 = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, PoissonBoltzmann=False, relax_param=0.05, refinement_style=refinement_style, return_type='Vector', max_iter=10_000, rtol=rtol)
y_S_DGM_10 = 1 - y_A_DGM_10 - y_C_DGM_10

# PB calculations
y_A_PB_10, y_C_PB_10, phi_PB_10, p_PB_10, x_PB_10 = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, PoissonBoltzmann=True, relax_param=0.05, refinement_style=refinement_style, return_type='Vector', max_iter=10_000, rtol=rtol)
y_S_PB_10 = 1 - y_A_PB_10 - y_C_PB_10



fig, ax1 = plt.subplots()
markers = ['-', '-.', ':']
# Plot electric potential
color_phi = 'tab:blue'
color_p = 'tab:red'
ax1.set_xlabel('x [-]')
ax1.set_ylabel('$\\varphi$  [-]')#, color=color)
ax1.tick_params(axis='y')#, labelcolor=color)
ax1.plot(x_DGM_10, phi_DGM_10, markers[0], color=color_phi)
ax1.plot(x_PB_10, phi_PB_10, markers[1], color=color_phi)
ax1.grid()
ax1.set_ylim(0.0, np.max(phi_DGM_10))
ax1.set_xlabel('$x$ [-]')
ax1.set_ylabel('$\\varphi$ [-]')
ax1.set_xlim(0,0.05)
dummy = ax1.plot(2,1/3, markers[0], color='grey', label='DGM')
dummy = ax1.plot(2,1/3, markers[1], color='grey', label='PB')
ax1.legend()

# Create a second y-axis
ax2 = ax1.twinx()
# Plot pressure
color = 'tab:red'
ax2.set_ylabel('$p$ [-]', color=color)
ax2.plot(x_DGM_10, p_DGM_10, markers[0], color=color_p)
ax2.plot(x_PB_10, p_PB_10, markers[1], color=color_p)
ax2.grid()
ax2.set_ylim(0.0, np.max(p_DGM_10))
ax2.set_xlim(0,0.05)
ax2.set_xlabel('$x$ [-]')
ax2.set_ylabel('$p$ [-]')
ax2.legend()
ax2.tick_params(axis='y', labelcolor=color)

ax1.grid()
fig.tight_layout()
fig.show()

# Plot Concentrations
plt.figure()
markers = ['--', '-', ':']
colors = ['tab:blue', 'tab:orange', 'tab:green']
plt.plot(x_DGM_10, y_A_DGM_10, markers[0], color=colors[0])
plt.plot(x_PB_10, y_A_PB_10, markers[0], color=colors[1])
plt.plot(x_DGM_10, y_C_DGM_10, markers[1], color=colors[0])
plt.plot(x_PB_10, y_C_PB_10, markers[1], color=colors[1])
plt.plot(x_DGM_10, y_S_DGM_10, markers[2], color=colors[0])
plt.plot(x_PB_10, y_S_PB_10, markers[2], color=colors[1])
dummy, = plt.plot(10, 0.1, color='grey', linestyle=markers[0], label='$y_A$')
dummy, = plt.plot(10, 0.1, color='grey', linestyle=markers[1], label='$y_C$')
dummy, = plt.plot(10, 0.1, color='grey', linestyle=markers[2], label='$y_S$')
dummy, = plt.plot(10, 0.1, color=colors[0], linestyle='-', label='DGM')
dummy, = plt.plot(10, 0.1, color=colors[1], linestyle='-', label='PB')
plt.legend()
plt.xlim(0,0.05)
plt.ylim(-0.02, 1.02)
plt.grid()
plt.xlabel('x [-]')
plt.ylabel('$y_\\alpha$ [-]')
plt.tight_layout()
plt.show()

# Save the results
np.savez('../Data/PoissonBoltzmann_10.npz', x_DGM_10=x_DGM_10, y_A_DGM_10=y_A_DGM_10, y_C_DGM_10=y_C_DGM_10, y_S_DGM_10=y_S_DGM_10, phi_DGM_10=phi_DGM_10, p_DGM_10=p_DGM_10, x_PB_10=x_PB_10, y_A_PB_10=y_A_PB_10, y_C_PB_10=y_C_PB_10, y_S_PB_10=y_S_PB_10, phi_PB_10=phi_PB_10, p_PB_10=p_PB_10)

# Smaller Delta varphi
phi_left = 1.0
y_A_DGM_1, y_C_DGM_1, phi_DGM_1, p_DGM_1, x_DGM_1 = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, PoissonBoltzmann=False, relax_param=0.05, x0=0, x1=1, refinement_style=refinement_style, return_type='Vector', max_iter=10_000, rtol=rtol)
y_S_DGM_1 = 1 - y_A_DGM_1 - y_C_DGM_1

y_A_PB_1, y_C_PB_1, phi_PB_1, p_PB_1, x_PB_1 = solve_System_4eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, PoissonBoltzmann=True, relax_param=0.025, x0=0, x1=1, refinement_style=refinement_style, return_type='Vector', max_iter=10_000, rtol=rtol)
y_S_PB_1 = 1 - y_A_PB_1 - y_C_PB_1
    
np.savez('../Data/PoissonBoltzmann_1.npz', phi_left=phi_left, phi_right=phi_right, p_right=p_right, z_A=z_A, z_C=z_C, y_A_R=y_A_R, y_C_R=y_C_R, K=K, Lambda2=Lambda2, a2=a2, number_cells=number_cells, y_A_DGM_01=y_A_DGM_1, y_C_DGM_01=y_C_DGM_1, y_S_DGM_01=y_S_DGM_1, phi_DGM_01=phi_DGM_1, p_DGM_01=p_DGM_1, x_DGM_01=x_DGM_1, y_A_PB_01=y_A_PB_1, y_C_PB_01=y_C_PB_1, y_S_PB_01=y_S_PB_1, phi_PB_01=phi_PB_1, p_PB_01=p_PB_1, x_PB_01=x_PB_1)

# DGM convergence towards PB
# Define Potential differences
phi_left_vec = np.linspace(1,10,10)
phi_left_vec = np.append(np.array([0.1, 0.2, 0.3, 0.5, 0.7]), phi_left_vec)
# Storage for the results
y_A_DGM, y_C_DGM, y_S_DGM, phi_DGM, p_DGM, x_DGM = [], [], [], [], [], []
y_A_PB, y_C_PB, y_S_PB, phi_PB, p_PB, x_PB = [], [], [], [], [], []
# Loop over the potential differences
for phi_left_ in phi_left_vec:
    # DGM model
    y_A_DGM_, y_C_DGM_, phi_DGM_, p_DGM_, x_DGM_ = solve_System_4eq(phi_left_, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, PoissonBoltzmann=False, x0=0, x1=1, refinement_style=refinement_style, return_type='Vector', max_iter=250_000, rtol=rtol, relax_param=0.05)
    y_A_DGM.append(y_A_DGM_)
    y_C_DGM.append(y_C_DGM_)
    y_S_DGM.append(1 - y_A_DGM_ - y_C_DGM_)
    phi_DGM.append(phi_DGM_)
    p_DGM.append(p_DGM_)
    x_DGM.append(x_DGM_)

    # PB model
    y_A_PB_, y_C_PB_, phi_PB_, p_PB_, x_PB_ = solve_System_4eq(phi_left_, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, PoissonBoltzmann=True, x0=0, x1=1, refinement_style=refinement_style, return_type='Vector', max_iter=250_000, rtol=rtol, relax_param=0.05)
    y_A_PB.append(y_A_PB_)
    y_C_PB.append(y_C_PB_)
    y_S_PB.append(1 - y_A_PB_ - y_C_PB_)
    phi_PB.append(phi_PB_)
    p_PB.append(p_PB_)
    x_PB.append(x_PB_)
    
# L2-error
# Interpolate solution vector
y_A_DGM_interp1d = [interp1d(x_DGM[i], y_A_DGM[i]) for i in range(len(phi_left_vec))]
y_C_DGM_interp1d = [interp1d(x_DGM[i], y_C_DGM[i]) for i in range(len(phi_left_vec))]
y_S_DGM_interp1d = [interp1d(x_DGM[i], y_S_DGM[i]) for i in range(len(phi_left_vec))]
phi_DGM_interp1d = [interp1d(x_DGM[i], phi_DGM[i]) for i in range(len(phi_left_vec))]
p_DGM_interp1d = [interp1d(x_DGM[i], p_DGM[i]) for i in range(len(phi_left_vec))]

y_A_PB_interp1d = [interp1d(x_PB[i], y_A_PB[i]) for i in range(len(phi_left_vec))]
y_C_PB_interp1d = [interp1d(x_PB[i], y_C_PB[i]) for i in range(len(phi_left_vec))]
y_S_PB_interp1d = [interp1d(x_PB[i], y_S_PB[i]) for i in range(len(phi_left_vec))]
phi_PB_interp1d = [interp1d(x_PB[i], phi_PB[i]) for i in range(len(phi_left_vec))]
p_PB_interp1d = [interp1d(x_PB[i], p_PB[i]) for i in range(len(phi_left_vec))]

# Calculate L2-error
y_A_error_L2, y_C_error_L2, y_S_error_L2, phi_error_L2, p_error_L2 = [], [], [], [], []
for i in range(len(phi_left_vec)):
    y_A_error_L2.append(np.sqrt(np.trapz((y_A_DGM_interp1d[i](x_DGM[i]) - y_A_PB_interp1d[i](x_DGM[i]))**2, x_DGM[i])))
    y_C_error_L2.append(np.sqrt(np.trapz((y_C_DGM_interp1d[i](x_DGM[i]) - y_C_PB_interp1d[i](x_DGM[i]))**2, x_DGM[i])))
    y_S_error_L2.append(np.sqrt(np.trapz((y_S_DGM_interp1d[i](x_DGM[i]) - y_S_PB_interp1d[i](x_DGM[i]))**2, x_DGM[i])))
    phi_error_L2.append(np.sqrt(np.trapz((phi_DGM_interp1d[i](x_DGM[i]) - phi_PB_interp1d[i](x_DGM[i]))**2, x_DGM[i])))
    p_error_L2.append(np.sqrt(np.trapz((p_DGM_interp1d[i](x_DGM[i]) - p_PB_interp1d[i](x_DGM[i]))**2, x_DGM[i])))
    
    
# Log-log plot of L2-error
plt.figure()
plt.plot(phi_left_vec, y_A_error_L2, 'o-', label='$y_A$')
plt.plot(phi_left_vec, y_C_error_L2, 'o-', label='$y_C$')
plt.plot(phi_left_vec, y_S_error_L2, 'o-', label='$y_S$')
plt.yscale('log')
plt.legend()
plt.xlabel('$\delta \\varphi$')
plt.ylabel('log($L_2$)')
plt.grid()
plt.tight_layout()
plt.show()


# Calculate infinity error
y_A_error_inf, y_C_error_inf, y_S_error_inf, phi_error_inf, p_error_inf = [], [], [], [], []
for i in range(len(phi_left_vec)):
    y_A_error_inf.append(np.max(np.abs(y_A_DGM_interp1d[i](x_DGM[i]) - y_A_PB_interp1d[i](x_DGM[i]))))
    y_C_error_inf.append(np.max(np.abs(y_C_DGM_interp1d[i](x_DGM[i]) - y_C_PB_interp1d[i](x_DGM[i]))))
    y_S_error_inf.append(np.max(np.abs(y_S_DGM_interp1d[i](x_DGM[i]) - y_S_PB_interp1d[i](x_DGM[i]))))
    phi_error_inf.append(np.max(np.abs(phi_DGM_interp1d[i](x_DGM[i]) - phi_PB_interp1d[i](x_DGM[i]))))
    p_error_inf.append(np.max(np.abs(p_DGM_interp1d[i](x_DGM[i]) - p_PB_interp1d[i](x_DGM[i]))))
    
# Log-log plot of infinity error
plt.figure()
plt.plot(phi_left_vec, y_A_error_inf, 'o-', label='$y_A$')
plt.plot(phi_left_vec, y_C_error_inf, 'o-', label='$y_C$')
plt.plot(phi_left_vec, y_S_error_inf, 'o-', label='$y_S$')
plt.yscale('log')
plt.legend()
plt.xlabel('$\delta \\varphi$')
plt.ylabel('log($L_\infty$)')
plt.grid()
plt.tight_layout()
plt.show()


# Save the results
np.savez('../Data/PoissonBoltzmann_Convergence.npz', phi_left_vec=phi_left_vec, y_A_error_L2=y_A_error_L2, y_C_error_L2=y_C_error_L2, y_S_error_L2=y_S_error_L2, phi_error_L2=phi_error_L2, p_error_L2=p_error_L2, y_A_error_inf=y_A_error_inf, y_C_error_inf=y_C_error_inf, y_S_error_inf=y_S_error_inf, phi_error_inf=phi_error_inf, p_error_inf=p_error_inf)