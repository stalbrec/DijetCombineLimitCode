import os,sys
import time

masses =[m*100 for m in range(10,45+1)]
models = ["altqW"]
#channels = ["qVHPnew","qVLPnew"]
channels =["qVnew","qWHP","qWLP","qZHP","qZLP"]
#workspaceBKG = "CMS_jj_bkg_qV_13TeV"
workspaceBKG = "CMS_jj_bkg_qValt_13TeV"
for channel in channels:
    for model in models:
        if model.find("q") != -1:
            masses =[m*100 for m in range(12,60+1)]
            #masses = [4000]
        for mass in masses:
            #workspaceSignal = "CMS_jj_"+model+"_"+str(int(mass))+"_13TeV"
            workspaceSignal = "CMS_jj_qW_"+str(int(mass))+"_13TeV"
            command = 'qsub -q all.q submitLimits.sh CMS_jj_'+model+'_'+str(int(mass))+'_13TeV_CMS_jj_'+channel+' '+str(int(mass))+' CMS_jj_'+str(int(mass))+'_'+model+'_13TeV_CMS_jj_'+channel+'_asymptoticCLs_new.root '+workspaceBKG+' '+workspaceSignal
            print command
            os.system(command)
            #time.sleep(1) 
            
            
            
            
#masses =[m*100 for m in range(12,43+1)]
##models = ["ZprimeWW","BulkWW","BulkZZ","WZ"]
#models = ["BulkWW"]
##channels = ["WWHP","WWLP","ZZHP","ZZLP","WZHP","WZLP","VVnew"]
##channels = ["ZZHP","ZZLP","VVnew"]
##models =["BulkWW"]
##masses =[4000]
##channels = ["VVHPnew","VVLPnew","VVnew"]
##channels = ["VVnew"]
#channels = ["WWHP","WWLP","ZZHP","ZZLP","WZHP","WZLP"]
#workspaceBKG = " CMS_jj_bkg_VV_13TeV"
#for channel in channels:
    #for model in models:
        #if model.find("q") != -1:
            #masses =[m*100 for m in range(12,60+1)]
        #for mass in masses:
            #workspaceSignal = "CMS_jj_"+model+"_"+str(int(mass))+"_13TeV"
            #command = 'qsub -q all.q submitLimits.sh CMS_jj_'+model+'_'+str(int(mass))+'_13TeV_CMS_jj_'+channel+' '+str(int(mass))+' CMS_jj_'+str(int(mass))+'_'+model+'_13TeV_CMS_jj_'+channel+'_asymptoticCLs_new.root '+workspaceBKG+' '+workspaceSignal
            #print command
            #os.system(command)
            ##time.sleep(1)
            
            
#masses =[m*100 for m in range(12,43+1)]
#models = ["qW"]
##channels = ["qVnew"]
#channels =["qWHP","qWLP","qZHP","qZLP","qVnew"]
#workspaceBKG = "CMS_jj_bkg_qV_13TeV"
#for channel in channels:
    #for model in models:
        #if model.find("q") != -1:
            #masses =[m*100 for m in range(12,60+1)]
        #for mass in masses:
            #workspaceSignal = "CMS_jj_"+model+"_"+str(int(mass))+"_13TeV"
            #command = 'qsub -q all.q submitLimits.sh CMS_jj_'+model+'_'+str(int(mass))+'_13TeV_CMS_jj_'+channel+' '+str(int(mass))+' CMS_jj_'+str(int(mass))+'_'+model+'_13TeV_CMS_jj_'+channel+'_asymptoticCLs_new.root '+workspaceBKG+' '+workspaceSignal
            #print command
            #os.system(command)
            ##time.sleep(1)
            
            
            
## alternaive fit function !
#masses =[m*100 for m in range(12,43+1)]
##masses =[4100]
#models = ["altBulkWW"]
##channels = ["WWHP","WWLP","ZZHP","ZZLP","WZHP","WZLP"]
#channels = ["VVnew"]
#workspaceBKG = " CMS_jj_bkg_VValt_13TeV"
#for channel in channels:
    #for model in models:
        #if model.find("q") != -1:
            #masses =[m*100 for m in range(12,41+1)]
        #for mass in masses:
            #workspaceSignal = "CMS_jj_"+model+"_"+str(int(mass))+"_13TeV"
            #command = 'qsub -q all.q submitLimits.sh CMS_jj_'+model+'_'+str(int(mass))+'_13TeV_CMS_jj_'+channel+' '+str(int(mass))+' CMS_jj_'+str(int(mass))+'_'+model+'_13TeV_CMS_jj_'+channel+'_asymptoticCLs_new.root '+workspaceBKG+' '+workspaceSignal
            #print command
            #os.system(command)
            ##time.sleep(1)
