#!/bin/bash

# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

pwd
echo "Workspace:" $WORKSPACE
echo "Job name:" $JOB_NAME

# storing the parent directory
# ------------------------------------------------------------------------------
if [ -d "/home/jenkins/nstat" ]; then
    rm -rf /home/jenkins/nstat
fi
mv $WORKSPACE /home/jenkins/nstat
export WORKSPACE='/home/jenkins/nstat'

PARENT_DIRECTORY=$(dirname $WORKSPACE)
export PYTHONPATH=$WORKSPACE
export MAVEN_OPTS="-Xmx1048m -XX:MaxPermSize=512m"
export no_proxy='localhost,127.0.0.1,192.168.100.20,192.168.100.21,192.168.100.22,192.168.100.23,192.168.100.24,192.168.100.25,192.168.100.26,192.168.100.27,192.168.100.28,192.168.100.29,192.168.100.30,192.168.100.31,192.168.100.32,192.168.100.33,192.168.100.34,192.168.100.35,192.168.100.1,172.28.40.10'
echo "Starting new test with Build Number= "$BUILD_NUMBER
export RESULTS_DIR=$JOB_NAME"_"$BUILD_NUMBER
export OUTPUT_FILENAME=$CONFIG_FILENAME
export COMMIT_MESSAGE="adding result file:"$OUTPUT_FILENAME" JOB: "$JOB_NAME_$BUILD_NUMBER