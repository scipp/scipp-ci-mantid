# scipp-ci-mantid
Contains tools for setting up the continuous integration and testing of 
scipp against Mantid. It is supposed to use Jenkins for CI needs. Script 
for deployment the jenkins slave on ubuntu is provided: 
`deploy_jenkins_slave_ubuntu.sh`. Execute it on the machine with ubuntu 
installed. Do not forget to set the password for `jenkins` user or to
set up another type of access for Jenkins master to slave.

#### Shell commands to execute on the slave machine

To use ubuntu as Jenkins slave:

```
sudo apt-get update
sudo apt-get install -y curl apt-transport-https ca-certificates gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg |sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
su
deploy_jenkins_slave_ubuntu.sh
passwd jenkins
exit
```

To update the docker image from this repo:

```bash
. ~/.profile && cd /opt/ci/scipp-ci-mantid && python3 build_docker.py --rebuild --http_proxy --https_proxy
``` 

to run tests:

```bash
cd /opt/ci/scipp-ci-mantid && python3 run_comparison_tests.py
```

#### Adding tests

Add needed tests compatible with `pytest` to `tests` folder. 


