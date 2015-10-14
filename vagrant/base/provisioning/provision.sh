#!/bin/bash

# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
# ------------------------------------------------------------------------------
# Display distribution release version
#-------------------------------------------------------------------------------

# Install NSTAT necessary tools
#-------------------------------------------------------------------------------


apt-get update && apt-get install -y \
    git \
    unzip \
    wget \
    net-tools

# build tools
#-------------------------------------------------------------------------------
apt-get install -y \
    snmp \
    snmpd \
    libpcap-dev \
    autoconf \
    make \
    automake \
    libtool \
    libconfig-dev

# ssh service & java installation
#-------------------------------------------------------------------------------
apt-get install -y \
    openssh-client \
    openssh-server \
    openjdk-7-jdk

# Python installation
#-------------------------------------------------------------------------------
apt-get install -y \
    build-essential \
    python-dev \
    python-setuptools \
    python3.4-dev \
    python3-setuptools \
    python \
    python3.4 \
    python-pip \
    python3-pip

# Install Python libraries
#-------------------------------------------------------------------------------
apt-get install -y \
    python3-bottle \
    python3-requests \
    python3-matplotlib \
    python3-lxml \
    python-lxml \
    python-bottle

# Install NSTAT necessary python3.4 tools
#-------------------------------------------------------------------------------
easy_install3 pip
pip3 install paramiko

# Install Mininet
#-------------------------------------------------------------------------------
git clone https://github.com/mininet/mininet.git
cd mininet
git checkout -b 2.2.1 2.2.1
./util/install.sh -vnf3

# Giving write access to ./opt (default directory where controller build
# handler downloads OpenDaylight from official repository)
#-------------------------------------------------------------------------------
cd /
sudo chmod 777 -R /opt
