#!/bin/bash

# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

# copy results back to test-server
# --------------------------------------------------------------------
cp -r $WORKSPACE/$JOB_NAME"_"$BUILD_NUMBER /home/jenkins/sample_tests/

# copy results under 'publisher' folder so that HTML publisher can
# archive the results
# -------------------------------------------------------------------
if [ -d "/tmp/publisher" ]; then
  cp -a $WORKSPACE/$JOB_NAME"_"$BUILD_NUMBER/*.* /tmp/publisher
else
  mkdir -p "/tmp/publisher"
  cp -a $WORKSPACE/$JOB_NAME"_"$BUILD_NUMBER/*.* /tmp/publisher
fi

# cleanup the machine
# --------------------------------------------------------------------
cd $(dirname $WORKSPACE)
rm -rf $JOB_NAME