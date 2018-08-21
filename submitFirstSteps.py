#!/usr/bin/env python
import os,glob,sys
sys.path.append('/afs/desy.de/user/a/albrechs/aQGCVVjj/python')
import PointName as PN 
from backup import backup

if (__name__=='__main__'):
    # channels=['VV']
    # parameters=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]

    # for channel in channels:
    #     for parameter in parameters:
    #         signal=channel+'_'+parameter
    steps=[1,2,3]
    # steps=[4]
    # steps=[1,2,3,4]
    signal=sys.argv[1]
    parameter=signal[-2:]
    coupling=sys.argv[2]
    #Changes to next line must be done also in Limits/brazilianFlag_aQTGC.py:~742
    # couplings=PN.OpList(parameter)
    # for coupling in couplings:
    #produce minitrees
    name=signal+"_"+coupling 
    if 1 in steps:
        os.system('root -b -q "MiniTreeProducerDataUHH_cut.C(\\"\\",\\"\\",\\"'+str(name)+'\\")"')
        os.system('root -b -q "MiniTreeSignalProducerUHH_cuts.C(10,11,0,\\"'+str(name)+'\\")"')
    #Fit and create datacards
    if 2 in steps:
        os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(name)+'\\",0,10,0,\\\"\\\")"') # VV-notVBF
        os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(name)+'\\",0,10,1,\\\"\\\")"') # VBF
        os.system('python Limits/CombineDatacardsUHH_cuts.py 0 '+str(name))
    #run combine
    if 3 in steps:
        os.system('python Limits/CalcAsympLimitsUHH_cuts.py 0 '+str(name))
    # if 4 in steps:
    #     os.system('python Limits/brazilianFlag_aQTGC.py '+str(signal))
