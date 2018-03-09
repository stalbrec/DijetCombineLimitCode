# First insall combine according to this
# https://cms-hcomb.gitbooks.io/combine/content/part1/#for-end-users-that-dont-need-to-commit-or-do-any-development

import os

#steps=[1,2]#,3]#,4,5]
steps=[1,2,3,4,5]
masses=[1200,2000,4000]
cuts=["VV","VBF","invM500","invM1000","invM1500","invM2000","invM2500","invM3000","invM3500","invM4000"]
#cuts=["tau21","tau21_deta4","tau21_deta5","tau21_deta6","tau21_04","tau21_04_deta4","tau21_04_deta5","tau21_04_deta6","tau21_05","tau21_05_deta4","tau21_05_deta5","tau21_05_deta6","tau21_06","tau21_06_deta4","tau21_06_deta5","tau21_06_deta6","tau21_07","tau21_07_deta4","tau21_07_deta5","tau21_07_deta6"]
#cuts=["check"]
#cuts=["newStrategy"]
#cuts=["tau21_deta4"]
#cuts=["checkVBFnewStr"]

if 1 in steps:
    for mass in masses:
       # interpolate between signal MCs
        for cut in cuts:
            os.system('python interpolateUHH_selectedMasses_cut.py input/graviton '+str(mass)+' '+str(cut)+'_Interpolated' )
            os.system('python interpolateUHH_selectedMasses_cut.py input/radion '+str(mass)+' '+str(cut)+'_Interpolated' )
            
if 2 in steps:
    # produce minitrees
    for cut in cuts:
        #    print cut
        os.system('root -b -q "MiniTreeProducerDataUHH_cut.C(\\"radion\\",\\"_'+str(cut)+'\\",\\"_2000\\",)"')
        for mass in masses:
            os.system('root -b -q "MiniTreeSignalProducerUHH_cuts.C(0,2,'+str(mass)+',\\"'+str(cut)+'\\")"')
        
if 3 in steps:
#if 1 in steps:
    for mass in masses:
        for cut in cuts:
            # create datacards
            os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(cut)+'\\",'+str(mass)+',0,0,\\\"\\\")"') # graviton inclusive
            os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(cut)+'\\",'+str(mass)+',1,0,\\\"\\\")"') # radion inclusive
            os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(cut)+'\\",'+str(mass)+',0,1,\\\"\\\")"') # graviton VBF-only
            os.system('root -b -q "UHHFitter_cuts_newStrategy.cc(\\"'+str(cut)+'\\",'+str(mass)+',1,1,\\\"\\\")"') # radion VBF-only
            os.system('python Limits/CombineDatacardsUHH_cuts.py '+str(mass)+' '+str(cut))

if 4 in steps:
#if 1 in steps:
    for mass in masses:
        for cut in cuts:
            os.system('python Limits/CalcAsympLimitsUHH_cuts.py '+str(mass)+' '+str(cut))

if 5 in steps:
#if 2 in steps:
    for cut in cuts:
        os.system('python Limits/brazilianFlag_theoryUncBand_selectedMasses_cuts.py '+str(cut))
