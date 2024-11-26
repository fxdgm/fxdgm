__author__ = "Jan Habscheid <Jan.Habscheid@rwth-aachen.de>"

from .ElectrolyticDiode import ElectrolyticDiode
from .Eq02 import solve_System_2eq
from .Eq04 import solve_System_4eq, create_refined_mesh
from .EqN import solve_System_Neq
from .Helper_DoubleLayerCapacity import *
from .RefinedMesh1D import create_refined_mesh