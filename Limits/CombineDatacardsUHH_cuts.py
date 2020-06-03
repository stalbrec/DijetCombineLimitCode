from __future__ import print_function
from ROOT import *
import ROOT
import array, math
import os,sys

mass=sys.argv[1]
cut=sys.argv[2]
if float(mass)>0:
  signals=["graviton_","radion_"]
else:
  signals=[""]
directory="datacards/"

for signal in signals:
  card=directory+"CMS_jj_"+signal+cut+"_"+mass+"_13TeV__invMass"
  command="combineCards.py " +card+".txt " +card+"_afterVBFsel.txt > " +card+"_combined.txt"
  print(command)
  os.system( command  )
  #create combined workspace solely for CombineHarvester
  text2workspace_command = "text2workspace.py "+card+"_combined.txt; mv "+card+'_combined.root workspaces/'
  print(command)
  os.system(command)
