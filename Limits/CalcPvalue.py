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

channels=["WZ","qW","qZ","BulkWW"]
channels=["BulkZZ","WZ","BulkZZ","ZprimeWW","qW","qZ"]
channels=["qZ","qW"]
fullToys=False

for chan in channels:
    print "chan =",chan

    if "q" in chan:
       masses =[m*100 for m in range(12,60+1)]
       masses =[5500]
       bins=["CMS_jj_qVHP","CMS_jj_qVLP","CMS_jj_qV"]
       bins=["CMS_jj_qVnew"]
       bins=["CMS_jj_qVHPnew", "CMS_jj_qVLPnew"]
       bins=["CMS_jj_qWLP","CMS_jj_qWHP", "CMS_jj_qZHP","CMS_jj_qZLP"]
       bins=["CMS_jj_qVnew"]
    else:
       masses =[m*100 for m in range(12,41+1)]
       bins=["CMS_jj_VVnew"]
       bins=["CMS_jj_VVHPnew", "CMS_jj_VVLPnew"]
       bins=["CMS_jj_WWLP", "CMS_jj_WWHP","CMS_jj_WZLP", "CMS_jj_WZHP","CMS_jj_ZZLP", "CMS_jj_ZZP"]
       bins=["CMS_jj_VVnew"]
    for bin in bins:
        sig=[]
        pval=[]
        for mass in masses:
            print "mass =",mass
            outputname = "CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_pvalue_submit.src"
            outfile="Limits/pValues/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_pvalue.out"
            outputfile = open(outputname,'w')
            outputfile.write('#!/bin/bash\n')
            outputfile.write("cd ${CMSSW_BASE}/src/DijetCombineLimitCode; eval `scramv1 run -sh`\n")
            if "CMS_jj_qV" in bin:
              freeze=" --freezeNuisances CMS_bkg_fit_slope3_CMS_jj_qVHP,CMS_bkg_fit_slope3_CMS_jj_qVLP"
            if "CMS_jj_ZZHP" in bin:
                freeze=" --freezeNuisances CMS_bkg_fit_slope1_CMS_jj_ZZHP_13TeV"
            if fullToys:
              outputfile.write("combine datacards_withPDFuncertainties/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+".txt -M HybridNew "+freeze+" --frequentist --fullBToys -T 3000 --fork 0 -m "+str(mass) + " -n "+chan+str(bin)+" --signif \n")
            else:
                outputfile.write("combine datacards/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+".txt -M ProfileLikelihood -v2 -m "+str(mass) + " -n "+chan+str(bin)+" --signif \n")
                outputfile.write("mv higgsCombine"+chan+str(bin)+".ProfileLikelihood.mH"+str(int(mass))+".root Limits/pValues/CMS_jj_"+str(mass)+"_"+chan+"_13TeV_"+bin+"_pvalue_new.root")
            outputfile.close()
  
            command="rm "+outfile
            print command
            os.system(command)
            if fullToys:
              command="bsub -q 8nh -o "+outfile+" source "+outputname
            else:
              command="bsub -q 1nh -o "+outfile+" source "+outputname
            command="chmod 755 ./"+outputname+";./"+outputname +">"+outfile
            print command
            os.system(command)

  	        
