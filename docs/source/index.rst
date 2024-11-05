.. Reproducibility Repository for: Numerical Treatment of a Thermodynamically Consistent Electrolyte Model documentation master file, created by
   sphinx-quickstart on Tue Sep  3 10:16:31 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Reproducibility Repository for Numerical Treatment of a Thermodynamically Consistent Electrolyte Model documentation
=====================================================================================================================

.. admonition:: \ \

   This python package has the purpose to make the implementation and the examples from the bachelor thesis "Numerical Treatment of a Thermodynamically Consistent Electrolyte Model" reproducible. The code is written in Python and uses the finite element library FEniCSx. The code is available at: https://doi.org/10.5281/zenodo.13645296

Thesis
======
| This repository contains the code to reproduce the results presented in the bachelor thesis: Numerical Treatment of a Thermodynamically Consistent Electrolyte Model
| Find the thesis at: https://doi.org/10.18154/RWTH-2024-09837

Abstract
========

| Batteries play a crucial role in the energy transition. The production of green energy depends on external factors. Storing energy in batteries is necessary to access green energy at any time.

| Better optimized batteries are essential for the future. Lifetime, loading time, and energy loss are just some aspects that must be improved to prepare for a greener future. Numerical simulations are crucial to understanding and optimizing batteries' behavior. Those simulations enable researchers to test many different materials without considerable additional expenses to, for example, find the best combination of anions and cations.

| The classical Nernst-Planck model for the ion transport in an electrolyte fails to predict the correct concentration in the boundaries of the electrolyte. This work will present and analyze a thermodynamically consistent electrolyte model with dimensionless units under isothermal conditions. A simplified version of the system for the one-dimensional equilibrium of an ideal mixture and the incompressible limit will be considered. The numerical implementation of the model with the open-source software FEniCSx will be discussed. Furthermore, the influence of different boundary conditions, material parameters, solvation, and compressibility on the electric potential, pressure, and ion concentration will be investigated, and the model will be compared with the classical Nernst-Planck model. Examples of the double layer capacity and electrolytic diode will be considered.

Installation
============
| As a numerical solver, mainly FEniCSx was used and installed via conda.
| All the calculations were performed on a Linux machine. According to the documentation, everything should work well on macOS, but this was not tested. FEniCSx offers some beta versions for Windows support, but it is recommended to use WSL2 instead.

.. code-block:: 
   
   conda create --name fenicsx-env python=3.12.3 -y
   conda activate fenicsx-env
   conda install -c conda-forge fenics-dolfinx=0.8.0 mpich=4.2.1 pyvista=0.43.10 matplotlib=3.8.4 numpy=1.26.4 scipy=1.14.0 -y

Alternative installation
========================
| Use the "environment.yml" file to install all necessary environments

.. code-block:: 

   conda env create -f environment.yml

Usage
=====
| Find the visualizations from the thesis and some extra calculations in the "examples" folder. 
| In the subfolder "ReproducableCode" is the code, to execute the calculations with some first visualizations.
| The subfolder "Data" stores the data for all the simulations in a ".npz" file, which can be read with numpy `np.load(file.npz)`. "Visualizations" creates the necessary figures from the thesis and stores them in ".svg" format in "Figures".
| In "src" there are the generic FEniCSx implementations, that were used to calculate the examples.

Contact
=======
**Author**

- Jan Habscheid
- Jan.Habscheid@rwth-aachen.de

**Supervisor**

- Dr. Lambert Theissen
- ACoM - Applied and Computational Mathematics
- RWTH Aachen University
- theisen@acom.rwth-aachen.de

**Supervisor**

- Prof. Dr. Manuel Torrilhon
- ACoM - Applied and Computational Mathematics
- RWTH Aachen University
- mt@acom.rwth-aachen.de

.. toctree::
   src
   example
   :maxdepth: 2
   :caption: Numerical Treatment of a Thermodynamically Consistent Electrolyte Model:
   :hidden:

