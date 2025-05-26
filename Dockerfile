# Start with a base image that includes conda
FROM continuumio/miniconda3:25.1.1-2

# Set environment variables
ENV CONDA_DEFAULT_ENV=base
ENV PATH /opt/conda/envs/${CONDA_DEFAULT_ENV}/bin:$PATH
ENV HOME /root

# Create the environment and install packages
# FEniCSx backend (+ sqlite for database support for coverage report)
RUN conda install -n ${CONDA_DEFAULT_ENV} -c conda-forge --yes \
    fenics-dolfinx=0.9.0 \
    mpich=4.3.0 \
    pyvista=0.43.10 \
    gcc=13.3.0 \
    sqlite=3.44.0 \ 
    && conda clean -afy

# Documentation tools
RUN pip install --no-cache-dir \
    sphinx==7.3.7 \
    myst-parser==4.0.0 \
    sphinx-copybutton==0.5.2 \
    sphinx-rtd-theme==3.0.1

# Testing tools
RUN pip install --no-cache-dir \
    pytest==8.3.3 \
    pytest-cov==6.0.0
# RUN conda install -n ${CONDA_DEFAULT_ENV} -c conda-forge sqlite=3.44 -y

WORKDIR /root

ADD . /fxdgm
RUN pip install --no-cache-dir --editable /fxdgm/.

CMD ["bash"]
