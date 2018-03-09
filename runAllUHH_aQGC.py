# First insall combine according to this
# https://cms-hcomb.gitbooks.io/combine/content/part1/#for-end-users-that-dont-need-to-commit-or-do-any-development

import os

steps=[1,2,3]
signals=["WPZ_T0",
        ]
couplings=["1p08",
           "2p04",
	   "3p00",
          ]

if 1 in steps:
    # produce minitrees
    for signal in signals:
      for coupling in couplings:
        name=signal+"_"+coupling
        os.system('root -b -q "MiniTreeProducerDataUHH_cut.C(\\"\\",\\"\\",\\"'+str(name)+'\\")"')
        os.system('root -b -q "MiniTreeSignalProducerUHH_cuts.C(10,11,0,\\"'+str(name)+'\\")"')
        
if 2 in steps:
    # create datacards
    for signal in signals:
      for coupling in couplings:
        name=signal+"_"+coupling
        os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(name)+'\\",0,10,0,\\\"\\\")"') # VV-notVBF
        os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(name)+'\\",0,10,1,\\\"\\\")"') # VBF
        os.system('python Limits/CombineDatacardsUHH_cuts.py 0 '+str(name))

if 3 in steps:
    for signal in signals:
      for coupling in couplings:
        name=signal+"_"+coupling
        os.system('python Limits/CalcAsympLimitsUHH_cuts.py 0 '+str(name))

if 4 in steps:
    for signal in signals:
      os.system('python Limits/brazilianFlag_aQGC.py '+str(signal))
