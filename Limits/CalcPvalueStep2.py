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

channels=["RS1WW","RS1ZZ","WZ","qW","qZ","BulkWW","BulkZZ"]

channels=["WZ","ZprimeWW","BulkWW","BulkZZ","qW","qZ"]
#channels=["qW","qZ"]
#channels=["qW","BulkZZ","WZ","BulkWW","ZprimeWW"]
for chan in channels:
    print "chan =",chan

    if "q" in chan:
       masses =[m*100 for m in range(12,60+1)]
       #masses =[1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,2700,2800,2900,3000,3100,3200,3300,3400,3500,3600,3700, 3800,3900,4000,4100,4200,4300,4400,4500,4600,4700,4800,4900,5000,5100,5200,5300,5400,5600,5700,5800,5900,6000]
       bins=["CMS_jj_qVHP","CMS_jj_qVLP","CMS_jj_qV"]
       bins=["CMS_jj_qVnew"]
       #bins=["CMS_jj_qWLP","CMS_jj_qWHP", "CMS_jj_qZHP","CMS_jj_qZLP"]
       
    else:
       masses =[m*100 for m in range(12,40+1)]
       bins=["CMS_jj_WWHP","CMS_jj_WZHP","CMS_jj_ZZHP","CMS_jj_WWLP","CMS_jj_WZLP","CMS_jj_ZZLP","CMS_jj_VVnew","CMS_jj_VVHPnew","CMS_jj_VVLPnew","CMS_jj_VV"]
       bins=["CMS_jj_VVnew"]
       #bins=["CMS_jj_WWLP", "CMS_jj_WWHP","CMS_jj_WZLP", "CMS_jj_WZHP","CMS_jj_ZZLP", "CMS_jj_ZZHP"]
    for bin in bins:
        sig=[]
        pval=[]
        for mass in masses:
            print "mass =",mass 

            f_fit=file("Limits/pValues/CMS_jj_"+chan+"_"+str(mass)+"_13TeV_"+bin+"_pvalue.out")
            print "we look inside the fit output for bin "+str(bin)
	    s=0
	    p=1.0
            for line in f_fit.readlines():
                if "Significance:" in line:
                    print float(line.split(":")[1].strip(" ").split(" ")[0])
                    s=float(line.split(":")[1].strip(" ").split(" ")[0])
                if "(p-value " in line:
                    print float(line.split("=")[1].split(")")[0])
                    p=float(line.split("=")[1].split(")")[0])
                if "Null p-value" in line:
                    print float(line.split(":")[1].strip().split(" ")[0])
                    p=float(line.split(":")[1].strip().split(" ")[0])
            f_fit.close()
	    sig+=[s]
	    pval+=[p]


        print "sig",[(masses[i],sig[i]) for i in range(len(masses))]

        sSig=[(masses[i],sig[i]) for i in range(len(masses))]

        f = open("Limits/CMS_jj_"+chan+"_13TeV_"+bin+"_significance.txt", "w")
        f.write(str(sSig))
        f.close()

        print "pval",[(masses[i],pval[i]) for i in range(len(masses))]

        sPval=[(masses[i],pval[i]) for i in range(len(masses))]

        f = open("Limits/CMS_jj_"+chan+"_13TeV_"+bin+"_pvalue.txt", "w")
        f.write(str(sPval))
        f.close()
