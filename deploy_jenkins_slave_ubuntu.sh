#!/usr/bin/env bash
set -x
apt-get update
# prepare for docker installation
apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
# install docker
apt-get install -y docker-ce docker-ce-cli containerd.io
# set up proxy settings for docker
mkdir /etc/systemd/system/docker.service.d
echo "[Service]" > /etc/systemd/system/docker.service.d/http-proxy.conf
echo "Environment=\"HTTP_PROXY=$http_proxy\"" >> /etc/systemd/system/docker.service.d/http-proxy.conf
echo "Environment=\"HTTPS_PROXY=$https_proxy\"" >> /etc/systemd/system/docker.service.d/http-proxy.conf
echo "Environment=\"NO_PROXY=localhost,127.0.0.1\"" >> /etc/systemd/system/docker.service.d/http-proxy.conf
systemctl daemon-reload
systemctl restart docker
# creating user for kenkins slave
useradd -m -s /bin/bash jenkins
usermod -aG docker jenkins
apt-get install -y openjdk-8-jdk
# DO  NOT FORGET TO SET THE PASSWORD FOR USER "jenkins" 
