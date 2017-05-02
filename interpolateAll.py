import os,sys
import time

masses =[m*100 for m in range(10,45+1)]
#samples = ["ZprimeWW_13TeV_"]#
#samples = ["ZprimeWW_13TeV_","WprimeWZ_13TeV_","BulkZZ_13TeV_","BulkWW_13TeV_"]
samples = ["QstarQW_13TeV_","QstarQZ_13TeV_"]
for sample in samples:
  if sample.find("Qstar") != -1:
    masses =[m*100 for m in range(10,60+1)]
  for mass in masses:
    #if sample.find("qZ") != -1 and mass == 2000: continue
    #if sample.find("BulkZZ") != -1 and mass > 4000: break
    command = 'qsub -q all.q interpolateAll.sh input/%s %i ' %(sample, mass)
    print command
    os.system(command)
  time.sleep(10)  







  
