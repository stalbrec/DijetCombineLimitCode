#!/usr/bin/python
from optparse import OptionParser
import os,commands, os.path
import sys
from ROOT import *
import math
import time
import copy
from array import *
import CMS_lumi, tdrstyle
from ROOT import TVirtualFitter
from heapq import nsmallest

tdrstyle.setTDRStyle()
#gStyle.SetOptFit(0) 
gROOT.SetBatch(True)
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4

legend_text = "CMS data"
suffix = "_MC_SR_test"
if legend_text.find("CMS")!=-1:
    suffix = "_SB"
sqrtS = 13000.
lumi =  36500.#12900.

def get_palette(mode):
 palette = {}
 palette['gv'] = [] 
 colors = ['#40004b','#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
 colors = ['#A43820','#598934','#2A3132','#505160','#763626','#003B46','#66A5AD']
 for c in colors:
  palette['gv'].append(c)
 return palette[mode]
 
palette = get_palette('gv')
col = TColor()
markerStyles = [20,22,26,20,22,26]

def performFit(fInputFile, fPlot, fNbins, fBins,fFitXmin, fFitXmax,fLabel,  fOutputFile,doSigmaBand):
  
  fits = []
  residuals = []
  
  xbins = array('d',fBins)

  file =TFile(fInputFile,"READ")
  hMass = file.Get(fPlot)
  hMass.SetBinErrorOption(TH1.kPoisson)

  
  firstbin = hMass.GetBinCenter(hMass.FindFirstBinAbove(0.99999))
  lastbin = hMass.GetBinCenter(hMass.FindLastBinAbove(0.19999))   #contained 0.99999
  lower = (nsmallest(2, fBins, key=lambda x: abs(x-lastbin)))[0]
  higher  = (nsmallest(2, fBins, key=lambda x: abs(x-lastbin)))[1]
  if lower > higher:
    fFitXmax = lower
  if higher > lower:
    fFitXmax = higher
  fFitXmax = lastbin    
  #fFitXmin = firstbin
  print "Last non-zero bin is at x=%f. Closest dijet mass bins are L = %i  H = %i" %(lastbin,lower,higher)
  print "Using x max = %i" %fFitXmax
  print "Using x min = %i" %fFitXmin

  hMass_rebinned = hMass.Rebin(fNbins,"hMass_rebinned",xbins)
  
  hMassNEW = TH1F("hist_mass","",fNbins,xbins)

# --------------------------------------- Filling new h dividing by binwidth ---------------------------------------
  alpha = 1 - 0.6827
  for i in range (1,fNbins):
    bincontent = hMass_rebinned.GetBinContent(i)
    binwidth = hMass_rebinned.GetBinWidth(i)
    hMassNEW.SetBinContent(i,bincontent/(binwidth))
    
    # if(bincontent==0): l = 0
#     else: l = Math.gamma_quantile(alpha/2,bincontent,1.) #as recommended in https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars
#     h = Math.gamma_quantile_c(alpha/2,bincontent+1,1)
#     eDATA_L = (bincontent-l)/(binwidth)
#     eDATA_H = (h-bincontent)/(binwidth)
#     if(eDATA_L > eDATA_H):
#       hMassNEW.SetBinError(i,eDATA_L)
#     elif(eDATA_H > eDATA_L):
#       hMassNEW.SetBinError(i,eDATA_H)


# ---------------------------- Create graph from data with Poisson error bars (for data) ----------------------------    
  x=[]
  y=[]
  exl=[]
  exh=[]
  eyl=[]
  eyh=[]
  alpha = 1 - 0.6827
  hMass_rebinned.SetBinErrorOption(TH1.kPoisson)
  for i in range(0,fNbins):
    n    = hMass_rebinned.GetBinContent(i+1)
    dm   = hMass_rebinned.GetBinWidth(i+1)
    mass = hMass_rebinned.GetBinCenter(i+1)
    xl   = hMass_rebinned.GetBinLowEdge(i+1)
    xh   = xl+dm
    x.append( (xl+xh)/2.)
    exl.append( dm/2.)
    exh.append( dm/2.)
    y.append( n / (dm))
    test = n/dm
    # l = 0.5*TMath.ChisquareQuantile(alpha/2,2*n) #as used in dijet analysis
    # h = 0.5*TMath.ChisquareQuantile(1-alpha/2,2*(n+1))
    if(n==0): 
        l = 0
    else: l = Math.gamma_quantile(alpha/2,n,1.) #as recommended in https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars
    h = Math.gamma_quantile_c(alpha/2,n+1,1) 
    eyl.append( (n-l)/(dm) )
    eyh.append( (h-n)/(dm) )
    
    print "============================="
    print mass
    print "error l : %f"%((n-l)/dm)
    print hMass_rebinned.GetBinErrorLow(i+1)/dm
    print "error h : %f"%((h-n)/dm)
    print hMass_rebinned.GetBinErrorUp(i+1)/dm
    print " l : %f"%l
    print "n : %f"%n
    print n-l
    print "dm %f"%dm
    print "n/dm %f"%(n/dm)
    print " sqrt(n)/dm : %f"%(TMath.Sqrt(n)/dm)
    print " sqrt(n/dm) : %f"%TMath.Sqrt(n/dm)
  
  vx = array("f",x)
  vy = array("f",y)
  vexl = array("f",exl)
  vexh = array("f",exh)
  veyl = array("f",eyl)
  veyh = array("f",eyh)
  
  #data in TGraph format
  g = TGraphAsymmErrors(fNbins,vx,vy,vexl,vexh,veyl,veyh)
  g.SetName("g_data")

  nBins_fit1 = hMassNEW.FindBin(fFitXmax)- hMassNEW.FindBin(fFitXmin)
  zeroBins = 0
  for i in range(0,nBins_fit1):
    if hMassNEW.GetBinContent(hMassNEW.FindBin(fFitXmin)+i)==0:
      zeroBins +=1        
  nBins_fit = nBins_fit1 - zeroBins
  
  rss = []
  chi2 = []
  dof = []
  fisher = []
  ConfidenceLevel = []
  ConfidenceLevel2 = []
  fpdfs = []
  histoCI = []
  
  f = 0
  FunctionTypes = [-2,0,1,3]
  for FunctionType in FunctionTypes:
    fitresult = doFit(FunctionType,hMassNEW,g,fFitXmin,fFitXmax,fNbins,xbins,fLabel)
    M1Bkg = fitresult[3]
    hist_fit_residual_vsMass = fitresult[4]
    nPar = nBins_fit - fitresult[1] - 1
    fits.append(M1Bkg)
    residuals.append(hist_fit_residual_vsMass)
    rss.append(fitresult[0])
    chi2.append(fitresult[2])
    dof.append(fitresult[1])
    if (doSigmaBand): histoCI.append(fitresult[6])
    
    print "Calculated Chi2 / dof for f%d = %f / %d" % (FunctionType,fitresult[2],fitresult[1])
    if (0<f<3):
      result = FisherTest(rss[f-1],rss[f],dof[f-1],dof[f],nBins_fit)
      # if (f>3):
 #        result = FisherTest(rss[1],rss[f],dof[1],dof[f],nBins_fit) #now comparing alternate four paramter fit to 3 paramter fit
      F = (result[0])
      CL = result[1]
      fisher.append(F)
      ConfidenceLevel.append(CL)
      CL2 = result[2]
      ConfidenceLevel2.append(CL2)
      fpdfs.append(result[3])
    f += 1
# --------------------------------------- Print some results ---------------------------------------
 
  print ""
  print "FOR CATEGORY: %s" %fLabel
  print ""
  print "Summary:"
  print "Residuals = "+str(rss)
  print "$\chi^2$ = "+str(chi2)
  print "D.O.F ="+str(dof)
  print "Fishers F = "+str(fisher)
  print "ConfidenceLevel = "+str(ConfidenceLevel)
  print "Alternate CL (using TMath.FDistI) = "+str(ConfidenceLevel2)
  print "Functions = "+str(FunctionTypes)
  print "Nr. bins in fit = "+str(nBins_fit)
  print "-----------------------------------------"
  print ""
  alpha = 0.1
  print  " F - test results using alternate method: " 
  print "-----------------------------------------"
  if (ConfidenceLevel2[0]>alpha):
    prmt = 2
    print  "A two parameter fit is sufficient to describe these data" 
  elif (ConfidenceLevel2[1]>alpha):
    prmt = 3
    print  " A three parameter fit is sufficient to describe these data." 
  # elif (ConfidenceLevel2[2]>alpha):
#     prmt = 4
#     print  " A four parameter fit appears adequate to describe these data."
#   # elif (ConfidenceLevel[3]>alpha):
#     # print  " The alternate fit is better than the 3 parameter default fit"
  else:
    prmt = 4
    # print  " A better fit is needed for these data. "
#     print  " You should check for higher-order polynomials. "
  print  " A four parameter fit is needed to describe these data "
  print "-----------------------------------------"
  print ""
  print "For Latex table:"
  print ""
  print"\\begin{table}[htb]"
  print"\centering"
  print"\\begin{tabular}{|l c c c |}"
  print"\hline"
  print "\multicolumn{4}{|c|}{%s}\\\\"%fLabel
  print "\hline"
  print "Function & Residuals & $\chi^2$ & ndof \\\\"
  print "\hline"
  print "2 par & %.3f & %.3f & %i \\\\"%(rss[0],chi2[0],dof[0])
  print "3 par & %.3f & %.3f & %i \\\\"%(rss[1],chi2[1],dof[1])
  print "4 par & %.3f & %.3f & %i \\\\"%(rss[2],chi2[2],dof[2])
  # print "5 par & %.3f & %.3f & %i \\\\"%(rss[3],chi2[3],dof[3])
  # print "Alt. 4 par& %.3f & %.3f & %i \\"%(rss[4],chi2[4],dof[4])
  print "\hline"
  print "\hline"
  print "Fishers23 \multicolumn{2}{l}{%.3f}&CL \multicolumn{2}{l|}{%.3f}\\\\"%(fisher[0],ConfidenceLevel2[0])
  print "Fishers34 \multicolumn{2}{l}{%.3f}&CL \multicolumn{2}{l|}{%.3f}\\\\"%(fisher[1],ConfidenceLevel2[1])
  # print "Fishers45 \multicolumn{2}{l}{%.3f}&CL \multicolumn{2}{l|}{%.3f}\\\\"%(fisher[2],ConfidenceLevel2[2])
  # print "Fishers3Alt4 \multicolumn{2}{l}{%.3f}&CL \multicolumn{2}{l|}{%.3f}\\"%(fisher[3],ConfidenceLevel[3])
  print "\hline"
  print "\end{tabular}"
  print "\caption{Residuals, $\chi^{2}$, and degrees of freedom for %s category. A %i parameter fit is needed to describe these data.}"%(fLabel,prmt)
  print "\label{tab:%s}"%fLabel
  print "\end{table}"
  with open("ftest_2016/f-test_VV.tex", "a") as text_file:
    text_file.write("\\begin{table}[htb]\n")
    text_file.write("\centering\n")
    text_file.write("\\begin{tabular}{|l c c c |}\n")
    text_file.write("\hline\n")
    text_file.write( "\multicolumn{4}{|c|}{%s}\\\\\n"%fLabel)
    text_file.write( "\hline\n")
    text_file.write( "Function & Residuals & $\chi^2$ & ndof \\\\\n")
    text_file.write( "\hline\n")
    text_file.write( "2 par & %.3f & %.3f & %i \\\\\n"%(rss[0],chi2[0],dof[0]))
    text_file.write( "3 par & %.3f & %.3f & %i \\\\\n"%(rss[1],chi2[1],dof[1]))
    text_file.write( "4 par & %.3f & %.3f & %i \\\\\n"%(rss[2],chi2[2],dof[2]))
    # text_file.write( "5 par & %.3f & %.3f & %i \\\\\n"%(rss[3],chi2[3],dof[3]))
    # text_file.write( "Alt. 4 par& %.3f & %.3f & %i \\"%(rss[4],chi2[4],dof[4])
    text_file.write( "\hline\n")
    text_file.write( "\hline\n")
    text_file.write( "Fishers23 \multicolumn{2}{l}{%.3f}&CL \multicolumn{2}{l|}{%.3f}\\\\\n"%(fisher[0],ConfidenceLevel2[0]))
    text_file.write( "Fishers34 \multicolumn{2}{l}{%.3f}&CL \multicolumn{2}{l|}{%.3f}\\\\\n"%(fisher[1],ConfidenceLevel2[1]))
    # text_file.write( "Fishers45 \multicolumn{2}{l}{%.3f}&CL \multicolumn{2}{l|}{%.3f}\\\\\n"%(fisher[2],ConfidenceLevel2[2]))
    # text_file.write( "Fishers3Alt4 \multicolumn{2}{l}{%.3f}&CL \multicolumn{2}{l|}{%.3f}\\"%(fisher[3],ConfidenceLevel[3]))
    text_file.write( "\hline\n")
    text_file.write( "\end{tabular}\n")
    text_file.write( "\caption{Residuals, $\chi^{2}$, and degrees of freedom for the %s category. A %i parameter fit is needed to describe these data.}\n"%(fLabel,prmt))
    text_file.write( "\label{tab:%s}\n"%fLabel)
    text_file.write( "\end{table}\n")

  # DrawFit(hMassNEW,g,fits,residuals,FunctionType,nPar,fFitXmin,fFitXmax,fLabel,fOutputFile) #when final fit is decided, plots only one fit
  FitComparisons(hMassNEW,g,fits,residuals,FunctionType,nPar,fFitXmin,fFitXmax,fLabel,fOutputFile,chi2,dof,doSigmaBand,histoCI) #draw all fit functions with residuals
  
  del file
  
def doFit(FunctionType,hMassNEW,g,fFitXmin,fFitXmax,fNbins,xbins,fLabel):
  print ""
  print ""
  print ""
  print ""
  
  if( FunctionType==-2 ):
    nPar=2
    BKGfit = TF1("BKGfit%i"%FunctionType," [0] / ( TMath::Power(x/13000,[1]) )",fFitXmin,fFitXmax)
 
     # signal region: 
    if fLabel.find("WW") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0,1.98680e-09)
      BKGfit.SetParameter(1,8.66744e+00)
    elif fLabel.find("WW") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0,1.13062e-07)
      BKGfit.SetParameter(1,7.85359e+00)  
    elif fLabel.find("WZ") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0,7.09589e-09)
      BKGfit.SetParameter(1,8.54541e+00)
    elif fLabel.find("WZ") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0,1.50873e-07)
      BKGfit.SetParameter(1,8.03595e+00)
    elif fLabel.find("ZZ") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0,1.82729e-09)
      BKGfit.SetParameter(1,8.92196e+00)
    elif fLabel.find("ZZ") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0,6.82046e-08)
      BKGfit.SetParameter(1,8.08889e+00)
      # sideband region: 
    if fLabel.find("WW") != -1 and fLabel.find("HP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0,1.98680e-09)
      BKGfit.SetParameter(1,8.66744e+00)
    elif fLabel.find("W") != -1 and fLabel.find("LP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0,1.13062e-07)
      BKGfit.SetParameter(1,7.85359e+00)  
    elif fLabel.find("Z") != -1 and fLabel.find("HP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0,7.09589e-09)
      BKGfit.SetParameter(1,8.54541e+00)
    elif fLabel.find("Z") != -1 and fLabel.find("LP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0,1.50873e-07)
      BKGfit.SetParameter(1,8.03595e+00)
      
  if( FunctionType==0 ):
    print "Fitting three parameter default function!"
    nPar=3
    BKGfit = TF1("BKGfit%i"%FunctionType,"( [0]*TMath::Power(1-x/13000,[1]) ) / ( TMath::Power(x/13000,[2]) )",fFitXmin,fFitXmax)
   
    
    # signal region:
    if fLabel.find("WW") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0,7.68629e-09 )       
      BKGfit.SetParameter(1,8.35270e+00 )
      BKGfit.SetParameter(2, 0.)
      #BKGfit.SetParameter(0, 9.01237e-12)
      #BKGfit.SetParameter(1,-1.58982e+01)
      #BKGfit.SetParameter(2, 1.02766e+01)
      BKGfit.SetParLimits(2,7,20)
    elif fLabel.find("WW") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0,3.75544e-07)
      BKGfit.SetParameter(1,3.37623e+00)
      BKGfit.SetParameter(2,7.49005e+00)
    elif fLabel.find("WZ") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0,7.09589e-09)
      BKGfit.SetParameter(1,8.54541e+00)
      BKGfit.SetParameter(2, 8.87103e+00)
    elif fLabel.find("WZ") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0,1.50874e-07)
      BKGfit.SetParameter(1,8.03595e+00)
      BKGfit.SetParameter(2,7.37063e+00)
    elif fLabel.find("ZZ") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0,1.06871e-08)
      BKGfit.SetParameter(1,1.03718e+00)
      BKGfit.SetParameter(2,8.38073e+00)
      BKGfit.SetParLimits(2, 8.2e+00 ,8.4e+00 )
      BKGfit.SetParLimits(1, 1.03718e+00 , 1.03718e+00)
    elif fLabel.find("ZZ") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0,6.82046e-08)
      BKGfit.SetParameter(2,8.08889e+00)
      BKGfit.SetParameter(1,0.00000000 )
    
    # sideband region:
    if fLabel.find("WW") != -1 and fLabel.find("HP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0, 9.01237e-12)
      BKGfit.SetParameter(1,-1.58982e+01)
      BKGfit.SetParameter(2, 1.02766e+01)
    elif fLabel.find("WW") != -1 and fLabel.find("LP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0,3.75544e-07)
      BKGfit.SetParameter(1,3.37623e+00)
      BKGfit.SetParameter(2,7.49005e+00) 
    elif fLabel.find("ZZ") != -1 and fLabel.find("HP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0,1.82729e-09)
      BKGfit.SetParameter(1,8.92196e+00)
      BKGfit.SetParameter(2,9.48734e+00)
    elif fLabel.find("ZZ") != -1 and fLabel.find("LP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0,6.82046e-08)
      BKGfit.SetParameter(2,8.08889e+00)
      BKGfit.SetParameter(1,0.00000000 )
    
          
  elif( FunctionType==1 ):
    print "Fitting four parameter default function!"
    nPar=4
    BKGfit = TF1("BKGfit%i"%FunctionType,"( [0]*TMath::Power(1-x/13000,[1]) ) / ( TMath::Power(x/13000,[2]+[3]*log(x/13000)) )",fFitXmin,fFitXmax)
    
    
    # signal region: 
    if fLabel.find("WW") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0,   2.45156e-02) #6.48238e-13 )
      BKGfit.SetParameter(1,  2.60131e+01 ) #1.11517e+00 )
      BKGfit.SetParameter(2,  1.17317e+00 ) #1.02840e+01 )
      BKGfit.SetParameter(3, -8.19261e-01 ) #8.45161e+03 )
      #BKGfit.FixParameter(3,0 )
      #BKGfit.SetParLimits(1,  2.60131e+01, 2.60131e+01)
      #BKGfit.SetParLimits(2,0,10)
      #BKGfit.SetParLimits(3,-8.19261e-01,-8.19261e-01)
      #BKGfit.SetParLimits(0,3.01257e-12,9.01257e-12)
    elif fLabel.find("WW") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0,3.72696e-07)
      BKGfit.SetParameter(1,3.35574e+00)
      BKGfit.SetParameter(2,7.49238e+00)
      BKGfit.SetParameter(3,-4.10905e-07)
    elif fLabel.find("WZ") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0,7.09589e-09)
      BKGfit.SetParameter(1,8.54541e+00)
      BKGfit.SetParameter(2, 8.87103e+00)
      BKGfit.SetParameter(3,-8.14899e-02)
    elif fLabel.find("WZ") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0,1.50873e-07)
      BKGfit.SetParameter(1,8.03595e+00)
      BKGfit.SetParameter(2,7.96865e+00)  
      BKGfit.SetParameter(3,9.66574e-02)
    elif fLabel.find("ZZ") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0, 5.90181e-02)# 1.82729e-09)
      BKGfit.SetParameter(1, 2.12431e+01)# 8.92196e+00)
      BKGfit.SetParameter(2,-1.00178e+00)# 4.76973e+00)
      BKGfit.SetParameter(3,-1.54769e+00)#-7.21037e-01)
      #BKGfit.SetParLimits(3, -1.54769e+00,-1.54769e+00)
      #BKGfit.SetParLimits(2,-1.00178e+00,-1.00178e+00 )
      #BKGfit.SetParLimits(1,2.12431e+01,2.12431e+01 )
      #BKGfit.SetParLimits(0,  5.90181e-02, 5.90181e-02)
    elif fLabel.find("ZZ") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0,6.82046e-08)
      BKGfit.SetParameter(2,8.08889e+00)
      BKGfit.SetParameter(1,0.00000000 )
      BKGfit.SetParameter(3,0.00000000 )
      
    # sideband region:
    if fLabel.find("WW") != -1 and fLabel.find("HP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0, 9.01257e-12)
      BKGfit.SetParameter(1,-1.09759e+01)
      BKGfit.SetParameter(2, 8.55014e+00)
      BKGfit.SetParameter(3,-1 )# -2.54954e-01)
      BKGfit.SetParLimits(3,-10,0)
    elif fLabel.find("WW") != -1 and fLabel.find("LP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0,3.72696e-07)
      BKGfit.SetParameter(1,3.35574e+00)
      BKGfit.SetParameter(2,7.49238e+00)
      BKGfit.SetParameter(3,-4.10905e-07)
    elif fLabel.find("ZZ") != -1 and fLabel.find("HP") != -1 and fLabel.find("SB")!=-1 :
      BKGfit.SetParameter(0,1.82729e-09)
      BKGfit.SetParameter(1,8.92196e+00)
      BKGfit.SetParameter(2, 4.76973e+00)
      BKGfit.SetParameter(3,-7.21037e-01)
    elif fLabel.find("ZZ") != -1 and fLabel.find("LP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0,6.82046e-08)
      BKGfit.SetParameter(2,8.08889e+00)
      BKGfit.SetParameter(1,0.00000000 )
      BKGfit.SetParameter(3,0.00000000 )
      
  elif( FunctionType==3 ):
    print "Fitting four parameter alternate function!"
    nPar=4
    BKGfit =  TF1("BKGfit%i"%FunctionType,"( [0]*TMath::Power(1-x/13000 + [3]*TMath::Power(x/13000,2),[1]) ) / ( TMath::Power(x/13000,[2]) )",fFitXmin,fFitXmax)
    
      
    
    # signal region:
    if fLabel.find("WW") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0,2.21926e-13) 
      BKGfit.SetParameter(1,2.25629e+00) 
      BKGfit.SetParameter(2,1.15338e+01) 
      BKGfit.SetParameter(3,2.11319e+02) 
      # BKGfit.SetParLimits(0,0.21926e-13,4.21926e-13) #WWHP
    elif fLabel.find("WW") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0,1.44775e-05 ) 
      BKGfit.SetParameter(1,2.05225e+01 ) 
      BKGfit.SetParameter(2,6.50590e+00 ) 
      BKGfit.SetParameter(3,1.86664e+00 ) 
    elif fLabel.find("WZ") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0,1.19345e-05) 
      BKGfit.SetParameter(1,3.73975e+01) 
      BKGfit.SetParameter(2,6.58579e+00) 
      BKGfit.SetParameter(3,2.48983e+00) 
    elif fLabel.find("WZ") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0,1.36722e-06)
      BKGfit.SetParameter(1,6.63254e+00)
      BKGfit.SetParameter(2,7.37687e+00)
      BKGfit.SetParameter(3,3.28215e-01)
    elif fLabel.find("ZZ") != -1 and fLabel.find("HP") != -1:
      BKGfit.SetParameter(0, 2.45629e-09 )
      BKGfit.SetParameter(1,-4.58690e+00 )
      BKGfit.SetParameter(2, 8.80612e+00 )
      BKGfit.SetParameter(3, 2.05830e+00 )
      #BKGfit.SetParLimits(2, 8.80612e+00, 8.80612e+00)
      #BKGfit.SetParLimits(3, 2.05830e+00, 2.05830e+00)
    elif fLabel.find("ZZ") != -1 and fLabel.find("LP") != -1:
      BKGfit.SetParameter(0, 1.74162e-06)
      BKGfit.SetParameter(1,-8.47400e-01)
      BKGfit.SetParameter(2, 7.05095e+00)
      BKGfit.SetParameter(3, 1.79446e+02)
      
    #sideband region:
    if fLabel.find("W") != -1 and fLabel.find("HP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0,2.21926e-13) 
      BKGfit.SetParameter(1,2.25629e+00) 
      BKGfit.SetParameter(2,1.15338e+01) 
      BKGfit.SetParameter(3,2.11319e+02) 
    elif fLabel.find("W") != -1 and fLabel.find("LP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0,1.44775e-05 ) 
      BKGfit.SetParameter(1,2.05225e+01 ) 
      BKGfit.SetParameter(2,6.50590e+00 ) 
      BKGfit.SetParameter(3,1.86664e+00 ) 
    elif fLabel.find("Z") != -1 and fLabel.find("HP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0, 1.82729e-09)
      BKGfit.SetParameter(1, 8.92196e+00)
      BKGfit.SetParameter(2, 4.76973e+00)
      BKGfit.SetParameter(3,-7.21037e-01)
    elif fLabel.find("Z") != -1 and fLabel.find("LP") != -1 and fLabel.find("SB")!=-1:
      BKGfit.SetParameter(0, 1.74162e-06)
      BKGfit.SetParameter(1,-8.47400e-01)
      BKGfit.SetParameter(2, 7.05095e+00)
      BKGfit.SetParameter(3, 1.79446e+02)
          
  stopProgram=1;
  for loop in range (0,10):
    r = hMassNEW.Fit("BKGfit%i"%FunctionType,"BISR","",fFitXmin,fFitXmax)
    fitStatus = int(r)
    print "fit status : %d" % fitStatus
    if(fitStatus==0):
      stopProgram=0
      # r.Print("V")
      break
  c1 = TCanvas("c3","fit",600,400)
  hMassNEW.Draw();
  suffix ="WHP";
  if fLabel.find('W')!=-1:
      suffix ="W"
  if fLabel.find('Z')!=-1:
      suffix ="Z"
  if fLabel.find('Z')!=-1:
      suffix ="Z"
  if fLabel.find('WW')!=-1:
      suffix ="WW"
  if fLabel.find('WZ')!=-1:
      suffix ="WZ"
  if fLabel.find('ZZ')!=-1:
      suffix ="WZ"
      
  if fLabel.find('HP')!=-1:
      suffix +="HP"
  if fLabel.find('LP')!=-1:
      suffix +="LP"
  c1.SaveAs("ftest_2016/test_"+suffix+".pdf");
  #if(stopProgram==1):
   # print "######################"
   # print"######################"
   # print "ERROR : Fit %i failed!!!!" %FunctionType
   # print "######################"
   # print "######################"
   # sys.exit()
  
  
  #Create a histogram to hold the confidence intervals
  # histoCI=TH1D("histoCI","", fNbins,xbins)
  # # histoCI=TH1D()
  # histoCI.SetTitle("Fitted histogram with .95 conf. band")
  # (TVirtualFitter.GetFitter()).GetConfidenceIntervals(histoCI)
  # #Now the "hint" histogram has the fitted function values as the
  # #bin contents and the confidence intervals as bin errors
  # histoCI.SetStats(kFALSE)
  # histoCI.SetFillColor(kRed+2)
  # histoCI.SetLineColor(kRed+2)
  # histoCI.SetFillStyle(3354)


  histoCI = TGraphErrors(fNbins)
  histoCI.SetTitle("Fitted line with .95 conf. band")
  for i in range (0, fNbins):
    histoCI.SetPoint(i, g.GetX()[i], 0)
  #Compute the confidence intervals at the x points of the created graph
  (TVirtualFitter.GetFitter()).GetConfidenceIntervals(histoCI)
  # //Now the "grint" graph contains function values as its y-coordinates
 #  //and confidence intervals as the errors on these coordinates
 #  //Draw the graph, the function and the confidence intervals
  histoCI.SetLineColor(0)
  histoCI.SetLineWidth(-802)
  histoCI.SetFillStyle(3002)
  histoCI.SetFillColor(2)  
  
  NumberOfVarBins = 0
  NumberOfObservations_VarBin = 0
  chi2_VarBin = 0.
  chi2_VarBin_notNorm = 0.
  hist_fit_residual_vsMass =  TH1D("hist_fit_residual_vsMass","hist_fit_residual_vsMass",fNbins,xbins)
  
  for bin in range (1,hMassNEW.GetNbinsX()):
    if( hMassNEW.GetXaxis().GetBinLowEdge(bin)>=fFitXmin and hMassNEW.GetXaxis().GetBinUpEdge(bin)<=fFitXmax ):
       NumberOfVarBins += 1
       data = hMassNEW.GetBinContent(bin)
       # data = g.Integral(hMassNEW.GetXaxis().GetBinLowEdge(bin) , hMassNEW.GetXaxis().GetBinUpEdge(bin) )
       err_data_low = g.GetErrorYlow(bin-1) 
       err_data_high= g.GetErrorYhigh(bin-1)
       fit = BKGfit.Integral(hMassNEW.GetXaxis().GetBinLowEdge(bin) , hMassNEW.GetXaxis().GetBinUpEdge(bin) )
       fit = fit / ( hMassNEW.GetBinWidth(bin) )
       # fit = BKGfit.Eval(hMassNEW.GetBinCenter(bin)) #yields same results
       if(fit > data):
         err_tot = err_data_high
       else:
         err_tot = err_data_low
       if err_tot!=0:  
            fit_residual = (data - fit) / err_tot
       else:
           print "Warning: err_tot = 0 !"
           fit_residual = 0
       err_fit_residual = 1
       
       if (hMassNEW.GetBinContent(bin)>0):
         NumberOfObservations_VarBin+=1
         print "(data-fit)**2 = "+str(pow( (data - fit) , 2 ))+" err_tot : "+str(err_tot)
         print chi2_VarBin
         chi2_VarBin += pow( (data - fit) , 2 ) / pow( err_tot , 2 )
         chi2_VarBin_notNorm += pow( (data - fit) , 2 )

       hist_fit_residual_vsMass.SetBinContent(bin,fit_residual)
       hist_fit_residual_vsMass.SetBinError(bin,err_fit_residual)
  
  ndf_VarBin = NumberOfObservations_VarBin - nPar -1 #ndof    
  return [chi2_VarBin_notNorm,ndf_VarBin,chi2_VarBin,BKGfit,hist_fit_residual_vsMass,nPar,histoCI]   

def FisherTest(RSS_1,RSS_2,dof_1,dof_2,N):
  RSS1 = RSS_1
  RSS2 = RSS_2
  n1 = N - dof_1 - 1
  n2 = N - dof_2 - 1
  F = (((RSS1-RSS2)/(n2-n1)) / (RSS2/(N-n2)))
  F_dist = TF1("F_distr","TMath::Sqrt( (TMath::Power([0]*x,[0]) * TMath::Power([1],[1])) / (TMath::Power([0]*x + [1],[0]+[1])) ) / (x*TMath::Beta([0]/2,[1]/2))",0,1000)
  F_dist.SetParameter(0, n2-n1)
  F_dist.SetParameter(1, N-n2)
  CL = 1 - F_distr.Integral(0.00000001,F)
  alternateCL =  1.-TMath.FDistI(F,n2-n1,N-n2)
  return [F,CL,alternateCL,F_dist]

def DrawFit(hMassNEW,g,M1Bkg,hist_fit_residual_vsMass,FunctionType,nPar,fFitXmin,fFitXmax,fLabel,fOutputFile):
  W = 600
  H = 700
  H_ref = 700 
  W_ref = 600 
  T = 0.08*H_ref
  B = 0.12*H_ref
  L = 0.12*W_ref
  R = 0.04*W_ref

  c1 = TCanvas("c1","VV mass fit",W,H)
  c1.GetWindowHeight()
  c1.GetWindowWidth()
  c1.SetLogy()
  c1.Divide(1,2,0,0,0)

  #------------ pad 1  ----------------
  c1.cd(1)
  p11_1 = c1.GetPad(1)
  p11_1.SetPad(0.01,0.26,0.99,0.98)
  p11_1.SetLogy()
  p11_1.SetRightMargin(0.05)
  p11_1.SetTopMargin(0.05)
  p11_1.SetFillColor(0)
  p11_1.SetBorderMode(0)
  p11_1.SetFrameFillStyle(0)
  p11_1.SetFrameBorderMode(0)

  #Pave text
  #addInfo = TPaveText(0.1558691,0.30735043,0.3750171,0.4070085,"NDC")
  addInfo = TPaveText(0.2358691,0.04035043,0.5050171,0.1870085,"NDC")
  
  addInfo.AddText(fLabel)
  # addInfo.AddText("65 GeV < M_{P} < 105 GeV")
  # addInfo.AddText("|#eta| < 2.4, p_{T} > 200 GeV")
  # addInfo.AddText("Pruned mass sideband")
  # addInfo.AddText("M_{jj} > 1 TeV, |#Delta#eta_{jj}| < 1.3")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  
  vFrame = p11_1.DrawFrame(fFitXmin,0.000005,fFitXmax,hMassNEW.GetMaximum()*5.0)  
  vFrame.SetTitle("")
  vFrame.SetXTitle("M_{jj} (GeV)")
  vFrame.SetYTitle("#frac{dN}{dm_{jj}} (GeV^{-1})")
  vFrame.GetXaxis().SetTitleSize(0.06)
  vFrame.GetXaxis().SetTitleOffset(0.95)
  vFrame.GetXaxis().SetLabelSize(0.05)
  vFrame.GetYaxis().SetTitleSize(0.06)
  #vFrame.GetYaxis().SetTitleOffset(1.0)
  vFrame.GetYaxis().SetLabelSize(0.05)

  g.SetMarkerSize(0.9)
  g.SetMarkerStyle(20)
  g.GetXaxis().SetNdivisions(405)
  g.Draw("pe0 same")
  M1Bkg[0].SetLineWidth(2)
  M1Bkg[0].SetLineStyle(1)
  M1Bkg[0].SetLineColor(kRed)
  M1Bkg[0].Draw("same")

 
  legend = TLegend(0.56164991,0.62,0.8503575,0.80)
  legend.SetTextSize(0.038)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  legend.AddEntry(g,legend_text,"lpe")
  legend.AddEntry(M1Bkg[0], "Fit","l")
  # legend.AddEntry(M1Bkg[3], "Fit","l")
  legend.Draw("same")
  addInfo.Draw("same")
  p11_1.RedrawAxis()
  p11_1.Update()
  p11_1.GetFrame().Draw()
  CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)
  
  c1.cd(2)
  p11_2 = c1.GetPad(2)
  p11_2.SetPad(0.01,0.02,0.99,0.27)
  p11_2.SetBottomMargin(0.35)
  p11_2.SetRightMargin(0.05)
  p11_2.SetGridx()
  p11_2.SetGridy()
  vFrame2 = p11_2.DrawFrame(p11_1.GetUxmin(), -3.5, p11_1.GetUxmax(), 3.5)
  # vFrame2 = p11_2.DrawFrame(fFitXmin,-3.5,fFitXmax,3.5)
  vFrame2.SetTitle("")
  vFrame2.SetXTitle("M_{jj} (GeV)")
  vFrame2.GetXaxis().SetTitleSize(0.06)
  vFrame2.SetYTitle("#frac{Data-Fit}{#sigma}")
  vFrame2.GetYaxis().SetTitleSize(0.15)
  vFrame2.GetYaxis().SetTitleOffset(0.40)
  vFrame2.GetYaxis().SetLabelSize(0.09)
  vFrame2.GetXaxis().SetTitleSize(0.15)
  vFrame2.GetXaxis().SetTitleOffset(0.90)
  vFrame2.GetXaxis().SetLabelSize(0.12)

  hist_fit_residual_vsMass[0].GetXaxis().SetNdivisions(405)
  hist_fit_residual_vsMass[0].SetLineColor( kBlack)
  hist_fit_residual_vsMass[0].SetMarkerColor(kBlack)
  hist_fit_residual_vsMass[0].SetMarkerStyle(20)
  hist_fit_residual_vsMass[0].SetMarkerSize(1.)
  hist_fit_residual_vsMass[0].Draw("same")
  line = TLine(fFitXmin,0,fFitXmax,0)
  line.Draw("same")
  p11_2.RedrawAxis()
  line2=TLine()
  line2.DrawLine(p11_2.GetUxmin(), p11_2.GetUymax(), p11_2.GetUxmax(), p11_2.GetUymax())
  line2.DrawLine(p11_2.GetUxmax(), p11_2.GetUymin(), p11_2.GetUxmax(), p11_2.GetUymax())


  cname = fOutputFile+"_fit.pdf"
  c1.SaveAs(cname)
  # time.sleep(100)
  # del c1
# ---------------------------------------------------------------------------------------------------------------------------    
def FitComparisons(hMassNEW,g,M1Bkg,hist_fit_residual_vsMass,FunctionType,nPar,fFitXmin,fFitXmax,fLabel,fOutputFile,chi2,dof,doSigmaBand,histoCI):
  
  H_ref = 600; 
  W_ref = 800; 
  W = W_ref
  H  = H_ref
  
  T = 0.08*H_ref
  B = 0.12*H_ref 
  L = 0.12*W_ref
  R = 0.04*W_ref

  c2 = TCanvas("c2","c2",50,50,W,H)
  c2.SetFillColor(0)
  c2.SetBorderMode(0)
  c2.SetFrameFillStyle(0)
  c2.SetFrameBorderMode(0)
  c2.SetLeftMargin( L/W )
  c2.SetRightMargin( R/W )
  c2.SetTopMargin( T/H )
  c2.SetBottomMargin( B/H )
  c2.SetTickx(0)
  c2.SetTicky(0)
  c2.GetWindowHeight()
  c2.GetWindowWidth()
  c2.SetLogy()
  c2.Divide(1,2,0,0,0)

  #------------ pad 1  ----------------
  c2.cd(1)
  p11_1 = c2.GetPad(1)
  p11_1.SetPad(0.01,0.25,0.99,0.98)
  p11_1.SetLogy()
  p11_1.SetLeftMargin( L/W )
  p11_1.SetRightMargin( R/W )
  p11_1.SetTopMargin( T/H )
  p11_1.SetBottomMargin(0.0015)
  p11_1.SetTickx(0)
  p11_1.SetTicky(0)
 
  #Pave text

  addInfo = TPaveText(0.1397805,0.01676406,0.4371859,0.2227225,"NDC")
  addInfo.AddText(fLabel)
  addInfo.AddText("|#eta| #leq 2.5, p_{T} > 200 GeV")
  addInfo.AddText("M_{jj} > 1050 GeV, |#Delta#eta_{jj}| #leq 1.3")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  # addInfo.SetTextFont(42)
  # addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  
  vFrame = p11_1.DrawFrame(fFitXmin,0.0005,fFitXmax,hMassNEW.GetMaximum()*20.0)  
  vFrame.SetTitle("")
  vFrame.SetXTitle("Dijet invariant mass (GeV)")
  vFrame.SetYTitle("#frac{dN}{dm_{jj}} (GeV^{-1})")
  # vFrame.GetXaxis().SetTitleSize(0.06)
#   vFrame.GetXaxis().SetTitleOffset(0.95)
#   vFrame.GetXaxis().SetLabelSize(0.05)
#   vFrame.GetYaxis().SetTitleSize(0.06)
  vFrame.GetYaxis().SetTitleOffset(0.76)
#   vFrame.GetYaxis().SetLabelSize(0.05)

  g.SetMarkerSize(0.9)
  g.SetMarkerStyle(20)
  g.Draw("pe0 same")
  if (doSigmaBand): histoCI[1].Draw("same3")
  g.Draw("pe0 same")

  linestyles = [1,2,7,3,3]
  markerstyles = [20,22,32,25,32]
  i =0
  for f in M1Bkg:
    f.SetLineWidth(2)
    f.SetLineStyle(linestyles[i])
    f.SetLineColor(col.GetColor(palette[i]))
    f.SetMarkerStyle(markerstyles[i])
    f.SetMarkerColor(col.GetColor(palette[i]))
    f.Draw("same")
    i+=1

  legend = TLegend(0.5512768,0.4885525,0.7217721,0.907654)
  if (doSigmaBand): legend = TLegend(0.5512768,0.4885525,0.7217721,0.907654)
  legend.SetTextSize(0.045)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  legend.AddEntry(g, legend_text,"lpe")
  if (doSigmaBand): 
    legend.AddEntry(M1Bkg[0], "2 par.   (#chi^{2}/ndof = %.2f/%i)"%(chi2[0],dof[0]),"lp")
    legend.AddEntry(histoCI[1], " #pm 1 #sigma (3 par. default fit)","f")
    legend.AddEntry(M1Bkg[1], "3 par.   (#chi^{2}/ndof = %.2f/%i)"%(chi2[1],dof[1]),"lp")
    
    legend.AddEntry(M1Bkg[2], "4 par.   (#chi^{2}/ndof = %.2f/%i)"%(chi2[2],dof[2]),"lp")
    # legend.AddEntry(M1Bkg[3], "5 par.   (#chi^{2}/ndof = %.2f/%i)"%(chi2[3],dof[3]),"l")
    legend.AddEntry(M1Bkg[3], "Alt. , 4 par. (#chi^{2}/ndof = %.2f/%i)"%(chi2[3],dof[3]),"lp")
  elif (not doSigmaBand): 
    legend.AddEntry(M1Bkg[0], "2 par.   (#chi^{2}/ndof = %.2f/%i)"%(chi2[0],dof[0]),"lp")
    legend.AddEntry(M1Bkg[1], "3 par.   (#chi^{2}/ndof = %.2f/%i)"%(chi2[1],dof[1]),"lp")
    legend.AddEntry(M1Bkg[2], "4 par.   (#chi^{2}/ndof = %.2f/%i)"%(chi2[2],dof[2]),"lp")
#   legend.AddEntry(M1Bkg[3], "5 par.   (#chi^{2}/ndof = %.2f/%i)"%(chi2[3],dof[3]),"l")
    legend.AddEntry(M1Bkg[3], "Alt. , 4 par. (#chi^{2}/ndof = %.2f/%i)"%(chi2[3],dof[3]),"lp")
  legend.Draw("same")
  addInfo.Draw("same")
  p11_1.RedrawAxis()
  p11_1.Update()
  p11_1.GetFrame().Draw()
  CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)
  
  c2.cd(2)
  p11_2 = c2.GetPad(2)
  p11_2.SetPad(0.01,0.02,0.99,0.25)
  p11_2.SetFillColor(0)
  p11_2.SetBorderMode(0)
  p11_2.SetFrameFillStyle(0)
  p11_2.SetFrameBorderMode(0)
  p11_2.SetLeftMargin( L/W )
  p11_2.SetRightMargin( R/W )
  p11_2.SetBottomMargin( B/H*2.5 )
  # p11_2.SetTopMargin( B/H*2.5 )
  p11_2.SetGridx()
  p11_2.SetGridy()
  vFrame2 = p11_2.DrawFrame(fFitXmin, -3.3, fFitXmax, 3.3)
  vFrame2.SetTitle("")
  vFrame2.SetXTitle("Dijet invariant mass (GeV)")
  vFrame2.GetXaxis().SetTitleSize(0.06)
  vFrame2.SetYTitle("#frac{Data-Fit}{#sigma}")
  vFrame2.GetYaxis().SetTitleSize(0.16)
  vFrame2.GetYaxis().SetTitleOffset(0.22)
  vFrame2.GetYaxis().SetLabelSize(0.10)
  vFrame2.GetXaxis().SetTitleSize(0.17)
 #  vFrame2.GetXaxis().SetTitleOffset(0.90)
  vFrame2.GetXaxis().SetLabelSize(0.14)
  vFrame2.GetYaxis().CenterTitle()
  vFrame2.GetXaxis().SetNdivisions(506)
  vFrame2.GetYaxis().SetNdivisions(104)
  
  
  i =0
  for h in hist_fit_residual_vsMass:   
    h.SetLineColor((col.GetColor(palette[i])))
    h.SetMarkerColor((col.GetColor(palette[i])))
    h.SetMarkerStyle(markerstyles[i])
    h.SetMarkerSize(1.)
    h.Draw("same")
    i+=1
  line = TLine(fFitXmin,0,fFitXmax,0)
  line.Draw("same")
  p11_2.RedrawAxis()
  
  line2=TLine()
  line2.DrawLine(p11_2.GetUxmin(), p11_2.GetUymax(), p11_2.GetUxmax(), p11_2.GetUymax())
  line2.DrawLine(p11_2.GetUxmax(), p11_2.GetUymin(), p11_2.GetUxmax(), p11_2.GetUymax())
  c2.cd(1)
  p11_1.RedrawAxis()
  
  cname = fOutputFile+suffix+".pdf"
  c2.SaveAs(cname)
  c2.SaveAs(cname.replace("pdf","root"),"root")
  c2.SaveAs(cname.replace("pdf","C"),"C")
  time.sleep(10)

 
# ---------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
  outdir = '/mnt/t3nfs01/data01/shome/dschafer/AnalysisOutput/figures/bkgfit/ReReco2016/'
  #orig_stdout = sys.stdout
  #f = file(outdir+"Sideband-fits-Ftest2.txt", 'w')
  #sys.stdout = f


  massBins =[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, #change bin 944 to 955!! and 1058 to 1055
             1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 
             4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808]
  
  channels = ["WW",'WZ','ZZ']
  #channels = ['WW']
  fitmax = 7000
  # file for data sideband: Data_VV_qV_SB_Run2016All.root
  # file for QCD pythia 8: QCD_pythia8_VV.root
  
  #infile = "../../ExoDiBosonAnalysis/results/Data_VVdijet_test40GeV_SB.root"
  infile = "/shome/dschafer/ExoDiBosonAnalysis/results/ReRecoData_VVdijet.root"
  
  for ch in channels:
    #performFit("input/JetHT_VV.root", "DijetMassHighPuri%s"%ch, len(massBins)-1, massBins, 955, fitmax, "%s category, HP"%ch, "ftest_2016/%sHP"%ch, doSigmaBand = False)
    #performFit("input/JetHT_VV.root", "DijetMassLowPuri%s"%ch , len(massBins)-1, massBins, 955, fitmax, "%s category, LP"%ch, "ftest_2016/%sLP"%ch, doSigmaBand = False)
    performFit(infile, "DijetMassHighPuri%s"%ch , len(massBins)-1, massBins, 1118, fitmax, "%s category, HP"%ch, "%s/%sHP"%(outdir,ch), doSigmaBand = False)
    performFit(infile, "DijetMassLowPuri%s"%ch , len(massBins)-1, massBins, 1118, fitmax, "%s category, LP"%ch, "%s/%sLP"%(outdir,ch), doSigmaBand = False)
    
  # sys.stdout = orig_stdout

 
 
