import os,sys,time

masses =[m*100 for m in range(11,43+1)]#45+1)]
# masses =[m*100 for m in range(12,62+1)]
samples = [4]  # 0==RS1WW/ZZ 2==W'/Z' 4==BulkG WW/ZZ 6==qW/qZ
altfunc = '\"alt\"'
for sample in samples:
  for mass in masses:
    channel = 1    # 1==VV 2==qV 3==No purity
    if sample != 0 and sample != 2 and sample != 4: 
      channel = 2
    sample1 = "BulkWW"
    sample2 = "BulkZZ"
    if sample == 2:
      sample1 = "WprimeWZ"
      sample2 = "ZprimeWW"  
    if sample == 6:
      sample1 = "qW"
      sample2 = "qZ"  
    command = 'qsub -q short.q submitWorkspaces.sh %i %i %i %s %s %s'%(mass,sample,channel,altfunc, sample1, sample2)
    print command
    os.system(command)


  
