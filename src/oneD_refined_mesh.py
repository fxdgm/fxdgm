'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import numpy as np
from mpi4py import MPI
from dolfinx import mesh
from ufl import Mesh


# Define mesh
def create_refined_mesh(refinement_style:str, number_cells:int) -> Mesh:
    '''
    Creates a one-dimensional mesh with a refined region at the left boundary

    Parameters
    ----------
    refinement_style : str
        How the mesh should be refined. Options are 'log', 'hard_log', 'hard_hard_log'
    number_cells : int
        Number of cells in the mesh

    Returns
    -------
    Mesh
        One-dimensional mesh, ready for use in FEniCSx
    '''
    if refinement_style == 'log':
        coordinates_np = (np.logspace(0, 1, number_cells+1) - 1) / 9
    elif refinement_style == 'hard_log':
        coordinates_np1 = (np.logspace(0,1,int(number_cells*0.9)+1,endpoint=False)-1)/9 * 0.1
        coordinates_np2 = 0.1 + (np.logspace(0,1,int(number_cells*0.1)+1)-1)/9 * 0.9
        coordinates_np = np.concatenate((coordinates_np1, coordinates_np2), axis=0)
    elif refinement_style == 'hard_hard_log':
        coordinates_np1 = (np.logspace(0,1,int(number_cells*0.9)+1,endpoint=False)-1)/9 * 0.004
        coordinates_np2 = 0.004 + (np.logspace(0,1,int(number_cells*0.1)+1)-1)/9 * 0.996
        coordinates_np = np.concatenate((coordinates_np1, coordinates_np2), axis=0)
    num_vertices = len(coordinates_np)
    num_cells = num_vertices - 1
    cells_np = np.column_stack((np.arange(num_cells), np.arange(1, num_cells+1)))
    gdim = 1
    shape = 'interval' # 'interval', 'triangle', 'quadrilateral', 'tetrahedron', 'hexahedron'
    degree = 1
    domain = Mesh(element("Lagrange", shape, 1, shape=(1,)))
    coordinates_np_ = []
    [coordinates_np_.append([coord]) for coord in coordinates_np]
    msh = mesh.create_mesh(MPI.COMM_WORLD, cells_np, coordinates_np_, domain)
    return msh