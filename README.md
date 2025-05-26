# fxdgm

[![Pipeline Status](https://git.rwth-aachen.de/janhab/fxdgm/badges/main/pipeline.svg)](https://git.rwth-aachen.de/janhab/fxdgm/pipelines)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://janhab.pages.rwth-aachen.de/fxdgm/)
[![coverage report](https://git.rwth-aachen.de/JanHab/fxdgm/badges/main/coverage.svg)](https://janhab.pages.rwth-aachen.de/fxdgm/htmlcov)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15388656.svg)](https://doi.org/10.5281/zenodo.15388656)
[![GitLab Version](https://img.shields.io/badge/version-1.1.1-blue.svg)](https://git.rwth-aachen.de/janhab/fxdgm/-/tags)
[![License](https://img.shields.io/badge/license-GPLv3-blue)](https://git.rwth-aachen.de/janhab/fxdgm/-/blob/main/LICENSE?ref_type=heads)

*A nonlinear, mixed finite element solver for the DGM electrolyte model*

<img src="media/logo.svg" alt="Logo" width="200" />

## Physical Background

The system, which is solved, refers to the original work, [Overcoming the shortcomings of the Nernst–Planck model](https://doi.org/10.1039/C3CP44390F), from Wolfgang Dreyer, Clemens Guhlke and Rüdiger Müller in 2013.\
This paper introduces a **new, generalized Nernst-Planck model, which is thermodynamically consistent**, as the classical Nernst-Planck model fails to predict the correct ion-concentrations close to the boundaries.
The open-source package [FEniCSx](https://fenicsproject.org/) was used for the numerical implementation.

## Main Features

- Solving steady [DGM](https://doi.org/10.1039/C3CP44390F) model in dimensionless units
  - for a ternary electrolyte (cations, anions, neutral solvent)
  - for an electrolyte of N arbitrary species
- Local mesh refinement for one-dimensional domains towards the electrode
- [Testcases](https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/tests?ref_type=heads) for the one-dimensional case or the two-dimensional electrolytic diode
- Solutions for the [Double-Layer Capacity](https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples/ReproducableCode/DoubleLayerCapacity?ref_type=heads), both numerical and analytical
- [Numerical Convergence](https://git.rwth-aachen.de/JanHab/fxdgm/-/blob/main/examples/ReproducableCode/Convergence.py?ref_type=heads) with relaxation parameter for newtons method
- Two-dimensional testcases for the example of the [electrolytic diode](https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples/ReproducableCode/ElectrolyticDiode?ref_type=heads)

## Installation

Install the **fxdgm** package with pip to get all the implemented functions.

``` bash
pip install git+https://git.rwth-aachen.de/JanHab/fxdgm
```

For the backend, **FEniCSx** was used and installed via conda.
The necessary dependencies can be installed with

``` bash
conda install -c conda-forge fenics-dolfinx=0.9.0 mpich=4.3.0 pyvista=0.43.10 gcc=13.3.0 -y
```

It is also possible to install the FEniCSx backend in a different manner. See the [FEniCSx documentation](https://fenicsproject.org/download/) for this.
Although this installation method should work, it was not tested for the purpose of this package.

### Alternative installation using Docker

Alternatively, the FEniCSx backend and the fxdgm package can be installed at once using Docker.

``` bash
docker compose build
docker compose run solver
```

### Testing

For testing clone the repository, install pytest and run the tests with

``` bash
pip install pytest==8.3.3
python -m pytest
```

## Usage

Find the package source code in [fxdgm](https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/fxdgm?ref_type=heads).
This implements the nonlinear electrolyte model.

Furthermore, some physical examples are provided in the [examples](https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples?ref_type=heads).
In the subfolder [ReproducableCode](https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples/ReproducableCode?ref_type=heads) is the code, to execute the calculations with some first visualizations.
The subfolder [Data](https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples/Data?ref_type=heads) stores the data for all the simulations in a *.npz file, which can be read with numpy `np.load(file.npz)`.
[Visualizations](https://git.rwth-aachen.de/JanHab/fxdgm/-/tree/main/examples/Visualizations?ref_type=heads) creates the necessary figures from the thesis and stores them either in *.svg or *.pdf format in "Figures".

## Contact

- **Jan Habscheid**:  
  - [Jan.Habscheid@rwth-aachen.de](mailto:Jan.Habscheid@rwth-aachen.de)
- **Dr. Satyvir Singh**
  - ACoM - Applied and Computational Mathematics
  - RWTH Aachen University
  - [singh@acom.rwth-aachen.de](mailto:singh@acom.rwth-aachen.de)
- **Dr. Lambert Theisen**
  - ACoM - Applied and Computational Mathematics
  - RWTH Aachen University
  - [theisen@acom.rwth-aachen.de](mailto:theisen@acom.rwth-aachen.de)
- **Dr. Stefanie Braun**
  - ACoM - Applied and Computational Mathematics
  - RWTH Aachen University
  - [braun@acom.rwth-aachen.de](mailto:braun@acom.rwth-aachen.de)
- **Prof. Dr. Manuel Torrilhon**
  - ACoM - Applied and Computational Mathematics
  - RWTH Aachen University
  - [mt@acom.rwth-aachen.de](mailto:mt@acom.rwth-aachen.de)
