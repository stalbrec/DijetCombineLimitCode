# First insall combine according to this
# https://cms-hcomb.gitbooks.io/combine/content/part1/#for-end-users-that-dont-need-to-commit-or-do-any-development

import os
   #hist = f.Get("MjjHists_invMAk4sel_1p0/M_jj_AK8_S2_5p0")                || to small weights: Use this ZZ_M0_4p50.root
   #hist = f.Get("MjjHists_invMAk4sel_1p0/M_jj_AK8_M1_0p70"),"ZZ_M1","ZZ_T1"
   #hist = f.Get("MjjHists_invMAk4sel_1p0/M_jj_AK8_T1_0p5"),"0p70","0p50"   || how to adjust for every point? columns?
steps=[1,2,3] 
signals=["ZZ_M0"
#"ZZ_M1" || "ZZ_M2"
#"ZZ_M3" |same couplings!| "ZZ_M4"
        ]
couplings=["4p50" #"0p0", "0p90", "1p80", "2p70", "3p60", 
#"0p00", "0p70", "1p40", "2p10", "2p80", "3p50" || "0p00", "1p50", "3p00", "4p50", "6p00", "7p50"
# "0p00", "10p00", "2p00", "4p00", "6p00", "8p00" |same| 
          ]
variables=["_mjj", "_pT"]
if 1 in steps:
    # produce minitrees
    for signal in signals:
      for coupling in couplings:
        for variable in variables:
          name=signal+"_"+coupling+variable
          os.system('root -b -q "MiniTreeProducerDataUHH_cut.C(\\"\\",\\"\\",\\"'+str(name)+'\\")"')
          os.system('root -b -q "MiniTreeSignalProducerUHH_cuts.C(10,11,0,\\"'+str(name)+'\\")"')
        
if 2 in steps:
    # create datacards
    for signal in signals:
      for coupling in couplings:
        for variable in variables:
          name=signal+"_"+coupling+variable
          os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(name)+'\\",0,10,0,\\\"\\\")"') # VV-notVBF
          os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(name)+'\\",0,10,1,\\\"\\\")"') # VBF
          os.system('python Limits/CombineDatacardsUHH_cuts.py 0 '+str(name))

if 3 in steps:
    for signal in signals:
      for coupling in couplings:
        for variable in variables:
          name=signal+"_"+coupling+variable
          os.system('python Limits/CalcAsympLimitsUHH_cuts.py 0 '+str(name))

if 4 in steps:
    for signal in signals:
      os.system('python Limits/brazilianFlag_aQTGC.py '+str(signal))
