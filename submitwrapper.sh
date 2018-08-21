#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh

DIJETDIR=/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode

cd $DIJETDIR
eval `scram runtime -sh`

python submitSteps.py $1 $2 $3
