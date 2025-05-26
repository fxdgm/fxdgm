# Start with a base image that includes conda
FROM continuumio/miniconda3:25.1.1-2

# Set environment variables
ENV CONDA_DEFAULT_ENV=base
ENV PATH /opt/conda/envs/${CONDA_DEFAULT_ENV}/bin:$PATH
ENV HOME /root

# Create the environment and install packages
# FEniCSx backend (+ sqlite for database support for coverage report) and docs/test tools
RUN conda install -n ${CONDA_DEFAULT_ENV} -c conda-forge --yes \
    fenics-dolfinx=0.9.0 \
    mpich=4.3.0 \
    pyvista=0.43.10 \
    gcc=13.3.0 \
    sqlite=3.44.0 \ 
    && conda clean -afy \
    && pip install --no-cache-dir \
    sphinx==7.3.7 \
    myst-parser==4.0.0 \
    sphinx-copybutton==0.5.2 \
    sphinx-rtd-theme==3.0.1 \
    && pip install --no-cache-dir \
    pytest==8.3.3 \
    pytest-cov==6.0.0

WORKDIR /root

# Add the source code to the container
ADD ./ ./

RUN pip install --no-cache-dir --editable .

CMD ["bash"]
