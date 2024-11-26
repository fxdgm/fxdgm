'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script is used to analyze the influence of the solvation on the charge of the system and the double-layer capacity.
'''

from fxdgm import solve_System_4eq, Phi_pot_center, C_dl, n, Q_num_, Q_num_dim

# Import plotting library
import matplotlib.pyplot as plt
import numpy as np

# Define Parameter
e0 = 1.602e-19 # [As]
k = 1.381e-23 # [J/K]
T = 293.75 # [K]
epsilon0 = 8.85e-12 #[F/m]
F = 9.65e+4 # [As/mol]
NA = 6.022e+23 # [1/mol] - Avogadro constant
nR_mol = 55
nR_m = nR_mol * NA * 1/(1e-3)# [1/m^3]
pR = 1.01325 * 1e+5 # [Pa]
LR = 20e-9
chi = 80 # [-]

# Parameter and bcs for the electrolyte
Lambda2 = (k*T*epsilon0*(1+chi))/(e0**2 * nR_m * (LR)**2)
a2 = (pR)/(nR_m * k * T)
K = 'incompressible'
Molarity = 0.01
y_R = Molarity / nR_mol
z_A, z_C = -1.0, 1.0
phi_R = 0.0
p_R = 0

# Solver settings
number_cells = 1024#*2
relax_param = 0.3
rtol = 1e-8
refinement_style = 'hard_log'
max_iter = 10_000
return_type = 'Vector'

# phi^L domain
Vol_start = -1.0
Volt_end = 1.0
n_Volts = 303

Phi_Pot_Diff_dim = np.linspace(Vol_start, Volt_end, n_Volts)
Phi_Pot_Diff_dimless = Phi_Pot_Diff_dim * e0/(k*T)

Phi_Pot_Diff_dim_PB = np.linspace(-0.35, 0.35, int(n_Volts/4))
Phi_Pot_Diff_dimless_PB = Phi_Pot_Diff_dim_PB * e0/(k*T)


# kappa
kappa_vec = [0, 5, 10, 15]
kappa_legend = ['PB', 0, 5, 10, 15]
# Solution vectors
y_A, y_C, y_S, phi, p, x = [], [], [], [], [], []

# Extra run for Poisson-Boltzmann
phi_PB, y_A_PB, y_C_PB, y_S_PB, p_PB,x_PB = [], [], [], [], [], []
for i, phi_bcs in enumerate(Phi_Pot_Diff_dimless_PB):
    y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_bcs, phi_R, p_R, z_A, z_C, y_R, y_R, K, Lambda2, a2, number_cells, solvation=0, PoissonBoltzmann=True, refinement_style='hard_log', rtol=rtol, max_iter=max_iter, relax_param=0.01, return_type=return_type)
    y_A_PB.append(y_A_)
    y_C_PB.append(y_C_)
    y_S_PB.append(1 - y_A_ - y_C_)
    phi_PB.append(phi_)
    p_PB.append(p_)
    x_PB.append(x_)

for kappa_ in kappa_vec:
    phi_inner, y_A_inner, y_C_inner, y_S_inner, p_inner,x_inner = [], [], [], [], [], []
    for i, phi_bcs in enumerate(Phi_Pot_Diff_dimless):
        relax_param = 0.025
        if kappa_ >= 10:
            relax_param = 0.01
        y_A_, y_C_, phi_, p_, x_ = solve_System_4eq(phi_bcs, phi_R, p_R, z_A, z_C, y_R, y_R, K, Lambda2, a2, number_cells, solvation=kappa_, refinement_style='hard_log', rtol=rtol, max_iter=max_iter, return_type=return_type, relax_param=relax_param)
        y_A_inner.append(y_A_)
        y_C_inner.append(y_C_)
        y_S_inner.append(1 - y_A_ - y_C_)
        phi_inner.append(phi_)
        p_inner.append(p_)
        x_inner.append(x_)
    y_A.append(y_A_inner)
    y_C.append(y_C_inner)
    y_S.append(y_S_inner)
    phi.append(phi_inner)
    p.append(p_inner)
    x.append(x_inner)


# Charge
Q_DL_dimless_PB_ = []
Q_DL_dim_PB_ = []
for j in range(len(Phi_Pot_Diff_dimless_PB)):
    Q_DL_dimless_PB_.append(Q_num_(y_A_PB[j], y_C_PB[j], n(p_PB[j], K), x_PB[j], z_A, z_C))
    Q_DL_dim_PB_.append(Q_num_dim(y_A_PB[j], y_C_PB[j], n(p_PB[j], K), x_PB[j], z_A, z_C, nR_m, e0, LR))
Q_DL_dimless_PB_ = np.array(Q_DL_dimless_PB_)
Q_DL_dim_PB_ = np.array(Q_DL_dim_PB_)

Q_DL_dimless_ = []
Q_DL_dim_ = []
for i in range(len(kappa_vec)):
    Q_inner_dimless_ = []
    Q_inner_dim_ = []
    for j in range(len(Phi_Pot_Diff_dimless)):
        Q_inner_dimless_.append(Q_num_(y_A[i][j], y_C[i][j], n(p[i][j], K), x[i][j], z_A, z_C))
        Q_inner_dim_.append(Q_num_dim(y_A[i][j], y_C[i][j], n(p[i][j], K), x[i][j], z_A, z_C, nR_m, e0, LR))
    Q_DL_dimless_.append(Q_inner_dimless_)
    Q_DL_dim_.append(Q_inner_dim_)
Q_DL_dimless_ = np.array(Q_DL_dimless_)
Q_DL_dim_ = np.array(Q_DL_dim_)


# Double Layer Capacity
C_DL_dimless_PB = C_dl(Q_DL_dimless_PB_, Phi_Pot_Diff_dimless_PB)
C_DL_dimless = [C_dl(q_dl, Phi_Pot_Diff_dimless) for q_dl in Q_DL_dimless_]

C_DL_dim_PB = C_dl(Q_DL_dim_PB_, Phi_Pot_Diff_dim_PB)
C_DL_dim = [C_dl(q_dl, Phi_Pot_Diff_dim) for q_dl in Q_DL_dim_]



# Plotting
# Charge
fig = plt.figure()
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:cyan', 'tab:purple']
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensional data
ax.plot(Phi_Pot_Diff_dim_PB, Q_DL_dim_PB_, color=colors[0])
for i, q_dl in enumerate(Q_DL_dim_):
    ax.plot(Phi_Pot_Diff_dim, q_dl, color=colors[i])
ax.grid()
ax.set_xlabel('$\delta \\varphi [nm]$', color=color_dim)
ax.set_ylabel('$Q$ [\u03bc$F/cm^3]$', color=color_dim)
ax.tick_params(axis='x', colors=color_dim)
ax.tick_params(axis='y', colors=color_dim)


ax2.plot(Phi_Pot_Diff_dimless_PB, Q_DL_dimless_PB_, color=colors[0], label=f'$\kappa$: {kappa_legend[0]}')
for i, q_dl in enumerate(Q_DL_dimless_):
    ax2.plot(Phi_Pot_Diff_dimless, q_dl, color=colors[i+1], label=f'$\kappa$: {kappa_legend[i+1]}')
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('$\delta \\varphi [-]$', color=color_dimless) 
ax2.set_ylabel('$Q [-]$', color=color_dimless)       
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 
ax2.tick_params(axis='x', colors=color_dimless)
ax2.tick_params(axis='y', colors=color_dimless)

fig.legend()
fig.tight_layout()
fig.show()


# Double Layer Capacity
Phi_pot_center_array_dimless_PB = Phi_pot_center(Phi_Pot_Diff_dimless_PB)
Phi_pot_center_array_dim_PB = Phi_pot_center(Phi_Pot_Diff_dim_PB)
Phi_pot_center_array_dimless = Phi_pot_center(Phi_Pot_Diff_dimless)
Phi_pot_center_array_dim = Phi_pot_center(Phi_Pot_Diff_dim)
fig = plt.figure()
color_dimless = 'tab:purple'
color_dim = 'tab:red'
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

# Plot dimensional data
ax.plot(Phi_pot_center_array_dim_PB, C_DL_dim_PB, color=colors[0])
for i, c_dl in enumerate(C_DL_dimless):
    ax.plot(Phi_pot_center_array_dimless, c_dl, color=colors[i])
ax.grid()
ax.set_xlabel('$\delta \\varphi [nm]$', color=color_dim)
ax.set_ylabel('$C_{dl}$ [\u03bc$F/cm^2]$', color=color_dim)
ax.tick_params(axis='x', colors=color_dim)
ax.tick_params(axis='y', colors=color_dim)

ax2.plot(Phi_pot_center_array_dimless_PB, C_DL_dimless_PB, color=colors[0], label=f'$\kappa$: {kappa_legend[0]}')
for i, c_dl in enumerate(C_DL_dimless):
    ax2.plot(Phi_pot_center_array_dimless, c_dl, color=colors[i+1], label=f'$\kappa$: {kappa_legend[i+1]}')
# ax2.grid()
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('$\delta \\varphi [-]$', color=color_dimless) 
ax2.set_ylabel('$Q [-]$', color=color_dimless)       
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 
ax2.tick_params(axis='x', colors=color_dimless)
ax2.tick_params(axis='y', colors=color_dimless)

fig.legend()
fig.tight_layout()
fig.show()

# Save the results
np.savez('../../Data/DoubleLayerCapacity/Solvation.npz', Lambda2=Lambda2, a2=a2, K=K, kappa_vec=kappa_vec, z_A=z_A, z_C=z_C, phi_R=phi_R, p_R=p_R, Vol_start=Vol_start, Volt_end=Volt_end, n_Volts=n_Volts, Phi_pot_center_array_dim=Phi_pot_center_array_dim, Phi_pot_center_array_dimless=Phi_pot_center_array_dimless, Phi_Pot_Diff_dim=Phi_Pot_Diff_dim, Phi_Pot_Diff_dimless=Phi_Pot_Diff_dimless, C_DL_dim=C_DL_dim, C_DL_dimless=C_DL_dimless, Q_DL_dim_=Q_DL_dim_, Q_DL_dimless_=Q_DL_dimless_, Molarity=Molarity, nR_mol=nR_mol, nR_m=nR_m, pR=pR, LR=LR, chi=chi, e0=e0, k=k, T=T, epsilon0=epsilon0, F=F, NA=NA, y_R=y_R, y_A=y_A, y_C=y_C, y_S=y_S, phi=phi, p=p, x=x, y_A_PB=y_A_PB, y_C_PB=y_C_PB, y_S_PB=y_S_PB, phi_PB=phi_PB, p_PB=p_PB, x_PB=x_PB, Q_DL_dim_PB_=Q_DL_dim_PB_, Q_DL_dimless_PB_=Q_DL_dimless_PB_, Phi_pot_center_array_dim_PB=Phi_pot_center_array_dim_PB, Phi_pot_center_array_dimless_PB=Phi_pot_center_array_dimless_PB, C_DL_dim_PB=C_DL_dim_PB, C_DL_dimless_PB=C_DL_dimless_PB, Phi_Pot_Diff_dim_PB=Phi_Pot_Diff_dim_PB, Phi_Pot_Diff_dimless_PB=Phi_Pot_Diff_dimless_PB)
