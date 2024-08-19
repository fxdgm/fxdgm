# Reproducibility Repository for: Numerical Treatment of a Thermodynamically Consistent Electrolyte Model (B.Sc. Thesis - Jan Habscheid)

## Thesis

This repository contains the code to reproduce the results presented in the bachelor thesis: Numerical Treatment of a Thermodynamically Consistent Electrolyte Model
Find the thesis at:
    - Insert link to thesis

### Abstract

- Insert Abstract from thesis

## Installation

As a numerical solver, mainly FEniCSx was used and installed via conda.

```
conda create --name fenicsx-env python=3.12.3 -y
conda activate fenicsx-env
conda install -c conda-forge fenics-dolfinx=0.8.0 mpich=4.2.1 pyvista=0.43.10 matplotlib=3.8.4 numpy=1.26.4 scipy=1.14.0 -y
```

### Alternative installation

Use the "environment.yml" file to install all necessary environments

```
conda env create -f environment.yml
```

## Usage


## Contact

**Author**
- Jan Habscheid
Jan.Habscheid@rwth-aachen.de

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