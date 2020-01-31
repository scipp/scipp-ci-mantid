#!/usr/bin/env bash
set -x
apt-get update
# install docker
apt-get install -y docker-ce docker-ce-cli containerd.io
# set up proxy settings for docker

if [[ ! -d "/etc/systemd/system/docker.service.d" ]]
then
    mkdir /etc/systemd/system/docker.service.d
fi
echo "[Service]" > /etc/systemd/system/docker.service.d/http-proxy.conf
echo "Environment=\"HTTP_PROXY=$http_proxy\"" >> /etc/systemd/system/docker.service.d/http-proxy.conf
echo "Environment=\"HTTPS_PROXY=$https_proxy\"" >> /etc/systemd/system/docker.service.d/http-proxy.conf
echo "Environment=\"NO_PROXY=localhost,127.0.0.1\"" >> /etc/systemd/system/docker.service.d/http-proxy.conf
systemctl daemon-reload
systemctl restart docker
# creating user for jenkins slave
if ! id -u jenkins > /dev/null 2>&1
then
    useradd -m -s /bin/bash jenkins
    usermod -aG docker jenkins
fi

git_http="git config --global http.proxy $http_proxy"
git_https="git config --global https.proxy $https_proxy"

echo "$git_http" >> /home/jenkins/.profile
echo "$git_https" >> /home/jenkins/.profile
bash -c "$git_http"
bash -c "$git_https"

apt-get install -y openjdk-8-jdk

if [[ ! -d "/opt/ci" ]]
then
    mkdir -p /opt/ci
fi

cd /opt/ci
git clone https://github.com/scipp/scipp-ci-mantid.git
chown -R jenkins:jenkins /opt/ci
chmod -R a+rw /opt/ci
echo "Don't forget to setup the password for user 'jenkins'."
# DO  NOT FORGET TO SET THE PASSWORD FOR USER "jenkins"
