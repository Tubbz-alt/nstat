#!/bin/bash

# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
# ------------------------------------------------------------------------------
# Display distribution release version
#-------------------------------------------------------------------------------

BASE_DIR=$(pwd)
cd $BASE_DIR

# Prevent headers and kernels updates. Mininet will not work with Linux kernel
# newer than 3.12.x
#-------------------------------------------------------------------------------
apt-mark hold linux-image-generic linux-headers-generic

# NSTAT node necessary tools
#-------------------------------------------------------------------------------
apt-get update && apt-get install --force-yes -y \
    git \
    unzip \
    wget \
    iperf \
    mz \
    wireshark \
    net-tools

# CONTROLLER_node necessary tools
#-------------------------------------------------------------------------------
apt-get install --force-yes -y \
    openssh-client \
    openssh-server \
    openjdk-7-jdk \
    openjdk-7-jre

# SOUTHBOUND_GEN_node necessary tools (build tools)
#-------------------------------------------------------------------------------
apt-get install --force-yes -y \
    build-essential \
    snmp \
    libsnmp-dev \
    snmpd \
    libpcap-dev \
    autoconf \
    make \
    automake \
    libtool \
    libconfig-dev \
    fakeroot \
    debhelper \
    libssl-dev \
    pkg-config \
    bzip2 \
    openssl \
    procps

# PYTHON installation
#-------------------------------------------------------------------------------
apt-get install --force-yes -y \
    python-dev \
    python-setuptools \
    python3.4-dev \
    python3-setuptools \
    python \
    python3.4 \
    python-pip \
    python3-pip

# PYTHON extra libraries
#-------------------------------------------------------------------------------
apt-get install --force-yes -y \
    python3-bottle \
    python3-requests \
    python3-matplotlib \
    python3-lxml \
    python-lxml \
    python-paramiko \
    python-pypcap \
    python-dpkt \
    python-bottle

# PYTHON3.4 NSTAT necessary libraries
#-------------------------------------------------------------------------------
easy_install3 pip
pip3 install paramiko
pip3 install collections-extended

# Giving write access to ./opt (default directory where controller build
# handler downloads OpenDaylight from official repository)
#-------------------------------------------------------------------------------
cd /
sudo chmod 777 -R /opt
cd $BASE_DIR

# MININET installation
#-------------------------------------------------------------------------------
sudo apt-get update && sudo apt-get install --force-yes -y uuid-runtime
git clone https://github.com/mininet/mininet.git /opt/mininet
cd /opt/mininet
git checkout -b 2.2.1 2.2.1
./util/install.sh -n3f

# OPENVSWITCH installation
#-------------------------------------------------------------------------------
./util/install.sh -V 2.3.0
service openvswitch-switch start
/bin/bash
cd $BASE_DIR

# NSTAT installation
#-------------------------------------------------------------------------------
git clone https://github.com/intracom-telecom-sdn/nstat.git /opt/nstat
cd /opt/nstat
git branch -a       # list NSTAT branches
git checkout master # checkout to master branch
git tag -l          # list NSTAT tags
cd $BASE_DIR