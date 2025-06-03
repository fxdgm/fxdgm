fxdgm
=====

.. image:: https://git.rwth-aachen.de/janhab/fxdgm/badges/main/pipeline.svg
   :target: https://git.rwth-aachen.de/JanHab/fxdgm/pipelines
.. image:: https://img.shields.io/badge/docs-latest-blue
   :target: https://janhab.pages.rwth-aachen.de/fxdgm/
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.15388656.svg
   :target: https://doi.org/10.5281/zenodo.15388656
.. image:: https://img.shields.io/badge/version-1.1.1-blue.svg
   :target: https://git.rwth-aachen.de/janhab/fxdgm/-/tags

*A nonlinear, mixed finite element solver for the DGM electrolyte model*

.. image:: ../../media/logo.svg
   :width: 300px

Physical Background
===================

| The system, which is solved, refers to the original work, `Overcoming the shortcomings of the Nernst–Planck model <https://doi.org/10.1039/C3CP44390F>`_, from Wolfgang Dreyer, Clemens Guhlke and Rüdiger Müller in 2013.
| This paper introduces a **new, generalized Nernst-Planck model, which is thermodynamically consistent**, as the classical Nernst-Planck model fails to predict the correct ion-concentrations close to the boundaries.
| The open-source package `FEniCSx <https://fenicsproject.org/>`_ was used for the numerical implementation.

Main Features
=============

- Solving stationary `DGM <https://doi.org/10.1039/C3CP44390F>`_ model in dimensionless units

   - for a ternary electrolyte (cations, anions, neutral solvent)

   - for an electrolyte of N arbitrary species

- Local mesh refinement for one-dimensional domains towards the electrode

- `Testcases <https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/tests?ref_type=heads>`_ for the one-dimensional case or the two-dimensional electrolytic diode

- Solutions for the `Double-Layer Capacity <https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples/ReproducableCode/DoubleLayerCapacity?ref_type=heads>`_, both numerical and analytical

- `Numerical Convergence <https://git.rwth-aachen.de/JanHab/fxdgm/-/blob/main/examples/ReproducableCode/Convergence.py?ref_type=heads>`_ with relaxation parameter for newtons method

- Two-dimensional testcases for the example of the `electrolytic diode <https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples/ReproducableCode/ElectrolyticDiode?ref_type=heads>`_


Installation
============
| First, install the **FEniCSx**  and the necessary compiler via conda and after the **fxdgm** package with pip.
| The necessary dependencies can be installed with

.. code-block:: 
   
   conda install -c conda-forge fenics-dolfinx=0.9.0 mpich=4.3.0 pyvista=0.43.10 c-compiler=1.9.0 cxx-compiler=1.9.0 fortran-compiler=1.9.0 -y
   git clone https://git.rwth-aachen.de/JanHab/fxdgm.git
   cd fxdgm
   pip install .

| It is also possible to install the FEniCSx backend in a different manner. See the `FEniCSx documentation <https://fenicsproject.org/download/>`_ for this.
| Although this installation method should work, it was not tested for the purpose of this package.

Alternative installation using Docker
-------------------------------------  

| Alternatively, the FEniCSx backend and the fxdgm package can be installed at once using Docker.

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

| Find the package source code in `fxdgm <https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/fxdgm?ref_type=heads>`_
| This implements the nonlinear electrolyte model.

| Furthermore, some physical examples are provided in the `examples <https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples?ref_type=heads>`_ folder.
| In the subfolder `ReproducableCode <https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples/ReproducableCode?ref_type=heads>`_ is the code, to execute the calculations with some first visualizations.
| The subfolder `Data <https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples/Data?ref_type=heads>`_ stores the data for all the simulations in a \*.npz file, which can be read with numpy `np.load(file.npz)`.
| `visualizations <https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples/Visualizations?ref_type=heads>`_ creates the necessary figures from the thesis and stores them either in \*.svg or \*.pdf format in "Figures".

Contact
=======

- Jan Habscheid
   - Jan.Habscheid@rwth-aachen.de

- Dr. Satyvir Singh
   - ACoM - Applied and Computational Mathematics
   - RWTH Aachen University
   - singh@acom.rwth-aachen.de

- Dr. Lambert Theisen
   - ACoM - Applied and Computational Mathematics
   - RWTH Aachen University
   - theisen@acom.rwth-aachen.de

- Dr. Stefanie Braun
   - ACoM - Applied and Computational Mathematics
   - RWTH Aachen University
   - braun@acom.rwth-aachen.de

- Prof. Dr. Manuel Torrilhon
   - ACoM - Applied and Computational Mathematics
   - RWTH Aachen University
   - mt@acom.rwth-aachen.de

.. toctree::
   src/oneD
   src/ElectrolyticDiode
   src/Miscellaneous
   example
   :maxdepth: 2
   :caption: fxdgm
   :hidden:

