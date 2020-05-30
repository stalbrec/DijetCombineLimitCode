#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh

export SCRAM_ARCH=slc6_amd64_gcc530


cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src

eval `scramv1 runtime -sh`

git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v7.0.13

cd $CMSSW_BASE/src

git clone https://github.com/stalbrec/DijetCombineLimitCode
cd DijetCombineLimitCode
git fetch origin
git checkout aQGC_2020

sed -i "s+REPLACEDIJETDIR+${CMSSW_BASE}/src/DijetCombineLimitCode+g" ${CMSSW_BASE}/src/DijetCombineLimitCode/submitwrapper.sh

scram b clean; scram b -j8
