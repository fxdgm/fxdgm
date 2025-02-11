'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This file implements the fenics solver for the reduced systme of equations to two equations for the electric potential and the pressure.
'''

import numpy as np
from mpi4py import MPI
from dolfinx import mesh, fem, log
from dolfinx.fem.petsc import NonlinearProblem
from dolfinx.nls.petsc import NewtonSolver
from ufl import TestFunctions, split, dot, grad, dx, inner, Mesh, exp
from basix.ufl import element, mixed_element
import matplotlib.pyplot as plt
from fxdgm.RefinedMesh1D import create_refined_mesh


def solve_System_2eq(phi_left:float, phi_right:float, p_right:float, z_A:float, z_C:float, y_A_R:float, y_C_R:float, K:float|str, Lambda2:float, a2:float, number_cells:int, solvation:float = 0, PoissonBoltzmann:bool=False, relax_param:float=None, x0:float=0, x1:float=1, refinement_style:str='uniform', return_type:str='Scalar', rtol:float=1e-8, max_iter:float=500):
    '''
    Solve the simplified dimensionless system of equations presented in: Numerical Treatment of a Thermodynamically Consistent Electrolyte Model, B.Sc. Thesis Habscheid 2024

    System of equations:
        λ²Δ φ =−L²n^F
        
        a²∇p=−n^F∇ φ
        
    with the space charge
        n^F = z_A y_A(φ, p) + z_C y_C(φ ,p)

    if the mixture is compressible: 
        y_alpha = C_alpha * (K+p−1)^(−κ+1)a²K exp(−z_α φ)

    if the mixture is incompressible: 
        y_alpha = D_alpha * exp(−(κ+1)a²p−z_α φ)

    with φ the electric potential, p the pressure, n^F the total free charge density, J_α the diffusion fluxes of species α, λ² a dimensionless parameter, L²=1, a² a dimensionless parameter, N the number of species, and α the species index.

    ! If the Newton solver diverges, you may try to reduce the relaxation parameter.

    Parameters
    ----------
    phi_left : float
        Value of φ at the left boundary
    phi_right : float
        Value of φ at the right boundary
    p_right : float
        Value of p at the right boundary
    z_A : float
        Charge number of species A
    z_C : float
        Charge number of species C
    y_A_R : float
        Atomic fractions of species A at right boundary
    y_C_R : float
        Atomic fractions of species C at right boundary
    K : float | str
        Dimensioness bulk modulus of the electrolyte. If 'incompressible', the system is solved for an incompressible electrolyte
    Lambda2 : float
        Dimensionless parameter
    a2 : float
        Dimensionless parameter
    number_cells : int
        Number of cells in the mesh
    solvation : float, optional
        solvation number, by default 0
    PoissonBoltzmann : bool, optional
        Solve classical Nernst-Planck model with the use of the Poisson-Boltzmann formulation if True, else solve the presented model by Dreyer, Guhlke, Müller, by default False
    relax_param : float, optional
        Relaxation parameter for the Newton solver
        xₙ₊₁ = γ xₙ f(xₙ)/f'(xₙ) with γ the relaxation parameter
        , by default None -> Determined automatically
    x0 : float, optional
        Left boundary of the domain, by default 0
    x1 : float, optional
        Right boundary of the domain, by default 1
    refinement_style : str, optional
        Specify for refinement towards zero
        Options are 'uniform', 'log', 'hard_log', 'hard_hard_log' by default 'uniform'
    return_type : str, optional
        'Vector' or 'Scalar', 'Scalar' returns dolfinx.fem type and 'Vector' numpy arrays of the solution, by default 'Scalar'
    rtol : float, optional
        Relative tolerance for Newton solver, by default 1e-8
    max_iter : float, optional
        Maximum number of Newton iterations, by default 500

    Returns
    -------
    y_A, y_C, phi, p, msh
        Returns atomic fractions for species A and C, electric potential, pressure, and the mesh
        If return_type is 'Vector', the solution is returned as numpy arrays
    '''
    if return_type == 'Scalar':
        raise NotImplementedError('Scalar return type is not implemented yet')
    # Define boundaries of the domain
    x0 = 0
    x1 = 1

    # Define boundaries for the boundary conditions
    def Left(x):
        return np.isclose(x[0], x0)

    def Right(x):
        return np.isclose(x[0], x1)
    
    # Create mesh
    if refinement_style == 'uniform':
        msh = mesh.create_unit_interval(MPI.COMM_WORLD, number_cells, dtype=np.float64)
    else:
        msh = create_refined_mesh(refinement_style, number_cells)

    # Define Finite Elements
    CG1_elem = element('Lagrange', msh.basix_cell(), 1)

    # Define Mixed Function Space
    W_elem = mixed_element([CG1_elem, CG1_elem])#, CG1_elem, CG1_elem])
    W = fem.functionspace(msh, W_elem)

    # Define Trial- and Testfunctions
    u = fem.Function(W)
    phi, p = split(u)
    (v_1, v_2) = TestFunctions(W)

    # Collapse function space for bcs
    W0, _ = W.sub(0).collapse()
    W1, _ = W.sub(1).collapse()
    
    # Define boundary conditions values
    def phi_left_(x):
        return np.full_like(x[0], phi_left)
    def phi_right_(x):
        return np.full_like(x[0], phi_right)
    def p_right_(x):
        return np.full_like(x[0], p_right)
    
    # Interpolate bcs functions
    phi_left_bcs = fem.Function(W0)
    phi_left_bcs.interpolate(phi_left_)
    phi_right_bcs = fem.Function(W0)
    phi_right_bcs.interpolate(phi_right_)
    p_right_bcs = fem.Function(W1)
    p_right_bcs.interpolate(p_right_)
    
    # Identify dofs for boundary conditions
    # Define boundary conditions
    facet_left_dofs = fem.locate_dofs_geometrical((W.sub(0), W.sub(0).collapse()[0]), Left)
    facet_right_dofs = fem.locate_dofs_geometrical((W.sub(0), W.sub(0).collapse()[0]), Right)
    bc_left_phi = fem.dirichletbc(phi_left_bcs, facet_left_dofs, W.sub(0))
    bc_right_phi = fem.dirichletbc(phi_right_bcs, facet_right_dofs, W.sub(0))

    facet_right_dofs = fem.locate_dofs_geometrical((W.sub(1), W.sub(1).collapse()[0]), Right)
    bc_right_p = fem.dirichletbc(p_right_bcs, facet_right_dofs, W.sub(1))

    
    # Combine boundary conditions into list
    bcs = [bc_left_phi, bc_right_phi, bc_right_p]

    def y_A(phi, p):
        if PoissonBoltzmann == False:
            D_A = y_A_R / exp(-(solvation + 1) * a2 * p_right - z_A * phi_right)
            return D_A * exp(-(solvation + 1) * a2 * p - z_A * phi)
        elif PoissonBoltzmann == True:
            D_A = y_A_R / exp(- z_A * phi_right)
            return D_A * exp(- z_A * phi)
    
    def y_C(phi, p):
        if PoissonBoltzmann == False:
            D_C = y_C_R / exp(-(solvation + 1) * a2 * - z_C * phi_right)
            return D_C * exp(-(solvation + 1) * a2 * p - z_C * phi)
        elif PoissonBoltzmann == True:
            D_C = y_C_R / exp(- z_C * phi_right)
            return D_C * exp(- z_C * phi)
    

    # Define variational problem
    if K == 'incompressible':
        # total free charge density
        def nF(y_A, y_C, p):
            return (z_C * y_C + z_A * y_A)
    else: 
        # total number density
        def n(p):
            return (p-1)/K + 1
        
        # total free charge density
        def nF(y_A, y_C, p):
            return (z_C * y_C + z_A * y_A) * n(p)
    # Variational Form
    A = (
        inner(grad(phi), grad(v_1)) * dx
        - 1 / Lambda2 * nF(y_A(phi, p), y_C(phi, p), p) * v_1 * dx
    ) + (
        inner(grad(p), grad(v_2)) * dx
        + 1 / a2 * nF(y_A(phi, p), y_C(phi, p), p) * dot(grad(phi), grad(v_2)) * dx
    )
    F = A

    # Define Nonlinear Problem
    problem = NonlinearProblem(F, u, bcs=bcs)

    # Define Newton Solver and solver settings
    solver = NewtonSolver(MPI.COMM_WORLD, problem)
    solver.convergence_criterion = "incremental"
    solver.rtol = rtol
    if relax_param != None:
        solver.relaxation_parameter = relax_param
    else:
        if phi_right == phi_left:
            solver.relaxation_parameter = 1.0
        else:
            solver.relaxation_parameter = 1/(np.abs(phi_right-phi_left)**(5/4))
    solver.max_it = max_iter
    solver.report = True

    # Solve the problem
    log.set_log_level(log.LogLevel.INFO)
    n, converged = solver.solve(u)
    assert (converged)
    print(f"Number of interations: {n:d}")

    # Split the mixed function space into the individual components    
    phi, p = u.split()
    
    # Return the solution
    if return_type=='Vector':
        x_vals = np.array(msh.geometry.x[:,0])
        phi_vals = np.array(u.sub(0).collapse().x.array)
        p_vals = np.array(u.sub(1).collapse().x.array)

        # Calculate the atomic fractions
        D_A = y_A_R / np.exp(-(solvation + 1) * a2 * p_right - z_A * phi_right)
        y_A_vals = D_A * np.exp(-(solvation + 1) * a2 * p_vals - z_A * phi_vals)
    
        D_C = y_C_R / np.exp(-(solvation + 1) * a2 * p_right - z_C * phi_right)
        y_C_vals = D_C * np.exp(-(solvation + 1) * a2 * p_vals - z_C * phi_vals)

        if PoissonBoltzmann:
            D_A = y_A_R / np.exp(- z_A * phi_right)
            y_A_vals = D_A * np.exp(- z_A * phi_vals)
            D_C = y_C_R / np.exp(- z_C * phi_right)
            y_C_vals = D_C * np.exp(- z_C * phi_vals)
        
        return y_A_vals, y_C_vals, phi_vals, p_vals, x_vals
    
# if __name__ == '__main__':
#     # Define the parameters
#     phi_left = 5.0
#     phi_right = 0.0
#     p_right = 0.0
#     y_A_R = 1/3
#     y_C_R = 1/3
#     z_A = -1.0
#     z_C = 1.0
#     K = 'incompressible'
#     Lambda2 = 8.553e-6
#     a2 = 7.5412e-4
#     number_cells = 1024
#     relax_param = .1
#     rtol = 1e-4
#     max_iter = 500
    
#     # Solve the system
#     y_A, y_C, phi, p, x = solve_System_2eq(phi_left, phi_right, p_right, z_A, z_C, y_A_R, y_C_R, K, Lambda2, a2, number_cells, relax_param=relax_param, x0=0, x1=1, refinement_style='uniform', return_type='Vector', max_iter=max_iter, rtol=rtol)
    
#     # Plot the solution
#     plt.plot(x, phi)
#     plt.xlim(0,0.05)
#     plt.grid()
#     plt.xlabel('x [-]')
#     plt.ylabel('$\\varphi$  [-]')
#     plt.show()
    
#     plt.plot(x, y_A, '--', color='tab:blue', label='$y_A$')
#     plt.plot(x, y_C, '-', color='tab:blue', label='$y_C$')
#     plt.plot(x, 1 - y_A - y_C, ':', color='tab:blue', label='$y_S$')
#     plt.xlim(0,0.05)
#     plt.legend()
#     plt.grid()
#     plt.xlabel('x [-]')
#     plt.ylabel('$y_\\alpha$ [-]')
#     plt.show()
    
#     plt.plot(x, p)
#     plt.xlim(0,0.05)
#     plt.grid()
#     plt.xlabel('x [-]')
#     plt.ylabel('$p$ [-]')
#     plt.show()
