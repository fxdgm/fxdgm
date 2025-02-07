# Jan Habscheid
# Jan.Habscheid@rwth-aachen.de

import numpy as np
from scipy.optimize import fixed_point, fsolve


# Helper functions
def Phi_pot_center(Phi_pot:np.ndarray) -> np.ndarray:
    '''
    Returns vector with the center of the electric potential values.

    Parameters
    ----------
    Phi_pot : np.ndarray
        Input vector with electric potential values.

    Returns
    -------
    np.ndarray
        Vector with the center of the electric potential values.
    '''
    return (Phi_pot[1:] + Phi_pot[:-1]) / 2

def dx(Phi_pot:np.ndarray) -> float:
    '''
    Returns the difference between the first two electric potential values.
    
    Assumes that the electric potential values are equally spaced.

    Parameters
    ----------
    Phi_pot : np.ndarray
        Input vector with electric potential values.

    Returns
    -------
    float
        Difference between the first two electric potential values.
    '''
    return Phi_pot[1] - Phi_pot[0]

def C_dl(Q_DL:np.ndarray, Phi_pot:np.ndarray) -> np.ndarray:
    '''
    Double Layer Capacity

    Parameters
    ----------
    Q_DL : np.ndarray
        Charge of the system
    Phi_pot : np.ndarray
        Electric potential values

    Returns
    -------
    np.ndarray
        Double Layer Capacity
    '''
    return (Q_DL[1:] - Q_DL[:-1]) / dx(Phi_pot)

def n(p:np.ndarray, K:str|float) -> np.ndarray:
    '''
    Calculates the total number density

    Parameters
    ----------
    p : np.ndarray
        Pressure
    K : str | float
        Bulk modulus, use 'incompressible' for an incompressible mixture

    Returns
    -------
    np.ndarray
        Total number density
    '''
    if K == 'incompressible':
        return np.ones_like(p)
    n_Dimensionless = (p-1) / K + 1
    return n_Dimensionless

def Q_num_(y_A:np.ndarray, y_C:np.ndarray, n:np.ndarray, x:np.ndarray, z_A:float=-1.0, z_C:float=1.0) -> float:
    '''
    Calculates the charge of the system

    Q = ∫_Ω n^F dΩ

    Parameters
    ----------
    y_A : np.ndarray
        Anion fraction
    y_C : np.ndarray
        Cation fraction
    n : np.ndarray
        Total number density
    x : np.ndarray
        Spatial discretization
    z_A : float, optional
        Charge number of anions, by default -1.0
    z_C : float, optional
        Charge number of cations, by default 1.0

    Returns
    -------
    float
        Charge of the system
    '''
    nF_dimensionless = (z_C * y_C + z_A * y_A) * n
    nF_int = -np.trapz(nF_dimensionless, x)
    return nF_int

def Q_num_dim(y_A:np.ndarray, y_C:np.ndarray, n:np.ndarray, x:np.ndarray, z_A:float, z_C:float, nR_m:float, e0:float, LR:float) -> float:
    '''
    Calculates the charge of the system

    Q = ∫_Ω n^F dΩ

    Parameters
    ----------
    y_A : np.ndarray
        Anion fraction
    y_C : np.ndarray
        Cation fraction
    n : np.ndarray
        Total number density
    x : np.ndarray
        Spatial discretization
    z_A : float, optional
        Charge number of anions, by default -1.0
    z_C : float, optional
        Charge number of cations, by default 1.0
    nR_m : float
        Reference number density in 1/m^3
    e0 : float
        Dielectric constant
    LR : float
        Reference length in m

    Returns
    -------
    float
        Charge of the system
    '''
    Q_DL = Q_num_(y_A, y_C, n, x, z_A, z_C)
    Q_DL *= nR_m * e0 * LR
    Q_DL *= 1e+6 
    Q_DL *= 1/(1e+4)
    return Q_DL

def Q_DL_dimless_ana(y_A_R:float, y_C_R:float, y_N_R:float, z_A:float, z_C:float, phi_L:float, phi_R:float, p_R:float, K:str|float, Lambda2:float, a2:float, solvation:float) -> float:
    '''
    Calculates charge of the system using the analytical method in dimensionless units

    Q = λ^2(∂ₓ φᴸ − ∂ₓ  φᴿ)

    Parameters
    ----------
    y_A_R : float
        Value of anion fraction at the right boundary
    y_C_R : float
        Value of cation fraction at the right boundary
    y_N_R : float
        Value of neutral fraction at the right boundary
    z_A : float
        Charge number of anions
    z_C : float
        Charge number of cations
    phi_L : float
        Electric potential at the left boundary [V]
    phi_R : float
        Electric potential at the right boundary
    p_R : float
        Pressure at the right boundary
    K : str | float
        Bulk modulus, use 'incompressible' for an incompressible mixture
    Lambda2 : float
        Dimensionless parameter
    a2 : float
        Dimensionless parameter
    solvation : float
        Solvation number

    Returns
    -------
    float
        Charge of the system in dimensionless units
    '''
    if solvation != 0:
        raise ValueError('Solvation number must be 0 for the analytical method')
    z_N = 0
    E_p = p_R
    if K == 'incompressible':
        # Assume E_p = p_R = 0        
        D_A = y_A_R / (np.exp(-a2*p_R-z_A*phi_R))
        D_C = y_C_R / (np.exp(-a2*p_R-z_C*phi_R))
        D_N = y_N_R / (np.exp(-a2*p_R))

        # Analytical method
        E_p = p_R
        CLambda_L = np.log(D_A * np.exp(-z_A * phi_L - E_p) + D_C * np.exp(-z_C * phi_L - E_p) + D_N * np.exp(-z_N * phi_L - E_p))

        Lambda = np.sqrt(Lambda2)
        Q_DL = (phi_L-phi_R) / np.abs(phi_L-phi_R) * Lambda * np.sqrt(2) * (np.sqrt(CLambda_L))
        return Q_DL
    else:
        C_A = y_A_R / ((K + p_R  - 1)**(-1*a2*K)*np.exp(-z_A*phi_R))
        C_C = y_C_R / ((K + p_R  - 1)**(-1*a2*K)*np.exp(-z_C*phi_R))
        C_N = y_N_R / ((K + p_R  - 1)**(-1*a2*K)*np.exp(-z_N*phi_R))

        CLambda_L = C_A * np.exp(-z_A*phi_L) + C_C * np.exp(-z_C*phi_L) + C_N

        Left = np.sqrt((1/CLambda_L)**(-1/(a2*K)) + 1 - K - E_p)

        Lambda = np.sqrt(Lambda2)
        a = np.sqrt(a2)

        Q_DL = (phi_L-phi_R) / np.abs(phi_L-phi_R) * Lambda * a * np.sqrt(2) * (Left)# - Right)
        return Q_DL
    raise ValueError('Invalid input for K')

def Q_DL_dim_ana(y_A_R:float, y_C_R:float, y_N_R:float, z_A:float, z_C:float, phi_L:float, phi_R:float, p_R:float, K:str|float, Lambda2:float, a2:float, nR_m:float, e0:float, LR:float, solvation:float) -> float:
    '''
    Calculates charge of the system using the analytical method in dimensionless units

    Q = λ^2(∂ₓ φᴸ − ∂ₓ  φᴿ)

    Parameters
    ----------
    y_A_R : float
        Value of anion fraction at the right boundary
    y_C_R : float
        Value of cation fraction at the right boundary
    y_N_R : float
        Value of neutral fraction at the right boundary
    z_A : float
        Charge number of anions
    z_C : float
        Charge number of cations
    phi_L : float
        Value of electric potential at the left boundary (dimensionless units)
    phi_R : float
        Value of electric potential at the right
    p_R : float
        Value of pressure at the right boundary
    K : str | float
        Bulk modulus, use 'incompressible' for an incompress
    Lambda2 : float
        Dimensionless parameter
    a2 : float
        Dimensionless parameter
    nR_m : float
        Reference number density in 1/m^3
    e0 : float
        Dielectric constant
    LR : float
        Reference length in m
    solvation : float
        Solvation number

    Returns
    -------
    float
        Charge of the system in µAs/cm³
    '''
    Q_DL = Q_DL_dimless_ana(y_A_R, y_C_R, y_N_R, z_A, z_C, phi_L, phi_R, p_R, K, Lambda2, a2, solvation)
    Q_DL *= nR_m * e0 * LR
    Q_DL *= 1e+6 
    Q_DL *= 1/(1e+4)
    return Q_DL



def C_DL_dimless_ana(y_A_R:float, y_C_R:float, y_N_R:float, z_A:float, z_C:float, phi_L:float, phi_R:float, p_R:float, K:str|float, Lambda2:float, a2:float, solvation:float) -> float:
    '''
    Calculates the double layer capacity of the system using the analytical method in dimensionless units

    C_dl = ∂Q/∂ φᴸ

    Parameters
    ----------
    y_A_R : float
        Value of anion fraction at the right boundary
    y_C_R : float
        Value of cation fraction at the right boundary
    y_N_R : float
        Value of neutral fraction at the right boundary
    z_A : float
        Charge number of anions
    z_C : float
        Charge number of cations
    phi_L : float
        Electric potential at the left boundary [V]
    phi_R : float
        Electric potential at the right boundary
    p_R : float
        Pressure at the right boundary
    K : str | float
        Bulk modulus, use 'incompressible' for an incompressible mixture
    Lambda2 : float
        Dimensionless parameter
    a2 : float
        Dimensionless parameter
    solvation : float
        Solvation number

    Returns
    -------
    float
        Double layer capacity of the system in dimensionless units
    '''
    if solvation != 0:
        raise ValueError('Solvation number must be 0 for the analytical method')
    z_N = 0
    E_p = p_R
    if K == 'incompressible':
        # Assume E_p = p_R = 0        
        D_A = y_A_R / (np.exp(-a2*p_R-z_A*phi_R))
        D_C = y_C_R / (np.exp(-a2*p_R-z_C*phi_R))
        D_N = y_N_R / (np.exp(-a2*p_R))

        CLambda_L = np.log(D_A * np.exp(-z_A * phi_L - E_p * a2) + D_C * np.exp(-z_C * phi_L - E_p * a2) + D_N * np.exp(-z_N * phi_L - E_p * a2))

        xi_CLambda_L = D_A * np.exp(-z_A * phi_L - E_p * a2) + D_C * np.exp(-z_C * phi_L - E_p * a2) + D_N * np.exp(-z_N * phi_L - E_p * a2)
        dxi_CLambda_L = - D_A * z_A * np.exp(-z_A * phi_L - E_p * a2) - D_C * z_C * np.exp(-z_C * phi_L - E_p * a2) - D_N * z_N * np.exp(-z_N * phi_L - E_p * a2)

        Lambda = np.sqrt(Lambda2)

        PreTerm = (phi_L-phi_R) / np.abs(phi_L-phi_R) * Lambda * np.sqrt(2)
        DerivedTerm = dxi_CLambda_L / (2 * xi_CLambda_L * np.sqrt(np.log(xi_CLambda_L)))
        
        return PreTerm * DerivedTerm
    else:
        C_A = y_A_R / ((K + p_R  - 1)**(-1*a2*K)*np.exp(-z_A*phi_R))
        C_C = y_C_R / ((K + p_R  - 1)**(-1*a2*K)*np.exp(-z_C*phi_R))
        C_N = y_N_R / ((K + p_R  - 1)**(-1*a2*K)*np.exp(-z_N*phi_R))
        
        z = 1 - K - E_p
        y = 1/(a2*K)

        CLambda = C_A * np.exp(-z_A*phi_L) + C_C * np.exp(-z_C*phi_L) + C_N * np.exp(-z_N*phi_L)
        dClambda = -C_A * z_A * np.exp(-z_A*phi_L) - C_C * z_C * np.exp(-z_C*phi_L) - C_N * z_N * np.exp(-z_N*phi_L)

        Lambda = np.sqrt(Lambda2)
        a = np.sqrt(a2)

        DerivedTerm = y * CLambda**(y-1) * dClambda / (2 * np.sqrt(CLambda**y + z))

        PreTerm = (phi_L-phi_R) / np.abs(phi_L-phi_R) * Lambda * a * np.sqrt(2)

        return PreTerm * DerivedTerm
    raise ValueError('Invalid input for K')



def C_DL_dim_ana(y_A_R:float, y_C_R:float, y_N_R:float, z_A:float, z_C:float, phi_L:float, phi_R:float, p_R:float, K:str|float, Lambda2:float, a2:float, nR_m:float, e0:float, LR:float, k:float, T:float, solvation:float) -> float:
    '''
    Calculates the double layer capacity of the system using the analytical method in dimensionless units

    C_dl = ∂Q/∂ φᴸ

    Parameters
    ----------
    y_A_R : float
        Value of anion fraction at the right boundary
    y_C_R : float
        Value of cation fraction at the right boundary
    y_N_R : float
        Value of neutral fraction at the right boundary
    z_A : float
        Charge number of anions
    z_C : float
        Charge number of cations
    phi_L : float
        Value of electric potential at the left boundary (dimensionless units)
    phi_R : float
        Value of electric potential at the right
    p_R : float
        Value of pressure at the right boundary
    K : str | float
        Bulk modulus, use 'incompressible' for an incompress
    Lambda2 : float
        Dimensionless parameter
    a2 : float
        Dimensionless parameter
    nR_m : float
        Reference number density in 1/m^3
    e0 : float
        Dielectric constant
    LR : float
        Reference length in m
    k : float
        Boltzmann constant
    T : float
        Temperature
    solvation : float
        Solvation number

    Returns
    -------
    float
        Double layer capacity of the system in µAs/cm²
    '''
    C_DL = C_DL_dimless_ana(y_A_R, y_C_R, y_N_R, z_A, z_C, phi_L, phi_R, p_R, K, Lambda2, a2, solvation)
    C_DL *= nR_m * e0 * LR
    # ! ToDo
    C_DL *= 1e+6
    C_DL *= 1/(1e+4) 
    C_DL *= 1 /(k*T/e0)
    return C_DL