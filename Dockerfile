# Start with a base image that includes conda
FROM continuumio/miniconda3

# Set environment variables
ENV CONDA_DEFAULT_ENV=fenicsx-env
ENV PATH /opt/conda/envs/${CONDA_DEFAULT_ENV}/bin:$PATH
ENV HOME /root

# Create the environment and install packages
RUN conda create --name ${CONDA_DEFAULT_ENV} python=3.12.3 -y && \
    conda install -n ${CONDA_DEFAULT_ENV} -c conda-forge fenics-dolfinx=0.8.0 mpich=4.2.1 pyvista=0.43.10 matplotlib=3.8.4 numpy=1.26.4 scipy=1.14.0 gcc=12.4.0 sphinx=7.3.7 myst-parser=4.0.0 sphinx-copybutton=0.5.2 sphinx-rtd-theme=3.0.1 pytest==8.3.3 -y

# Activate environment
SHELL ["conda", "run", "-n", "fenicsx-env", "/bin/bash", "-c"]

WORKDIR /root

# Set the default environment on container start
# ENTRYPOINT ["conda", "run", "-n", "fenicsx-env", "/bin/bash", "-c"]
CMD ["bash"]
