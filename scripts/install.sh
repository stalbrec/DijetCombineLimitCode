#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh

cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src

eval `scramv1 runtime -sh`

git clone https://github.com/stalbrec/DijetCombineLimitCode
cd DijetCombineLimitCode
git fetch origin
git checkout aQGC_2020

DIJETDIR=$(pwd)
sed -i "s+REPLACEDIJETDIR+${DIJETDIR}+g" submitwrapper.sh

scram b clean; scram b -j8
