'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de

This module solves the dimensionless system of equations for the example of an electric diode

# ! Disclaimer: The results conform with [A Numerical Strategy for Nernst–Planck Systems with Solvation Effect, J. Fuhrmann, DOI:10.1002/fuce.201500215]. As the size of the domain, the boundary conditions, and the parameters are chosen differently, it can not be expected to match the same results quantitatively but qualitatively. In [Fuhrmann], only the potential and the cations are visualized. The potential behaves the same, and the cations are pushed to the outside of the domain for the forward bias and to the center of the domain for the backward bias. Furthermore, a rectification effect in the concentrations of the ions cannot be seen, as the range of the concentrations is the same along the different biases. On the other hand, this rectification process can be observed in [Entropy and convergence analysis for two finite volume schemes for a Nernst-Planck-Poisson system with ion volume constraints, B. Gaudeaul, J. Fuhrmann, DOI:10.1007/s00211-022-01279-y]. The electric potential can be verified to match the behavior from [Gaudeaul & Fuhrmann]. Furthermore, the ion concentrations can also be validated qualitatively. However, in [Gaudeaul & Fuhrmann], a rectification effect can be observed, reducing the concentrations of anions and cations for the reverse bias and no bias compared to the forward bias.
'''

import numpy as np
from mpi4py import MPI
from dolfinx import mesh, fem, log, io
from dolfinx.fem.petsc import NonlinearProblem
from dolfinx.nls.petsc import NewtonSolver
from ufl import TestFunctions, split, dot, grad, dx, inner, ln
from basix.ufl import element, mixed_element
import matplotlib.pyplot as plt
from ufl import Measure
from dolfinx.mesh import locate_entities, meshtags

def ElectrolyticDiode(Bias_type:str, phi_bias:float, g_phi:float, z_A:float, z_C:float, y_A_bath:float, y_C_bath:float, K:float|str, Lambda2:float, a2:float, number_cells:list, solvation:float = 0, PoissonBoltzmann:bool=False, relax_param:float=None, Lx:float=2, Ly:float=10, rtol:float=1e-8, max_iter:float=500, return_type:str='Vector'):
    '''
    Solves the system of equations for the example of an electric diode

    Solve the dimensionless system of equations presented in: Numerical Treatment of a Thermodynamically Consistent Electrolyte Model, B.Sc. Thesis Habscheid 2024

    ! If the Newton solver diverges, you may try to reduce the relaxation parameter.

    Parameters
    ----------
    Bias_type : str
        ForwardBias, NoBias, BackwardBias
    phi_bias : float
        Bias in φ
    g_phi : float
        Neumann boundary condition for φ
    z_A : float
        Charge number of species A
    z_C : float
        Charge number of species C
    y_A_bath : float
        Bath concentration of anions
    y_C_bath : float
        Bath concentration of cations
    K : float | str
        Dimensioness bulk modulus of the electrolyte. If 'incompressible', the system is solved for an incompressible electrolyte
        ! Only implemented for incompressible mixtures, yet
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
    Lx : float, optional
        Length of domain in x-direction, by default 2
    Ly : float, optional
        Length of domain in y-direction, by default 10
    rtol : float, optional
        Relative tolerance for Newton solver, by default 1e-8
    max_iter : float, optional
        Maximum number of Newton iterations, by default 500
    return_type : str, optional
        Type of return value, by default 'Vector'
        'Vector' -> Returns the solution as a numpy array for triangle elements
        'Extended' -> Returns the solution as both, a numpy array for triangle elements and the fenicsx function u


    Returns
    -------
    y_A_vector, y_C_vector, phi_vector, p_vector, x_vector
        Returns atomic fractions for species A and C, electric potential, pressure, and the mesh as numpy arrays for triangle elements. x_vector is a list of both dimensions [x, y]
        If return_type is 'Extended', also returns the fenicsx function u
    '''
    if K != 'incompressible':
        raise NotImplementedError('Only incompressible electrolytes are implemented yet')
    x0 = np.array([0, 0])
    x1 = np.array([Lx, Ly])
    match Bias_type:
        case 'ForwardBias': phi_bias = phi_bias
        case 'NoBias': phi_bias = 0
        case 'BackwardBias': phi_bias = -phi_bias
        case _: raise ValueError('Invalid Bias_type')

    # Define boundaries
    geom_tol = 1E-4 # ! Geometric tolerance, may need to be adjusted
    def Left(x):
        return np.isclose(x[0], x0[0], geom_tol, geom_tol)

    def Right(x):
        return np.isclose(x[0], x1[0], geom_tol, geom_tol)

    def Top(x):
        return np.isclose(x[1], x1[1], geom_tol, geom_tol)

    def Bottom(x):
        return np.isclose(x[1], x0[1], geom_tol, geom_tol)

    def Right_Top(x):
        NeumannPart = np.logical_and(1/2*Ly < x[1], x[1] < 3/4*Ly)
        RightPart = np.isclose(x[0], x1[0], geom_tol, geom_tol)
        return np.logical_and(RightPart, NeumannPart)

    def Right_Bottom(x):
        NeumannPart = np.logical_and(1/4*Ly < x[1], x[1] < 1/2*Ly)
        RightPart = np.isclose(x[0], x1[0], geom_tol, geom_tol)
        return np.logical_and(RightPart, NeumannPart)

    def Left_Top(x):
        NeumannPart = np.logical_and(1/2*Ly < x[1], x[1] < 3/4*Ly)
        LeftPart = np.isclose(x[0], x0[0], geom_tol, geom_tol)
        return np.logical_and(LeftPart, NeumannPart)

    def Left_Bottom(x):
        NeumannPart = np.logical_and(1/4*Ly < x[1], x[1] < 1/2*Ly)
        LeftPart = np.isclose(x[0], x0[0], geom_tol, geom_tol)
        return np.logical_and(LeftPart, NeumannPart)
    
    # Create the mesh
    msh = mesh.create_rectangle(MPI.COMM_WORLD, [x0, x1], number_cells)

    # Define Finite Elements
    CG1_elem = element('Lagrange', msh.basix_cell(), 1)
    # from ufl import FiniteElement
    # CG1_elem = FiniteElement("Lagrange", msh.ufl_cell(), 1)

    # Define Mixed Function Space
    W_elem = mixed_element([CG1_elem, CG1_elem, CG1_elem, CG1_elem])
    W = fem.functionspace(msh, W_elem)

    # Define Trial- and Testfunctions
    u = fem.Function(W)
    y_A, y_C, phi, p = split(u)
    (v_A, v_C, v_1, v_2) = TestFunctions(W)

    # Define boundary conditions
    W0, _ = W.sub(0).collapse()
    W1, _ = W.sub(1).collapse()
    W2, _ = W.sub(2).collapse()
    W3, _ = W.sub(3).collapse()

    def phi_bottom_(x):
        return np.full_like(x[1], 0)
    def phi_top_(x):
        return np.full_like(x[1], phi_bias)
    def y_A_bottom_(x):
        return np.full_like(x[1], y_A_bath)
    def y_A_top_(x):
        return np.full_like(x[1], y_A_bath)
    def y_C_bottom_(x):
        return np.full_like(x[1], y_C_bath)
    def y_C_top_(x):
        return np.full_like(x[1], y_C_bath)
    
    phi_bottom_bcs = fem.Function(W2)
    phi_bottom_bcs.interpolate(phi_bottom_)
    phi_top_bcs = fem.Function(W2)
    phi_top_bcs.interpolate(phi_top_)
    y_A_bottom_bcs = fem.Function(W0)
    y_A_bottom_bcs.interpolate(y_A_bottom_)
    y_A_top_bcs = fem.Function(W0)
    y_A_top_bcs.interpolate(y_A_top_)
    y_C_bottom_bcs = fem.Function(W1)
    y_C_bottom_bcs.interpolate(y_C_bottom_)
    y_C_top_bcs = fem.Function(W1)
    y_C_top_bcs.interpolate(y_C_top_)

    # Identify face tags and create dirichlet conditions
    facet_bottom_dofs = fem.locate_dofs_geometrical((W.sub(2), W.sub(2).collapse()[0]), Bottom)
    facet_top_dofs = fem.locate_dofs_geometrical((W.sub(2), W.sub(2).collapse()[0]), Top)
    bc_bottom_phi = fem.dirichletbc(phi_bottom_bcs, facet_bottom_dofs, W.sub(2))
    bc_top_phi = fem.dirichletbc(phi_top_bcs, facet_top_dofs, W.sub(2))

    facet_bottom_dofs = fem.locate_dofs_geometrical((W.sub(0), W.sub(0).collapse()[0]), Bottom)
    bc_bottom_y_A = fem.dirichletbc(y_A_bottom_bcs, facet_bottom_dofs, W.sub(0))
    facet_top_dofs = fem.locate_dofs_geometrical((W.sub(0), W.sub(0).collapse()[0]), Top)
    bc_top_y_A = fem.dirichletbc(y_A_top_bcs, facet_top_dofs, W.sub(0))

    facet_bottom_dofs = fem.locate_dofs_geometrical((W.sub(1), W.sub(1).collapse()[0]), Bottom)
    bc_bottom_y_C = fem.dirichletbc(y_C_bottom_bcs, facet_bottom_dofs, W.sub(1))
    facet_top_dofs = fem.locate_dofs_geometrical((W.sub(1), W.sub(1).collapse()[0]), Top)
    bc_top_y_C = fem.dirichletbc(y_C_top_bcs, facet_top_dofs, W.sub(1))

    # Collect boundary conditions
    bcs = [bc_bottom_phi, bc_top_phi, bc_bottom_y_A, bc_top_y_A, bc_bottom_y_C, bc_top_y_C]
    # bcs = [bc_bottom_phi, bc_top_phi, bc_bottom_y_A, bc_bottom_y_C]


    # def p_bottom_(x):
    #     return np.full_like(x[1], 0)
    # def p_top_(x):
    #     return np.full_like(x[1], 0)
    # p_bottom_bcs = fem.Function(W3)
    # p_bottom_bcs.interpolate(p_bottom_)
    # p_top_bcs = fem.Function(W3)
    # p_top_bcs.interpolate(p_top_)
    # facet_bottom_dofs = fem.locate_dofs_geometrical((W.sub(3), W.sub(3).collapse()[0]), Bottom)
    # facet_top_dofs = fem.locate_dofs_geometrical((W.sub(3), W.sub(3).collapse()[0]), Top)
    # bc_bottom_p = fem.dirichletbc(p_bottom_bcs, facet_bottom_dofs, W.sub(3))
    # bc_top_p = fem.dirichletbc(p_top_bcs, facet_top_dofs, W.sub(3))
    # bcs.append(bc_bottom_p)
    # bcs.append(bc_top_p)

    # Variational formulation
    if K == 'incompressible':
        # def nF(y_A, y_C):
        #     return (z_C * y_C + z_A * y_A) # n = 1
    
        # A = (
        #     inner(grad(phi), grad(v_1)) * dx
        #     - 1 / Lambda2 * nF(y_A, y_C) * v_1 * dx
        # ) + (
        #     inner(grad(p), grad(v_2)) * dx
        #     + 1 / a2 * nF(y_A, y_C) * dot(grad(phi), grad(v_2)) * dx
        # ) + (
        #     inner(grad(ln(y_A) + a2 * solvation * p - ln(1-y_A-y_C) + z_A * phi), grad(v_A)) * dx
        #     + inner(grad(ln(y_C) + a2 * solvation * p- ln(1-y_A-y_C) + z_C * phi), grad(v_C)) * dx
        # )
        # def nF(y_A, y_C):
        #     # n = const = 1
        #     return (z_C * y_C + z_A * y_A)

        # def J_A(y_A, y_C, phi, p):
        #     g_A = (solvation + 1) * a2 * (p - 1) # g_Aref, but constant and take gradient
        #     mu_A = g_A + ln(y_A)
        #     g_N = a2 * (p - 1) # solvation_N = 0, g_Sref, but constant and take gradient
        #     mu_N = g_N + ln(1 - y_A - y_C)
        #     return grad(mu_A - mu_N + z_A * phi)
        #     # return grad(ln(y_A) - ln(1 - y_A - y_C) + z_A * phi)
        
        # def J_C(y_A, y_C, phi, p):
        #     g_C = (solvation + 1) * a2 * (p - 1) # g_Cref, but constant and take gradient
        #     mu_C = g_C + ln(y_C)
        #     g_N = a2 * (p - 1)
        #     mu_N = g_N + ln(1 - y_A - y_C)
        #     return grad(mu_C - mu_N + z_C * phi)
        #     # return grad(ln(y_C) - ln(1 - y_A - y_C) + z_C * phi)

        def nF(y_A, y_C):
            return (z_C * y_C + z_A * y_A)
        
        # Diffusion fluxes for species A and C
        def J_A(y_A, y_C, phi, p):
            return grad(ln(y_A) + a2 * (p - 1) * (solvation + 1) + z_A * phi)
        
        def J_C(y_A, y_C, phi, p):
            return grad(ln(y_C) + a2 * (p - 1) * (solvation + 1) + z_C * phi)

        # if PoissonBoltzmann:
        #     def J_A(y_A, y_C, phi, p):
        #         return grad(ln(y_A) + z_A * phi)
        #     def J_C(y_A, y_C, phi, p):
        #         return grad(ln(y_C) + z_C * phi)

        A = (
            inner(grad(phi), grad(v_1)) * dx
            - 1 / Lambda2 * nF(y_A, y_C) * v_1 * dx
        ) + (
            inner(grad(p), grad(v_2)) * dx
            + 1 / a2 * nF(y_A, y_C) * dot(grad(phi), grad(v_2)) * dx
        ) + (
            inner(J_A(y_A, y_C, phi, p), grad(v_A)) * dx
            + inner(J_C(y_A, y_C, phi, p), grad(v_C)) * dx
        )

    # Define Neumann boundaries
    boundaries = [(0, Right_Top), (1, Right_Bottom), (2, Left_Top), (3, Left_Bottom)]
    facet_indices, facet_markers = [], []
    fdim = msh.topology.dim - 1
    for (marker, locator) in boundaries:
        facets = locate_entities(msh, fdim, locator)
        facet_indices.append(facets)
        facet_markers.append(np.full_like(facets, marker))
    facet_indices = np.hstack(facet_indices).astype(np.int32)
    facet_markers = np.hstack(facet_markers).astype(np.int32)
    sorted_facets = np.argsort(facet_indices)
    facet_tag = meshtags(msh, fdim, facet_indices[sorted_facets], facet_markers[sorted_facets])
    ds = Measure("ds", domain=msh, subdomain_data=facet_tag)
    L = 0
    L += (
        inner(g_phi, v_1) * ds(0)
        + inner(-g_phi, v_1) * ds(1)
        # Uncomment, if you want to apply the Neumann bcs on both sides/ left side
        # + inner(g_phi, v_1) * ds(2)
        # + inner(-g_phi, v_1) * ds(3)
    )

    F = A + L

    # Initialize initial guess for u
    y_C_init = fem.Function(W1)
    y_A_init = fem.Function(W0)
    y_C_init.interpolate(lambda x: np.full_like(x[0], y_C_bath))
    y_A_init.interpolate(lambda x: np.full_like(x[0], y_A_bath))

    with u.x.petsc_vec.localForm() as u_loc:
        u_loc.set(0)
    u.sub(0).interpolate(y_A_init)
    u.sub(1).interpolate(y_C_init)

    # Define Nonlinear Problem
    problem = NonlinearProblem(F, u, bcs=bcs)

    solver = NewtonSolver(MPI.COMM_WORLD, problem)
    solver.convergence_criterion = 'residual' #"incremental"
    solver.rtol = rtol
    solver.relaxation_parameter = relax_param
    solver.max_it = max_iter
    solver.report = True

    # Solve the problem
    log.set_log_level(log.LogLevel.INFO)
    n, converged = solver.solve(u)
    assert (converged)
    print(f"Number of interations: {n:d}")

    # Extract solution
    y_A_vector = u.sub(0).collapse().x.array
    y_C_vector = u.sub(1).collapse().x.array
    phi_vector = u.sub(2).collapse().x.array
    p_vector = u.sub(3).collapse().x.array

    X = W.sub(0).collapse()[0].tabulate_dof_coordinates()
    x_vector = [X[:, 0], X[:, 1]]

    if return_type == 'Vector':
        return y_A_vector, y_C_vector, phi_vector, p_vector, x_vector
    elif return_type == 'Extended':
        return y_A_vector, y_C_vector, phi_vector, p_vector, x_vector, u
    else:
        raise ValueError('Invalid return_type')

if __name__ == '__main__': # pragma: no cover # dont cover main in coverage
    phi_bias = 10#10
    Bias_type = 'ForwardBias' # 'ForwardBias', 'NoBias', 'BackwardBias'
    g_phi = 350#5
    y_fixed = 0.01#0.01
    z_A = -1.0
    z_C = 1.0
    K = 'incompressible'
    Lambda2 = 8.553e-6 # ! Change back to 1e-6
    # g_phi *= np.sqrt(Lambda2) # ! Unsure about this scaling
    # g_phi *= Lambda2
    # g_phi = g_phi / np.sqrt(Lambda2)
    a2 = 7.5412e-4
    number_cells = [20, 128]#[20, 100]
    Lx = 0.02
    Ly = 0.1
    x0 = np.array([0, 0])
    x1 = np.array([Lx, Ly])
    refinement_style = 'uniform'
    solvation = 5
    PoissonBoltzmann = False
    rtol = 1e-3
    relax_param = 0.15
    max_iter = 15_000

    # Solve the system
    y_A, y_C, phi, p, X = ElectrolyticDiode(Bias_type, phi_bias, g_phi, z_A, z_C, y_fixed, y_fixed, K, Lambda2, a2, number_cells, solvation, PoissonBoltzmann, relax_param, Lx, Ly, rtol, max_iter, return_type='Vector')
    x, y = X[0], X[1]
    y_S = 1 - y_A - y_C

    # Plot results
    levelsf = 10
    levels = 10    
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(8,10))

    c = axs[0,0].tricontourf(x, y, y_A, levelsf)
    fig.colorbar(c)
    axs[0,0].tricontour(x, y, y_A, levels, colors='black')
    axs[0,0].set_title('$y_A$')

    c = axs[0,1].tricontourf(x, y, y_C, levelsf)
    fig.colorbar(c)
    axs[0,1].tricontour(x, y, y_C, levels, colors='black')
    axs[0,1].set_title('$y_C$')

    c = axs[0,2].tricontourf(x, y, y_S, levelsf)
    fig.colorbar(c)
    axs[0,2].tricontour(x, y, y_S, levels, colors='black')
    axs[0,2].set_title('$y_S$')

    c = axs[1,0].tricontourf(x, y, phi, levelsf)
    fig.colorbar(c)
    axs[1,0].tricontour(x, y, phi, levels, colors='black')
    axs[1,0].set_title('$\\varphi$')

    c = axs[1,1].tricontourf(x, y, p, levelsf)
    fig.colorbar(c)
    axs[1,1].tricontour(x, y, p, levels, colors='black')
    axs[1,1].set_title('$p$')

    fig.tight_layout()
    fig.show() 