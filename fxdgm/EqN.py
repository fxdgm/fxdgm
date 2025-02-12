'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This script implements the fenics solver for the generic system of equations for N species
'''

import numpy as np
from mpi4py import MPI
from dolfinx import mesh, fem, log
from dolfinx.fem.petsc import NonlinearProblem
from dolfinx.nls.petsc import NewtonSolver
from ufl import TestFunctions, split, dot, grad, dx, inner, ln, Mesh
from basix.ufl import element, mixed_element
import matplotlib.pyplot as plt
from fxdgm.RefinedMesh1D import create_refined_mesh

def solve_System_Neq(phi_left:float, phi_right:float, p_right:float, z_alpha:list, y_R:list, K:float|str, Lambda2:float, a2:float, number_cells:int, solvation:float = 0, PoissonBoltzmann:bool=False, relax_param:float=None, x0:float=0, x1:float=1, refinement_style:str='uniform', return_type:str='Vector', rtol:float=1e-8, max_iter:float=500):
    '''
    Solve the dimensionless system of equations presented in: Numerical Treatment of a Thermodynamically Consistent Electrolyte Model, B.Sc. Thesis Habscheid 2024

    System of equations:
        λ²Δ φ =−L²n^F

        a²∇p=−n^F∇ φ
        
        div(J_α)=0  α∈ {1,...,N−1}

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
    z_alpha : list
        Charge numbers for species α = 1,...,N-1
    y_R : list
        Atomic fractions at right boundary for species α = 1,...,N-1
    K : float | str
        Dimensioness bulk modulus of the electrolyte. If 'incompressible', the system is solved for an incompressible electrolyte
    Lambda2 : float
        Dimensionless parameter
    a2 : float
        Dimensionless parameter
    number_cells : int
        Number of cells in the mesh
    solvation : float, optional
        solvation number, not implemented yet, by default 0
    PoissonBoltzmann : bool, optional
        Solve classical Nernst-Planck model with the use of the Poisson-Boltzmann formulation if True, else solve the presented model by Dreyer, Guhlke, Müller, Not implemented yet, by default False
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
        'Vector' or 'Scalar' (not implemented yet, should be implemented in a later version), 'Scalar' returns dolfinx.fem type and 'Vector' numpy arrays of the solution, by default 'Vector'
    rtol : float, optional
        Relative tolerance for Newton solver, by default 1e-8
    max_iter : float, optional
        Maximum number of Newton iterations, by default 500

    Returns
    -------
    y_A, y_C, phi, p, msh
        Returns atomic fractions for species A and C, electric potential, pressure, and the mesh
        If return_type is 'Vector', the solution is returned as numpy arrays
        Only return_type 'Vector' is implemented yet
    '''
    if solvation != 0: 
        raise NotImplementedError('Solvation number not implemented yet')
    if PoissonBoltzmann:
        raise NotImplementedError('Poisson-Boltzmann not implemented yet')
    # Define boundaries of the domain
    x0 = 0
    x1 = 1

    # Define boundaries
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
    Elem_list = [CG1_elem, CG1_elem]
    [Elem_list.append(CG1_elem) for _ in range(len(z_alpha))]
    W_elem = mixed_element(Elem_list)
    W = fem.functionspace(msh, W_elem)

    # Define Trial- and Testfunctions
    u = fem.Function(W)
    my_TrialFunctions = split(u)
    my_TestFunctions = TestFunctions(W)

    phi, p = my_TrialFunctions[0], my_TrialFunctions[1]
    v_1, v_2 = my_TestFunctions[0], my_TestFunctions[1]
    y_alpha = my_TrialFunctions[2:]
    v_alpha = my_TestFunctions[2:]

    # Collapse function space for bcs
    W_ = []
    [W_.append(W.sub(i).collapse()[0]) for i in range(len(z_alpha)+2)]

    # Define boundary conditions values
    def phi_left_(x):
        return np.full_like(x[0], phi_left)
    def phi_right_(x):
        return np.full_like(x[0], phi_right)
    def p_right_(x):
        return np.full_like(x[0], p_right)
    
    # Interpolate bcs functions
    phi_left_bcs = fem.Function(W_[0])
    phi_left_bcs.interpolate(phi_left_)
    phi_right_bcs = fem.Function(W_[0])
    phi_right_bcs.interpolate(phi_right_)
    p_right_bcs = fem.Function(W_[1])
    p_right_bcs.interpolate(p_right_)

    # Identify dofs for boundary conditions
    facet_left_dofs = fem.locate_dofs_geometrical((W.sub(0), W.sub(0).collapse()[0]), Left)
    facet_right_dofs = fem.locate_dofs_geometrical((W.sub(0), W.sub(0).collapse()[0]), Right)
    bc_left_phi = fem.dirichletbc(phi_left_bcs, facet_left_dofs, W.sub(0))
    bc_right_phi = fem.dirichletbc(phi_right_bcs, facet_right_dofs, W.sub(0))

    facet_right_dofs = fem.locate_dofs_geometrical((W.sub(1), W.sub(1).collapse()[0]), Right)
    bc_right_p = fem.dirichletbc(p_right_bcs, facet_right_dofs, W.sub(1))

    # Combine boundary conditions for electric potential and pressure into list
    bcs = [bc_left_phi, bc_right_phi, bc_right_p]

    # Repeat the same for the boundary conditoins for the atomic fractions
    for i in range(len(z_alpha)):
        y_right_bcs = fem.Function(W_[i+2])
        def y_right_(x):
            return np.full_like(x[0], y_R[i])
        y_right_bcs.interpolate(y_right_)
        facet_right_dofs = fem.locate_dofs_geometrical((W.sub(i+2), W.sub(i+2).collapse()[0]), Right)
        bc_right_y = fem.dirichletbc(y_right_bcs, facet_right_dofs, W.sub(i+2))
        bcs.append(bc_right_y)
        
    # Define variational problem
    if K == 'incompressible':
        # total free charge density
        def nF(y_alpha):
            nF = 0
            for i in range(len(z_alpha)):
                nF += z_alpha[i] * y_alpha[i]
            return nF
        
        # Diffusion fluxes for species A and C
        def J_alpha(y_alpha, alpha, phi, p):
            mu_alpha = ln(y_alpha[alpha])
            mu_S = ln(1 - sum(y_alpha))
            return grad(mu_alpha - mu_S + z_alpha[alpha] * phi)
        
        # Variational Form
        A = (
            inner(grad(phi), grad(v_1)) * dx
            - 1 / Lambda2 * nF(y_alpha) * v_1 * dx
        ) + (
            inner(grad(p), grad(v_2)) * dx
            + 1 / a2 * nF(y_alpha) * dot(grad(phi), grad(v_2)) * dx
        )
        for alpha in range(len(z_alpha)):
            A += (
                inner(J_alpha(y_alpha, alpha, phi, p), grad(v_alpha[alpha])) * dx
            )
        if PoissonBoltzmann:
            raise ValueError('Poisson-Boltzmann not implemented for incompressible systems')
    else: 
        raise ValueError('Only incompressible systems are implemented')
    F = A

    # Initialize initial guess for u
    with u.vector.localForm() as u_loc:
        u_loc.set(0)

    # Initialize initial guess for u
    for alpha in range(len(z_alpha)):
        y_alpha_init = fem.Function(W_[alpha+2])
        y_alpha_init.interpolate(lambda x: np.full_like(x[0], y_R[alpha]))
        u.sub(alpha+2).interpolate(y_alpha_init)

    # Define Nonlinear Problem
    problem = NonlinearProblem(F, u, bcs=bcs)

    # Define Newton Solver
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

    
    log.set_log_level(log.LogLevel.INFO)
    n, converged = solver.solve(u)
    assert (converged)
    print(f"Number of (interations: {n:d}")

    # Return the solution    
    if return_type=='Vector':
        x = np.array(msh.geometry.x[:,0])
        phi = np.array(u.sub(0).collapse().x.array)
        p = np.array(u.sub(1).collapse().x.array)
        y = []
        [y.append(u.sub(i+2).collapse().x.array) for i in range(len(z_alpha))]
        y = np.array(y)    
        return y, phi, p, x
    
    
if __name__ == '__main__': # pragma: no cover # dont cover main in coverage
    # Define the parameters
    phi_left = 8.0
    phi_right = 0.0
    p_right = 0.0
    y_R = [3/6, 1/6, 1/6]
    z_alpha = [-1.0, 1.0, 2.0]
    K = 'incompressible'
    Lambda2 = 8.553e-6
    a2 = 7.5412e-4
    number_cells = 1024
    relax_param = .05
    rtol = 1e-4
    max_iter = 2_500
    refinement_style = 'hard_log'
    return_type = 'Vector'
    
    # Solve the system
    y, phi, p, x = solve_System_Neq(phi_left, phi_right, p_right, z_alpha, y_R, K, Lambda2, a2, number_cells, relax_param=relax_param, refinement_style=refinement_style, return_type=return_type, max_iter=max_iter, rtol=rtol)
    
    # Plot the solution
    plt.figure()
    plt.plot(x, phi)
    plt.xlim(0,0.05)
    plt.grid()
    plt.xlabel('x [-]')
    plt.ylabel('$\\varphi$ [-]')
    plt.show()
    
    plt.figure()
    plt.xlim(0,0.05)
    plt.plot(x, p)
    plt.grid()
    plt.xlabel('x [-]')
    plt.ylabel('$p$ [-]')
    plt.show()

    plt.figure()
    for i in range(len(z_alpha)):
        plt.plot(x, y[i], label=f'$y_{i}$')
    plt.xlim(0,0.05)
    plt.legend()
    plt.grid()
    plt.xlabel('x [-]')
    plt.ylabel('$y_i$ [-]')
    plt.show()