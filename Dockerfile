# Start with a base image that includes dolfinx
FROM dolfinx/dolfinx:v0.9.0

# Update OS
RUN apt-get update && apt-get install -y

# Update pip
RUN python -m pip install --upgrade pip

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

WORKDIR /root

ADD . /fxdgm
RUN pip install --no-cache-dir --editable /fxdgm/.

CMD ["bash"]
