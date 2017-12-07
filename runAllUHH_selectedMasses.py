# First insall combine according to this
# https://cms-hcomb.gitbooks.io/combine/content/part1/#for-end-users-that-dont-need-to-commit-or-do-any-development

import os

steps=[1,2,3,4,5]
masses=[1200,2000,4000]

if 1 in steps:
 for mass in masses:
  # interpolate between signal MCs
  os.system('python interpolateUHH_selectedMasses.py input/graviton '+str(mass))
  os.system('python interpolateUHH_selectedMasses.py input/radion '+str(mass))

if 2 in steps:
 # produce minitrees
 os.system('root -b -q MiniTreeProducerDataUHH.C')
 for mass in masses:
     os.system('root -b -q "MiniTreeSignalProducerUHH.C(0,2,'+str(mass)+')"')
#  os.system('root -b -q "MiniTreeSignalProducerUHH.C('+str(mass)+')"')

if 3 in steps:
 for mass in masses:
  # create datacards
  os.system('root -b -q "UHHFitter.cc('+str(mass)+',0,0,\\\"\\\")"') # graviton inclusive
  os.system('root -b -q "UHHFitter.cc('+str(mass)+',1,0,\\\"\\\")"') # radion inclusive
  os.system('root -b -q "UHHFitter.cc('+str(mass)+',0,1,\\\"\\\")"') # graviton VBF-only
  os.system('root -b -q "UHHFitter.cc('+str(mass)+',1,1,\\\"\\\")"') # radion VBF-only

if 4 in steps:
 for mass in masses:
  os.system('python Limits/CalcAsympLimitsUHH.py '+str(mass))

if 5 in steps:
# for mass in masses:
  os.system('python Limits/brazilianFlag_theoryUncBand_selectedMasses.py')
