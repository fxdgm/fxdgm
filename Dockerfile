# Start with a base image that includes conda
FROM continuumio/miniconda3

# Set environment variables
ENV CONDA_DEFAULT_ENV=fxdgm
ENV PATH /opt/conda/envs/${CONDA_DEFAULT_ENV}/bin:$PATH
ENV HOME /root

# Create the environment and install packages
# FEniCSx backend + documentation and testing dependencies
RUN conda create --name ${CONDA_DEFAULT_ENV} python=3.12.3 -y # && \
    conda install -n ${CONDA_DEFAULT_ENV} -c conda-forge fenics-dolfinx=0.8.0 mpich=4.2.1 pyvista=0.43.10 gcc=12.4.0 sphinx=7.3.7 myst-parser=4.0.0 sphinx-copybutton=0.5.2 sphinx-rtd-theme=3.0.1 pytest==8.3.3 -y
# fxdgm package from git
RUN pip install git+https://git.rwth-aachen.de/JanHab/bsc-electrolytemodels@Package
# Activate environment
SHELL ["conda", "run", "-n", "fenicsx-env", "/bin/bash", "-c"]

# WORKDIR /root
WORKDIR /solver

# Set the default environment on container start
# ENTRYPOINT ["conda", "run", "-n", "fenicsx-env", "/bin/bash", "-c"]
CMD ["bash"]
