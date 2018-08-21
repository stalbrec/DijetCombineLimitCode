# First insall combine according to this
# https://cms-hcomb.gitbooks.io/combine/content/part1/#for-end-users-that-dont-need-to-commit-or-do-any-development

import os,sys
sys.path.append('/afs/desy.de/user/a/albrechs/aQGCVVjj/python')
import PointName as PN 
#TODO: edit PointName, so it takes the OpName as Argument! Then impelent it in here

channels=['VV']
parameters=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]
# parameters=['T0']
steps=[1,2,3]

for channel in channels:
    for parameter in parameters:
        signal=channel+'_'+parameter
        #Changes to next line must be done also in Limits/brazilianFlag_aQTGC.py:~742
        couplings=PN.OpList(parameter,10)
        for coupling in couplings:
            #produce minitrees
            name=signal+"_"+coupling 
            if 1 in steps:
                os.system('root -b -q "MiniTreeProducerDataUHH_cut.C(\\"\\",\\"\\",\\"'+str(name)+'\\")"')
                os.system('root -b -q "MiniTreeSignalProducerUHH_cuts.C(10,11,0,\\"'+str(name)+'\\")"')
            #create datacards
            if 2 in steps:
                os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(name)+'\\",0,10,0,\\\"\\\")"') # VV-notVBF
                os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(name)+'\\",0,10,1,\\\"\\\")"') # VBF
                os.system('python Limits/CombineDatacardsUHH_cuts.py 0 '+str(name))
            #run combine
            if 3 in steps:
                os.system('python Limits/CalcAsympLimitsUHH_cuts.py 0 '+str(name))
        if 4 in steps:
            os.system('python Limits/brazilianFlag_aQTGC.py '+str(signal))
            
# steps=[1,2,3]
# steps=[4]

# channels=["WPZ_T0",
#         ]
# couplings=["1p08"]#,
#           #  "2p04",
# 	  #  "3p00",
#           # ]


# if 1 in steps:
#     # produce minitrees
#     for signal in signals:
#       for coupling in couplings:
#         name=signal+"_"+coupling
#         os.system('root -b -q "MiniTreeProducerDataUHH_cut.C(\\"\\",\\"\\",\\"'+str(name)+'\\")"')
#         os.system('root -b -q "MiniTreeSignalProducerUHH_cuts.C(10,11,0,\\"'+str(name)+'\\")"')
        
# if 2 in steps:
#     # create datacards
#     for signal in signals:
#       for coupling in couplings:
#         name=signal+"_"+coupling
#         os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(name)+'\\",0,10,0,\\\"\\\")"') # VV-notVBF
#         os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(name)+'\\",0,10,1,\\\"\\\")"') # VBF
#         os.system('python Limits/CombineDatacardsUHH_cuts.py 0 '+str(name))

# if 3 in steps:
#     for signal in signals:
#       for coupling in couplings:
#         name=signal+"_"+coupling
#         os.system('python Limits/CalcAsympLimitsUHH_cuts.py 0 '+str(name))

# if 4 in steps:
#     for signal in signals:
#       os.system('python Limits/brazilianFlag_aQTGC.py '+str(signal))
