'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Define the parameters and boundary conditions
Lambda2 = 8.553e-6
z_A = -1
z_C = 1
y_L = 1/3

# Define the equilibrium concentrations
def y_C(phi, phi_prime):
    return y_L * np.exp(-z_C * phi - 1/2 * Lambda2 * phi_prime**2)

def y_A(phi, phi_prime):
    return y_L * np.exp(-z_A * phi - 1/2 * Lambda2 * phi_prime**2)

# Define the ODEs as a system of first-order ODEs
def func(PHI, x):
    phi, phi_prime = PHI
    f = -1/Lambda2 * (z_C * y_C(phi, phi_prime) + z_A * y_A(phi, phi_prime))
    return [phi_prime, f]

# Initial conditions
Y0 = [0, 1e-9]
x_end = np.array([-0.95, -1.0, -1.05, -1.1])*1e-1

# Storage for the results
y_C_end, y_A_end, y_S_end = [], [], []
phi_end, x_vec = [], []

# Solve the ODEs for different values of x_end
for x_ in x_end:
    x = np.linspace(x_, 0, 1024)

    Y = odeint(func, Y0, x)

    Y_mirror = np.flip(Y, axis=0)
    phi_end.append(Y_mirror[:, 0])
    y_C_end.append(y_C(Y_mirror[:, 0], Y_mirror[:, 1]))
    y_A_end.append(y_A(Y_mirror[:, 0], Y_mirror[:, 1]))
    y_S_end.append(1-y_C_end[-1]-y_A_end[-1])
    x_vec.append(x)

# Visualize the results
# create 2x1 subplots
fig, axs = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(14-14/3, 12), constrained_layout=True)

# clear subplots
for ax in axs:
    ax.remove()

# add subfigure per subplot
gridspec = axs[0].get_subplotspec().get_gridspec()
subfigs = [fig.add_subfigure(gs) for gs in gridspec]

for row, subfig in enumerate(subfigs):
    subfig.suptitle(f'$L_x = $ {abs(round(x_end[row], 4))}', fontsize=22)

    # create 1x2 subplots per subfig
    axs = subfig.subplots(nrows=1, ncols=2)

    for col, ax in enumerate(axs):
        labelsize = 20
        ax.set_ylim(-0.05, 1.05)
        match col:
            case 0: 
                ax.plot(x_vec[row], phi_end[row])
                ax.set_ylim(-0.5, phi_end[-1][0]+0.5)
                ax.set_ylabel('$\\varphi$', fontsize=labelsize)
            case 1: 
                ax.plot(x_vec[row], y_C_end[row], label='$y_C$')
                ax.plot(x_vec[row], y_A_end[row], label='$y_A$')
                ax.plot(x_vec[row], y_S_end[row], label='$y_S$')
                ax.legend()
                ax.set_ylabel('$y_\\alpha$', fontsize=labelsize)
        ax.set_xlim(min(x_end), 0)
        ax.set_xlabel('x [-]', fontsize=labelsize)
        ax.grid(True)
        ax.tick_params(axis='x', labelrotation=45)
fig.show()




# Streamplot
phi_range = np.arange(-0.1, 0.1, 0.01)  # Range for x-axis
dphi_range = np.linspace(-5e-3, 5e-3, 10)  # Range for y-axis

# Create a meshgrid with different sizes for x and y axes
phi_values, dphi_values = np.meshgrid(phi_range, dphi_range)
initial_conditions = np.array([phi_values.ravel(), dphi_values.ravel()]).T

# Points at which the solution is requested
x_domain = np.linspace(0, 1.0e-1, 1024)

# Prepare storage for the results
results = np.zeros((len(initial_conditions), len(x_domain), 2))

# Numerical integration for each initial condition
for i, Y0 in enumerate(initial_conditions):
    Y = odeint(func, Y0, x_domain)
    results[i, :, :] = Y

# Reshape results for plotting
Y_reshaped = results[:, :, 0].reshape(len(dphi_range), len(phi_range), len(x_domain))

# Select a specific slice for plotting, e.g., the last time point -> last point of phi
Y_slice = Y_reshaped[:, :, -1]

# Compute derivatives for the streamplot
U, V = np.gradient(Y_slice, dphi_range, phi_range)

# Plotting
plt.subplots(tight_layout=True)
# lw = 5*Y_slice/Y_slice.max()
strm = plt.streamplot(phi_values, dphi_values, U, V, color=U, linewidth=2, cmap='autumn', density=10)
plt.colorbar(strm.lines)
plt.xlim(-0.01, 0.01)
plt.ylim(dphi_values.min(), dphi_values.max())
plt.xlabel('$\\varphi$')
plt.xticks(rotation='vertical')
plt.ylabel("$\phi$")
plt.show()