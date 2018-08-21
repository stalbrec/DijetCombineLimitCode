#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh

DIJETDIR=/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode

cd $DIJETDIR
eval `scram runtime -sh`

# python submitLastStep.py $1
python Limits/brazilianFlag_aQTGC.py $1
# #produce minitrees
# root -b -q "MiniTreeProducerDataUHH_cut.C(\"\",\"\",\"${1}\")"
# root -b -q "MiniTreeSignalProducerUHH_cuts.C(10,11,0,\"${1}\")"

# #create datacards
# root -b -q "UHHFitter_cuts_newStrategy.cc(\"${1}\",0,10,0,\"\")" # VV-notVBF 
# root -b -q "UHHFitter_cuts_newStrategy.cc(\"${1}\",0,10,1,\"\")" # VBF
# python Limits/CombineDatacardsUHH_cuts.py 0 $1

# #run combine
# python Limits/CalcAsympLimitsUHH_cuts.py 0 $1
