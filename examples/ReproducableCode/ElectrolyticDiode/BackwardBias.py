'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

Solve the electrolitic diode for the backward bias case

'''
# import the needed functions from the fxdgm module
from fxdgm import ElectrolyticDiode

# Import plotting library
import matplotlib.pyplot as plt
import numpy as np

# Parameter
phi_bias = 10
Bias_type = 'BackwardBias'
g_phi = 350
y_fixed = 0.01
z_A = -1.0
z_C = 1.0
K = 'incompressible'
Lambda2 = 8.553e-6
a2 = 7.5412e-4
solvation = 5
number_cells = [80, 512]#[20, 128] # ! [40, 400]
Lx = 0.02
Ly = 0.1
x0 = np.array([0, 0])
x1 = np.array([Lx, Ly])

# Solver parameters
rtol = 1e-8
relax_param = 0.15 #0.05
max_iter = 15_000    

# Solve the system
y_A, y_C, phi, p, X, u = ElectrolyticDiode(Bias_type, phi_bias, g_phi, z_A, z_C, y_fixed, y_fixed, K, Lambda2, a2, number_cells, relax_param=relax_param, Lx=Lx, Ly=Ly, solvation=solvation, rtol=rtol, max_iter=max_iter, return_type='Extended')
x, y = X[0], X[1]
y_S = 1 - y_A - y_C

# Plot results
levelsf = 10
levels = 10

# y_A
plt.figure(figsize=(2, 4))
c = plt.tricontourf(x, y, y_A, levelsf)
plt.colorbar(c)
plt.tricontour(x, y, y_A, levels, colors='black')
plt.title('$y_A$')
plt.show()

# y_C
plt.figure(figsize=(2, 4))
c = plt.tricontourf(x, y, y_C, levelsf)
plt.colorbar(c)
plt.tricontour(x, y, y_C, levels, colors='black')
plt.title('$y_C$')
plt.show()

# y_S
plt.figure(figsize=(2, 4))
c = plt.tricontourf(x, y, y_S, levelsf)
plt.colorbar(c)
plt.tricontour(x, y, y_S, levels, colors='black')
plt.title('$y_S$')
plt.show()

# phi
plt.figure(figsize=(2, 4))
c = plt.tricontourf(x, y, phi, levelsf)
plt.colorbar(c)
plt.tricontour(x, y, phi, levels, colors='black')
plt.title('$\\varphi$')
plt.show()

# p
plt.figure(figsize=(2, 4))
c = plt.tricontourf(x, y, p, levelsf)
plt.colorbar(c)
plt.tricontour(x, y, p, levels, colors='black')
plt.title('$p$')
plt.show()

# Save the results
np.savez('../../Data/ElectrolyticDiode/BackwardBias.npz', phi_bias=phi_bias, g_phi=g_phi, y_fixed=y_fixed, z_A=z_A, z_C=z_C, K=K, Lambda2=Lambda2, a2=a2, number_cells=number_cells, Lx=Lx, Ly=Ly, x0=x0, x1=x1, solvation=0, rtol=rtol, relax_param=relax_param, max_iter=max_iter, y_A=y_A, y_C=y_C, y_S=y_S, phi=phi, p=p, x=x, y=y)
