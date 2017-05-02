from ROOT import *
import ROOT
import array, math
import os

gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.2,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.03)
gStyle.SetPadRightMargin(0.05)
gStyle.SetMarkerSize(1.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)

channels=["qW","qZ"]#,"BulkWW","BulkZZ"]
channels=["altqW"]#,"BulkZZ","WZ","ZprimeWW"]
fullToys=False

freezeCMD="--freezeNuisances CMS_bkg_fit_slope1_CMS_jj_ZZHP_13TeV"
# freezeCMD=""
for chan in channels:
    print "chan =",chan

    if "q" in chan:
       masses =[m*100 for m in range(46,60+1)]
       #bins=["CMS_jj_qVHP","CMS_jj_qVLP","CMS_jj_qV"]
       bins=["CMS_jj_qWHP","CMS_jj_qWLP","CMS_jj_qW","CMS_jj_qZHP","CMS_jj_qZLP","CMS_jj_qZ","CMS_jj_qVHPnew","CMS_jj_qVLPnew"]
       bins=["CMS_jj_qWHP"]
    else:
       masses =[m*100 for m in range(12,45+1)]
       # masses=[4000]
       # bins=["CMS_jj_VVnew"]
       bins = ["CMS_jj_WWHP","CMS_jj_WZHP","CMS_jj_ZZHP","CMS_jj_WWLP","CMS_jj_WZLP","CMS_jj_ZZLP","CMS_jj_VVHPnew","CMS_jj_VVLPnew"]
       #bins = ["CMS_jj_WWHP","CMS_jj_WZHP","CMS_jj_ZZHP","CMS_jj_WWLP","CMS_jj_WZLP","CMS_jj_ZZLP","CMS_jj_VVHPnew","CMS_jj_VVLPnew","CMS_jj_VVnew",]
       #bins = ["CMS_jj_VVHPnew","CMS_jj_VVLPnew","CMS_jj_VVnew"]
       bins = ["CMS_jj_VVnew"]

    if fullToys:
      points=[]
      for p in range(1,10):
    	points+=[float(p/10.)]
    	points+=[float(p/10.+0.05)]
    	points+=[float(p/1.)]
    	points+=[float(p/1.+0.5)]
    	points+=[float(p*10.)]
    	points+=[float(p*10.+5.)]
    else:
      points=[0.1]
    points=[0.1] 
    #masses =[4300,4400,4500]
    for bin in bins:

        for mass in masses:
          print "mass =",mass

          for point in points:

            outputname = "CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_limit"+str(int(point*10))+"_submit.src"
            logname = "CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_limit"+str(int(point*10))+"_submit.out"
            outputfile = open(outputname,'w')
            outputfile.write('#!/bin/bash\n')
            outputfile.write("cd ${CMSSW_BASE}/src/DijetCombineLimitCode; eval `scramv1 run -sh`\n")
            if fullToys:
              outputfile.write("combine datacards/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+".txt -M HybridNew --frequentist --clsAcc 0 -T 100 -i 30 --singlePoint "+str(point)+" -s 10000"+str(int(point*100))+" --saveHybridResult --saveToys -m "+str(mass) + " -n "+chan+str(bin)+" &>CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_toy"+str(int(point*10))+"_fullCLs.out\n")
              outputfile.write("hadd -f grid_mX"+str(mass)+"_" + chan + "_13TeV_"+bin+".root higgsCombine" + chan + str(bin)+".HybridNew.mH"+str(int(mass))+".10000*.root\n")
              outputfile.write("combine datacards/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+".txt -M HybridNew --frequentist --grid grid_mX"+str(mass)+"_" + chan + "_13TeV_"+bin+".root -m "+str(mass) + " -n "+chan+str(bin)+" &>CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_obs_fullCLs.out\n")
              outputfile.write("combine datacards/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+".txt -M HybridNew --frequentist --grid grid_mX"+str(mass)+"_" + chan + "_13TeV_"+bin+".root -m "+str(mass) + " -n "+chan+str(bin)+" --expectedFromGrid 0.5 &>CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_50_fullCLs.out\n")
              outputfile.write("combine datacards/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+".txt -M HybridNew --frequentist --grid grid_mX"+str(mass)+"_" + chan + "_13TeV_"+bin+".root -m "+str(mass) + " -n "+chan+str(bin)+" --expectedFromGrid 0.16 &>CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_16_fullCLs.out\n")
              outputfile.write("combine datacards/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+".txt -M HybridNew --frequentist --grid grid_mX"+str(mass)+"_" + chan + "_13TeV_"+bin+".root -m "+str(mass) + " -n "+chan+str(bin)+" --expectedFromGrid 0.84 &>CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_84_fullCLs.out\n")
              outputfile.write("combine datacards/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+".txt -M HybridNew --frequentist --grid grid_mX"+str(mass)+"_" + chan + "_13TeV_"+bin+".root -m "+str(mass) + " -n "+chan+str(bin)+" --expectedFromGrid 0.025 &>CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_025_fullCLs.out\n")
              outputfile.write("combine datacards/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+".txt -M HybridNew --frequentist --grid grid_mX"+str(mass)+"_" + chan + "_13TeV_"+bin+".root -m "+str(mass) + " -n "+chan+str(bin)+" --expectedFromGrid 0.975 &>CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_975_fullCLs.out\n")
            else:
                outputfile.write("combine datacards/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+".txt -M Asymptotic -v2 -m "+str(mass) + " -n "+chan+str(bin)+" --rMax 100 --rMin 0.000001 &>CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_asymptoticCLs.out\n")
                outputfile.write("mv higgsCombine"+chan+str(bin)+".Asymptotic.mH"+str(int(mass))+".root Limits/withoutPDFandScale/CMS_jj_"+str(mass)+"_"+chan+"_13TeV_"+bin+"_asymptoticCLs_new.root")
            outputfile.close()
  
            command="rm "+logname
            print command
            os.system(command)
            if fullToys:
              command="""bsub -q 8nh -o """+logname+" source "+outputname
              # command="""qsub -q all.q """+outputname+" source "+outputname
               # submitJobsOnT3batch.sh
            else:
              command="chmod 755 ./"+outputname+";./"+outputname
            print command
            os.system(command)
            os.system("chmod 755 ./"+outputname+";./"+outputname)
