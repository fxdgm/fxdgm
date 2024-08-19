'''
Jan Habscheid
Jan.Habscheid@rwth-aachen.de
'''

import numpy as np


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

def Q_DL_dimless_ana(y_A_R:float, y_C_R:float, y_N_R:float, z_A:float, z_C:float, phi_L:float, phi_R:float, p_R:float, Lambda2:float, a2:float, kappa:float) -> float:
    '''
    Calculates charge of the system using the analytical method in dimensionless units

    Q = sgn(φᴸ −φᴿ)λ√(2/(κ+1))(√(Λᴸ)−√(Λᴿ))

    with 
    Λ = ln(∑_α D_α exp(−z_α φ + Eₚ a²)

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
        Electric potential at the left boundary
    phi_R : float
        Electric potential at the right boundary
    p_R : float
        Pressure at the right boundary
    Lambda2 : float
        Dimensionless parameter
    a2 : float
        Dimensionless parameter
    kappa : float
        Solvation number

    Returns
    -------
    float
        Charge of the system in dimensionless units
    '''
    z_N = 0
    D_A = y_A_R / (np.exp(-a2*p_R-z_A*phi_R))
    D_C = y_C_R / (np.exp(-a2*p_R-z_C*phi_R))
    D_N = y_N_R / (np.exp(-a2*p_R-z_N*phi_R))
    E_p = p_R
    CLambda_L = np.log(D_A * np.exp(-z_A * phi_L + E_p * a2) + D_C * np.exp(-z_C * phi_L + E_p * a2) + D_N * np.exp(-z_N * phi_L + E_p * a2))
    CLambda_R = np.log(D_A * np.exp(-z_A * phi_R + E_p * a2) + D_C * np.exp(-z_C * phi_R + E_p * a2) + D_N * np.exp(-z_N * phi_R + E_p * a2))
    Lambda = np.sqrt(Lambda2)
    Q_DL = (phi_L-phi_R) / np.abs(phi_L-phi_R) * Lambda * np.sqrt(2/(kappa+1)) * (np.sqrt(CLambda_L) - np.sqrt(CLambda_R))
    return Q_DL

def Q_DL_dim_ana(y_A_R:float, y_C_R:float, y_N_R:float, z_A:float, z_C:float, phi_L:float, phi_R:float, p_R:float, Lambda2:float, a2:float, nR_m:float, e0:float, LR:float, kappa:float) -> float:
    '''
    Calculates charge of the system using the analytical method in dimensionless units

    Q = sgn(φᴸ −φᴿ)λ√(2/(κ+1))(√(Λᴸ)−√(Λᴿ))

    with 
    Λ = ln(∑_α D_α exp(−z_α φ + Eₚ a²)

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
        Value of electric potential at the left boundary
    phi_R : float
        Value of electric potential at the right
    p_R : float
        Value of pressure at the right boundary
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
    kappa : float
        Solvation number

    Returns
    -------
    float
        Charge of the system in µAs/cm³
    '''
    Q_DL = Q_DL_dimless_ana(y_A_R, y_C_R, y_N_R, z_A, z_C, phi_L, phi_R, p_R, Lambda2, a2, kappa)
    Q_DL *= nR_m * e0 * LR
    Q_DL *= 1e+6 
    Q_DL *= 1/(1e+4)
    return Q_DL