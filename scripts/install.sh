#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh

export SCRAM_ARCH=slc7_amd64_gcc700


cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src

eval `scramv1 runtime -sh`

git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.1.0

cd $CMSSW_BASE/src

echo 'installing combineHarvester'
git clone https://github.com/cms-analysis/CombineHarvester.git 

git clone https://github.com/stalbrec/DijetCombineLimitCode
cd DijetCombineLimitCode
git fetch origin
git checkout aQGC_2020

sed -i "s+REPLACEDIJETDIR+${CMSSW_BASE}/src/DijetCombineLimitCode+g" ${CMSSW_BASE}/src/DijetCombineLimitCode/submitwrapper.sh

cd $CMSSW_BASE/src

scram b clean; scram b -j8

cd DijetCombineLimitCode

echo "creating some mandatory directories"
mkdir -p MiniTrees/DataUHH
mkdir -p MiniTrees/SignalUHH
mkdir -p workspaces


