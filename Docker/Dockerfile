#The oficial image from Anaconda
FROM conda/miniconda3

# set up proxies for using conda
ENV http_proxy ${http_proxy}
ENV https_proxy ${https_proxy}
RUN echo "http_proxy=$http_proxy" > /etc/environment && \
    echo "https_proxy=$https_proxy" > /etc/environment

RUN conda config --set proxy_servers.http "$http_proxy" && \
    conda config --set proxy_servers.https "$https_proxy"

# The default version of conda is broken
RUN conda update -n base -c defaults conda
# Install mantid
RUN conda install --yes \
    -c conda-forge \
    -c mantid/label/nightly \
    -c mantid \
    mantid-framework=4 \
    pytest

# needed for mantid for some reason
RUN apt-get update
RUN apt-get install -y libgl1 libglu1-mesa && \
    apt-get clean

# updating scipp and run tests
CMD conda install --yes \
    -c scipp/label/dev scipp && \
    pytest /opt/tests
