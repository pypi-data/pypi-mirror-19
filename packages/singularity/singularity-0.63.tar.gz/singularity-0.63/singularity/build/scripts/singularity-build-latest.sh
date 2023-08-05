#!/bin/sh
apt-get update > /tmp/.install-log
apt-get -y install git \
                   build-essential \
                   libtool \
                   autotools-dev \
                   automake \
                   autoconf \
                   python3-pip >> /tmp/.install-log

# so that adjusted PATH propagates into sudo
sed -i -e 's/^Defaults\tsecure_path.*$//' /etc/sudoers

# Install Singularity from Github
cd /tmp && git clone http://www.github.com/singularityware/singularity 
cd singularity && ./autogen.sh && ./configure --prefix=/usr/local && make && make install

# Pip3 installs
pip3 install --upgrade pip &&
pip3 install --upgrade google-api-python-client &&
pip3 install --upgrade google &&
pip3 install oauth2client==3.0.0 gitpython singularity

# Main running script
python3 -c "from singularity.build.google import run_build; run_build()" > /tmp/.shub-log 2>&1

# Finish by sending log
export command=$(echo "from singularity.build.google import finish_build; finish_build()") &&
python3 -c "$command"
