# Start with a base image that includes conda
FROM continuumio/miniconda3:24.9.2-0

# Set environment variables
ENV CONDA_DEFAULT_ENV=base
ENV PATH /opt/conda/envs/${CONDA_DEFAULT_ENV}/bin:$PATH
ENV HOME /root

# Create the environment and install packages
# FEniCSx backend + documentation and testing dependencies
# sqlite for coverage, it necessary
RUN conda install -n ${CONDA_DEFAULT_ENV} -c conda-forge fenics-dolfinx=0.8.0 mpich=4.2.1 pyvista=0.43.10 gcc=12.4.0 sphinx=7.3.7 myst-parser=4.0.0 sphinx-copybutton=0.5.2 sphinx-rtd-theme=3.0.1 pytest=8.3.3 pytest-cov=6.0.0 sqlite=3.41.2 -y

WORKDIR /root

ADD . /fxdgm
RUN pip install --editable /fxdgm/.

CMD ["bash"]
