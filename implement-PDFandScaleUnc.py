from array import array
import sys
import ROOT
from ROOT import *
import ROOT as rt

import os,commands, os.path
import fileinput

def uncertaintyFromFile(f):
  pFile=open(f)
  unc=rt.TGraph()
  startCrossSection=False
  for l in pFile.readlines():
    if startCrossSection and "00" in l:
      unc.Set(unc.GetN()+1)
      unc.SetPoint(unc.GetN(),float(l.split()[0]),float(l.split()[3])/100.)
    if "acceptance" in l: startCrossSection=True
  return unc

qStarqWunc=uncertaintyFromFile("updf_qStarqW.txt")
qStarqZunc=uncertaintyFromFile("updf_qStarqZ.txt")
BulkGWWunc=uncertaintyFromFile("updf_BulkGWW.txt")
BulkGZZunc=uncertaintyFromFile("updf_BulkGZZ.txt")
ZprimeWWunc=uncertaintyFromFile("updf_ZprimeWW.txt")
WprimeWZunc=uncertaintyFromFile("updf_WprimeWZ.txt")

def get_xsec_unc(mass):
   uncs = {}
   fin = rt.TFile.Open("/mnt/t3nfs01/data01/shome/thaarres/EXOVVAnalysisRunII/LimitCode/CMSSW_7_1_5/src/DijetCombineLimitCode/EXOVVSystematics/xsec-unc-13TeV.root",'READ')   
   cin = fin.Get('c')
   for p in cin.GetListOfPrimitives():
    if p.InheritsFrom("TMultiGraph"):
     for g in p.GetListOfGraphs(): uncs[g.GetName()] = g.Eval(mass) 
   fin.Close() 
   uncs['qq_PDF_Wprime']=WprimeWZunc.Eval(mass)
   uncs['qq_PDF_Zprime']=ZprimeWWunc.Eval(mass)
   uncs['gg_PDF_WW']=BulkGWWunc.Eval(mass)
   uncs['gg_PDF_ZZ']=BulkGZZunc.Eval(mass)
   uncs['qW_PDF']=qStarqWunc.Eval(mass)
   uncs['qZ_PDF']=qStarqZunc.Eval(mass)
   return uncs

prefixDCin  = "datacards/CMS_jj_"
prefixDCout = "datacards_withNewPDFandScaleUnc/CMS_jj_"

signals=["BulkWW","BulkZZ","WZ","ZprimeWW","qW","qZ"]
purities = ["LP","HP"]

# signals=["WZ"]
# masses = [1200]
     
for signal in signals:

 if "q" in signal:
    masses =[m*100/2 for m in range(2*10,2*40+1)]
    masses =[m*100 for m in range(12,62+1)]
    channels = ["qW","qZ"]
 else:
    masses =[m*50 for m in range(20,80+1)]
    masses =[m*100 for m in range(11,42+1)]
    channels = ["WW","WZ","ZZ"]

 for mass in masses:
   print "mass = ",mass

   xsecUnc	=  get_xsec_unc(mass)
  
   pdf_Wprime	= 1.+xsecUnc['qq_PDF_Wprime']
   pdf_Zprime	= 1.+xsecUnc['qq_PDF_Zprime']
   scale_Wprime = 1.+xsecUnc['qq_scale_Wprime']
   scale_Zprime = 1.+xsecUnc['qq_scale_Zprime']
   pdf_BulkWW	= 1.+xsecUnc['gg_PDF_WW']
   pdf_BulkZZ	= 1.+xsecUnc['gg_PDF_ZZ']
   scale_Bulk	= 1.+xsecUnc['gg_scale']
   pdf_qW   = 1.+xsecUnc['qW_PDF']
   pdf_qZ   = 1.+xsecUnc['qZ_PDF']
   scale_qW=1.
   scale_qZ=1.
 
   if signal.find("Bulk") != -1:
     newline1 = '\nCMS_XS_gg_PDF                lnN				    '
     newline2 = '\nCMS_XS_gg_scale              lnN				    '
   else: 
     newline1 = '\nCMS_XS_qq_PDF                lnN				    '
     newline2 = '\nCMS_XS_qq_scale              lnN				    '
       
   if signal.find("BulkWW") != -1:
     pdf   =  pdf_BulkWW  
     scale =  scale_Bulk
   elif signal.find("BulkZZ") != -1:
     pdf   =  pdf_BulkZZ  
     scale =  scale_Bulk
   elif signal.find("Zprime") != -1:
       pdf   = pdf_Zprime
       scale = scale_Zprime
   elif signal.find("WZ") != -1:
       pdf   = pdf_Wprime
       scale = scale_Wprime
   elif signal.find("qW") != -1:
       pdf   = pdf_qW
       scale = scale_qW
   elif signal.find("qZ") != -1:
       pdf   = pdf_qZ
       scale = scale_qZ
   else:
       signaluncertaintynotfound
 
   newline1+="%.3f        %.3f        -" %(pdf   ,pdf)
   newline2+="%.3f        %.3f        -" %(scale ,scale)
   
   print newline1
   print newline2
   
   for purity in purities:
     for ch in channels:
       
       fname_datacard_in  = prefixDCin  + "%s_%i"%(signal,mass)+"_13TeV_CMS_jj_"+ch+purity+".txt"
       fname_datacard_out = prefixDCout + "%s_%i"%(signal,mass)+"_13TeV_CMS_jj_"+ch+purity+".txt"
       lines = []   
       try:
         print " Opening " , fname_datacard_in
         with open(fname_datacard_in) as infile:
           for line in infile:
             if not line.find("CMS_XS_")!=-1:
               lines.append(line)
           
           lines.append(newline1)
           lines.append(newline2)
           with open(fname_datacard_out, 'w') as outfile:
             print " Writing to " , fname_datacard_out
             for line in lines:
               outfile.write(line)
       except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
           print 'oops, datacard not found!'
       
 
 
  
