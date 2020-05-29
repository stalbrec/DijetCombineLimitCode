#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh

DIJETDIR=REPLACEDIJETDIR

cd $DIJETDIR
eval `scram runtime -sh`

python submitSteps.py $1 $2 $3
