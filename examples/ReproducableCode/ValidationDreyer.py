'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to validate the implemetation with:
Wolfgang Dreyer, Clemens Guhlke, and Rüdiger Müller. Bulk-surface electrothermodynamics and applications to electrochemistry. Entropy, 20(12), 2018
'''

# import the src file needed to solve the system of equations
import sys
import os

# Add the src directory to the sys.path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'src')
sys.path.insert(0, src_path)

from Eq04 import solve_System_4eq
from Eq02 import solve_System_2eq

# Remove the src directory from sys.path after import
del sys.path[0]

# Further imports
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Define the parameters and boundary conditions
e0 = 1.602e-19 # [As]
k = 1.381e-23 # [J/K]
T = 293.75#298#293.15 # [K]
epsilon0 = 8.85e-12 #[F/m]
F = 9.65e+4 # [As/mol]
NA = 6.022e+23 # [1/mol] - Avogadro constant
p_ref = 1.01325 * 1e+5 # [Pa]
L_ref = 20e-9 # 20e-9[m]
chi = 80 # [-]

# BCS according to Dreyer
nRef = 55.4 # [mol/L]
Molarity = 0.5
y_A_R, y_C_R = Molarity / nRef, Molarity / nRef #0.01, 0.01
pR = 0
z_A, z_C = -1.0, 1.0
nR_m = nRef * NA * 1/(1e-3) # [1/m^3]
phi_L_dim = 0.6 # [V] ->  600 mV
phi_R_dim = 0.0 # [V]
phi_L_dimless = phi_L_dim * e0 / (k * T)
phi_R_dimless = phi_R_dim * e0 / (k * T)
phi_L_dimless, phi_R_dimless

# Parameters
K = 'incompressible'
Lambda2 = (k*T*epsilon0*(1+chi))/(e0**2 * nR_m * (L_ref)**2)
a2 = (p_ref)/(nR_m * k * T) # 0.0007486770882915494
Lambda2, a2 # values not sure, as T, chi and L_ref not given in Dreyer paper
# ! Lambda2 would be: 8.491106981682818e-06 with these parameter
# Let's try out smaller values to reproduce the results from the Dreyer paper
# Lambda2 = 3.4e-6
Lambda2 = 2.4e-6
a2 = 0.00075 # 0.0007
# Lambda2 = Lambda2 * 1e-1

# Solver parameters
number_cells = 1024
# number_cells_PB = number_cells*16
relax_param = 0.005
refinement_style = 'log'
max_iter = 100_000
return_type = 'Vector'
rtol = 1e-8


y_A_dimless, y_C_dimless, y_S_dimless, phi_dimless, p_dimless, x_dimless = [], [], [], [], [], []
y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_L_dimless, phi_R_dimless, pR, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells=number_cells, solvation=0, PoissonBoltzmann=False, relax_param=relax_param, refinement_style=refinement_style, return_type=return_type, max_iter=max_iter, rtol=rtol)
y_A_dimless.append(y_A_)
y_C_dimless.append(y_C_)
y_S_dimless.append(1 - y_A_ - y_C_)
phi_dimless.append(phi_)
p_dimless.append(p_)
x_dimless.append(x_)

y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_L_dimless, phi_R_dimless, pR, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells=number_cells, solvation=8, PoissonBoltzmann=False, relax_param=relax_param, refinement_style=refinement_style, return_type=return_type, max_iter=max_iter, rtol=rtol)
y_A_dimless.append(y_A_)
y_C_dimless.append(y_C_)
y_S_dimless.append(1 - y_A_ - y_C_)
phi_dimless.append(phi_)
p_dimless.append(p_)
x_dimless.append(x_)

# ? Additional issue from NP -> very bad convergence
# Apply extra refinement because of bad convergence, but use larger relaxation parameter due to the simplified system to two equations
# Use only system of 2 equations to get better convergence
y_A_, y_C_, phi_, p_, x_ = solve_System_2eq(phi_L_dimless, phi_R_dimless, pR, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, solvation=0, PoissonBoltzmann=True, relax_param=0.7, refinement_style='hard_hard_log', return_type=return_type, max_iter=max_iter, rtol=rtol)
y_A_dimless.append(y_A_)
y_C_dimless.append(y_C_)
y_S_dimless.append(1 - y_A_ - y_C_)
phi_dimless.append(phi_)
p_dimless.append(p_)
x_dimless.append(x_)

# Rescale to physical values
y_A_dimless, y_C_dimless, y_S_dimless, phi_dimless, p_dimless, x_dimless = np.array(y_A_dimless), np.array(y_C_dimless), np.array(y_S_dimless), np.array(phi_dimless), np.array(p_dimless), np.array(x_dimless)
phi_dim = phi_dimless * k * T / e0
p_dim = p_dimless * p_ref
x_dim = x_dimless * L_ref
y_A_dim = y_A_dimless
y_C_dim = y_C_dimless
y_S_dim = y_S_dimless
n_A_dim = y_A_dim * nRef
n_C_dim = y_C_dim * nRef
n_S_dim = y_S_dim * nRef

# Store the results
np.savez('../Data/Validation_Dreyer_BulkSurface.npz', y_A_dimless=y_A_dimless, y_C_dimless=y_C_dimless, y_S_dimless=y_S_dimless, phi_dimless=phi_dimless, p_dimless=p_dimless, x_dimless=x_dimless, y_A_dim=y_A_dim, y_C_dim=y_C_dim, y_S_dim=y_S_dim, n_A_dim=n_A_dim, n_C_dim=n_C_dim, n_S_dim=n_S_dim, phi_dim=phi_dim, p_dim=p_dim, x_dim=x_dim, Lambda2=Lambda2, a2=a2)

# Visualize the results if main
if __name__ == '__main__':
    # Options
    markers = [':', '-.', '-'] #['-', '-.', ':', '--']
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
    labelsize = 15
    lw = 2
    legend_width = 3

    scale_x = 1e-9
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))

    # Figure
    fig, axs = plt.subplots(ncols=2, figsize=(13,5))
    axs[0].plot(x_dim[0], n_A_dim[0], markers[0], color=colors[0], lw=lw, label='Poisson-Boltzmann')
    axs[0].plot(x_dim[1], n_A_dim[1], markers[1], color=colors[1], lw=lw, label=f'ideal mixture, $\kappa = 0$')
    # axs[0].plot(x_dim[2], n_A_dim[2], markers[2], color=colors[2], lw=lw, label=f'solvated ions, $\kappa = 8$')
    axs[0].grid()
    axs[0].xaxis.set_major_formatter(ticks_x)
    axs[0].set_xlim(0, 2.5*scale_x)
    axs[0].set_ylim(0, 60)
    axs[0].set_xlabel('x [nm]', fontsize=labelsize)
    axs[0].set_ylabel('$n_A$ [mol/m$^3$]', fontsize=labelsize)

    a = plt.axes([.17, .4, .29, .5])
    a.plot(x_dim[0], n_C_dim[0], markers[0], color=colors[0], lw=lw)
    a.plot(x_dim[1], n_C_dim[1], markers[1], color=colors[1], lw=lw)
    # a.plot(x_dim[2], n_C_dim[2], markers[2], color=colors[2], lw=lw)
    a.grid()
    a.xaxis.set_major_formatter(ticks_x)
    a.set_xlim(0, 4.5*scale_x)
    a.set_xlabel('x [nm]', fontsize=labelsize)
    a.set_ylabel('$n_C$ [mol/m$^3$]', fontsize=labelsize)



    axs[1].plot(x_dim[0], phi_dim[0], markers[0], color=colors[0], lw=lw)
    axs[1].plot(x_dim[1], phi_dim[1], markers[1], color=colors[1], lw=lw)
    # axs[1].plot(x_dim[2], phi_dim[2], markers[2], color=colors[2], lw=lw)
    axs[1].grid()
    axs[1].xaxis.set_major_formatter(ticks_x)
    axs[1].set_xlim(0, 2.5*scale_x)
    axs[1].set_xlabel('x [nm]', fontsize=labelsize)
    axs[1].set_ylabel('$\\varphi [V]$', fontsize=labelsize)

    a = plt.axes([.18+.5, .4, .29, .5])
    a.plot(x_dim[0], p_dim[0]*1e-6, markers[0], color=colors[0], lw=lw)
    a.plot(x_dim[1], p_dim[1]*1e-6, markers[1], color=colors[1], lw=lw)
    # a.plot(x_dim[2], p_dim[2]*1e-6, markers[2], color=colors[2], lw=lw)
    a.grid()
    a.xaxis.set_major_formatter(ticks_x)
    a.set_xlim(0, 0.9*scale_x)
    a.set_ylim(0, 2_700)
    a.set_xlabel('x [nm]', fontsize=labelsize)
    a.set_ylabel('$p [MPa]$', fontsize=labelsize)

    lgnd = fig.legend(bbox_to_anchor=(0.85, 1.1), fontsize=labelsize, ncol=6)
    for line in lgnd.get_lines():
        line.set_linewidth(legend_width)

    fig.tight_layout()
    fig.show()