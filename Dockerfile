FROM continuumio/miniconda3:25.1.1-2

# Set environment variables
ENV CONDA_DEFAULT_ENV=base
ENV PATH /opt/conda/envs/${CONDA_DEFAULT_ENV}/bin:$PATH
ENV HOME /root

# Install fenicsx backend + documentation and testing dependencies
RUN conda install -n ${CONDA_DEFAULT_ENV} -c conda-forge --yes \
    fenics-dolfinx=0.9.0 \
    mpich=4.3.0 \
    pyvista=0.43.10 \
    c-compiler=1.9.0 \
    cxx-compiler=1.9.0 \
    fortran-compiler=1.9.0 \
    sqlite=3.44.0 \
    && pip install --no-cache-dir \
        sphinx==7.3.7 \
        myst-parser==4.0.0 \
        sphinx-copybutton==0.5.2 \
        sphinx-rtd-theme==3.0.1 \
        pytest==8.3.3 \
        pytest-cov==6.0.0
    # && conda clean -afy \
    # && conda clean --all --yes \
    # && pip cache purge \
    # && rm -rf /opt/conda/pkgs/* \
    # && rm -rf /tmp/* \
    # && rm -rf /root/.cache \
    # && apt-get autoremove -y \
    # && apt-get clean \
    # && rm -rf /var/lib/apt/lists/*

# Set working directory and copy application
WORKDIR /fxdgm
COPY . .

# Install fxdgm package and final cleanup
RUN pip install --no-cache-dir . \
    && pip cache purge \
    && rm -rf /root/.cache

CMD ["bash"]
