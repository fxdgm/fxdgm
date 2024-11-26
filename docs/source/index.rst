fxdgm
==========

.. image:: https://git.rwth-aachen.de/Jan.Habscheid/bsc-electrolytemodels/badges/main/pipeline.svg
   :target: https://git.rwth-aachen.de/JanHab/bsc-electrolytemodels/pipelines
.. image:: https://img.shields.io/badge/docs-latest-blue
   :target: https://janhab.pages.rwth-aachen.de/bsc-electrolytemodels/
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.13645296.svg
   :target: https://doi.org/10.5281/zenodo.13645296
.. image:: https://img.shields.io/badge/version-1.0-blue.svg
   :target: https://git.rwth-aachen.de/janhab/bsc-electrolytemodels/-/tags

*A nonlinear, mixed finite element solver for the DGM electrolyte model*

Physical Background
===================


| Batteries play a crucial role in the energy transition. The production of green energy depends on external factors. Storing energy in batteries is necessary to access green energy at any time.
| Better optimized batteries are essential for the future. Lifetime, loading time, and energy loss are just some aspects that must be improved to prepare for a greener future. Numerical simulations are crucial to understanding and optimizing batteries' behavior. Those simulations enable researchers to test many different materials without considerable additional expenses to, for example, find the best combination of anions and cations.
| The classical Nernst-Planck model for the ion transport in an electrolyte fails to predict the correct concentration in the boundaries of the electrolyte. The code in this repository solves a thermodynamically consistent electrolyte model with dimensionless units under isothermal conditions. A simplified version of the system for the one-dimensional equilibrium of an ideal mixture and the incompressible limit are considered, too. The numerical implementation is done with the open-source software FEniCSx. Furthermore, the influence of different boundary conditions, material parameters, solvation, and compressibility on the electric potential, pressure, and ion concentration can be investigated, and the model can be compared with the classical Nernst-Planck model. Examples of the double layer capacity and electrolytic diode can be recreated.

| The system, which is solved, refers to the original work, `Overcoming the shortcomings of the Nernst–Planck model <https://doi.org/10.1039/C3CP44390F>`_, from Wolfgang Dreyer, Clemens Guhlke and Rüdiger Müller in 2013.

Main Features
=============

- Solving steady DGM model in dimensionless units
- Testcases for the one-dimensional case or the two-dimensional electrolytic diode
- Solutions for the Double-Layer Capacity, both numerical and analytical
- Numerical Convergence with relaxation parameter for newtons method
- Local mesh refinement for one-dimensional domains

Installation
============
| Install the fxdgm package with pip to get all the implemented functions.

.. code-block:: 
   
   pip install git+https://git.rwth-aachen.de/JanHab/bsc-electrolytemodels

| For the backend, FEniCSx was used and installed via conda.
| The necessery dependencies can be installed with

.. code-block:: 

   conda install -c conda-forge fenics-dolfinx=0.8.0 mpich=4.2.1 pyvista=0.43.10 gcc=12.4.0 -y

| It is also possible to install the FEniCSx backend in a different manner. See the [FEniCSx documentation](https://fenicsproject.org/download/) for this.
| Although this installation method should work, it was not tested for the purpose of this package.

macOS installation using Docker
-------------------------------

| The docker installation method works for linux too. It was not tested on windows.

.. code-block::

   docker compose build
   docker compose run solver

Testing
=======

| For testing clone the repository, install pytest and run the tests with

.. code-block::

   pip install pytest==8.3.3
   python -m pytest


Usage
=====

| Find the package source code in `src <https://git.rwth-aachen.de/JanHab/bsc-electrolytemodels/-/tree/main/src?ref_type=heads>`_
| This implements the nonlinear electrolyte model.

| Furthermore, some physical examples are provided in the `examples <https://git.rwth-aachen.de/JanHab/bsc-electrolytemodels/-/tree/main/examples?ref_type=heads>`_ folder.
| In the subfolder `ReproducableCode <https://git.rwth-aachen.de/JanHab/bsc-electrolytemodels/-/tree/main/examples/ReproducableCode?ref_type=heads>`_ is the code, to execute the calculations with some first visualizations.
| The subfolder `Data <https://git.rwth-aachen.de/JanHab/bsc-electrolytemodels/-/tree/main/examples/Data?ref_type=heads>`_ stores the data for all the simulations in a \*.npz file, which can be read with numpy `np.load(file.npz)`.
| `visualizations <https://git.rwth-aachen.de/JanHab/bsc-electrolytemodels/-/tree/main/examples/Visualizations?ref_type=heads>`_ creates the necessary figures from the thesis and stores them either in \*.svg or \*.pdf format in "Figures".

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

