#The oficial image from Anaconda
FROM ubuntu

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install --yes wget locales

# Set locale to be sure CSS can work with all needed symbols
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /opt/miniconda.sh && \
    bash /opt/miniconda.sh -b -p /opt/miniconda && \
    rm /opt/miniconda.sh

ENV PATH=/opt/miniconda/bin:$PATH

# set up proxies for using conda
ENV http_proxy ${http_proxy}
ENV https_proxy ${https_proxy}
RUN echo "http_proxy=$http_proxy" > /etc/environment && \
    echo "https_proxy=$https_proxy" > /etc/environment

RUN conda config --set proxy_servers.http "$http_proxy" && \
    conda config --set proxy_servers.https "$https_proxy"

COPY scripts /opt/scripts
RUN chmod -R a+rwx /opt/scripts

RUN echo scipp_env > /opt/scipp_env

# Create the environment with mantid and python version
# valid for latest scipp
RUN conda remove --yes -n $(cat /opt/scipp_env) --all && \
    conda create --yes -n $(cat /opt/scipp_env) \
    -c conda-forge \
    -c mantid/label/nightly \
    -c scipp/label/dev \
    -c mantid \
    python=$(bash /opt/scripts/common_scipp_mantid_py_version.sh) \
    mantid-framework=$(/opt/scripts/mantid_framework_latest_version.sh) \
    scipp=$(/opt/scripts/scipp_latest_version.sh) \
    pytest \
    matplotlib ipywidgets   # should be resolved on dependencies of scipp


# needed for mantid for some reason
RUN apt-get update
RUN apt-get install -y libgl1 libglu1-mesa && \
    apt-get clean

# updating scipp and run tests
CMD source activate $(cat /opt/scipp_env) && \
    bash /opt/scripts/check_python_version.sh && \
    conda install --yes \
    -c scipp/label/dev \
    scipp=$(bash /opt/scripts/scipp_latest_version.sh) && \
    echo $(bash /opt/scripts/scipp_latest_version.sh) && \
    pytest /opt/tests


