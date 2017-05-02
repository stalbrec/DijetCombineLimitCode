import ROOT as rt
from ROOT import *
import os
import sys
from array import *
import time

import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()
rt.gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4


# define the plot canvas
def setStyle(c,histo):
    # canvas style
    rt.gStyle.SetOptStat(0)
    rt.gStyle.SetOptTitle(0)        
    
    c.SetTickx(1)
    c.SetTicky(1)
    
    # c.SetRightMargin(0.14)
    # c.SetTopMargin(0.14)
    # c.SetLeftMargin(0.14)
    # c.SetBottomMargin(0.14)
  
    histo.GetXaxis().SetTitleSize(0.05)
    histo.GetXaxis().SetTitleOffset(1.2)

    histo.GetYaxis().SetLabelSize(0.04)
    histo.GetYaxis().SetTitleSize(0.05)
    histo.GetYaxis().SetTitleOffset(1.05)
    # histo.GetYaxis().CenterTitle(True)

def PlotPValue(filePVALNAME, label):

    filePVAL = open(filePVALNAME)
    pvalPairs = eval(filePVAL.readline())

    mass = []
    pval = []

    for entry in pvalPairs:
        mass.append(entry[0]/1000.)
        pval.append(entry[1])

    pvalGraph = rt.TGraph(len(mass), array('d',mass), array('d',pval))
    pvalGraph.GetXaxis().SetLimits(1.1,4.1)
    if filePVALNAME.find("q")!=-1:
         pvalGraph.GetXaxis().SetLimits(1.1,6.0)
    
    c1 =rt.TCanvas("c1","",630,600)
    c1.SetLogy()
    pvalGraph.Draw("AL")
    htemp = pvalGraph.GetHistogram()
    c1.SetLogy()
    setStyle(c1,htemp)
    htemp.GetXaxis().SetTitle("Resonance Mass (TeV)")
    htemp.GetYaxis().SetTitle("p-value")
    pvalGraph.SetLineColor(rt.kBlack)
    pvalGraph.SetLineWidth(2)
    htemp.SetMinimum(1E-5)
    htemp.SetMaximum(1)
    pvalGraph.GetXaxis().SetNdivisions(508)

    # sigmas
    sigmas = [0.8413447,0.9772499,0.9986501,0.9999683,0.9999997]
    line = rt.TLine()
    line.SetLineColor(2)
    for sigma in sigmas:
        line.DrawLine(htemp.GetXaxis().GetXmin(), 1-sigma,htemp.GetXaxis().GetXmax(), 1-sigma)
        line.Draw("SAME")
        pvalGraph.Draw("LSAME")
    text = []
    for i in range(1,6):
        text.append(rt.TLatex(htemp.GetXaxis().GetXmax()*0.92, (1-sigmas[i-1])*1.10,"%i #sigma" %i))
        #text = rt.TLatex(1800.,0.001,"%i #sigma" %i)
        #text.SetNDC()
        #text.SetTextFont(42)
        #text.SetTextSize(0.038)
        text[i-1].SetTextColor(2)
        text[i-1].Draw("SAME")
        
        
    addInfo = rt.TPaveText(0.1879195,0.2272727,0.4563758,0.3339161,"NDC")
    addInfo.SetFillColor(0)
    addInfo.SetLineColor(0)
    addInfo.SetFillStyle(0)
    addInfo.SetBorderSize(0)
    addInfo.SetTextFont(42)
    addInfo.SetTextSize(0.040)
    addInfo.SetTextAlign(12)
    signal=""
    if label.find("BulkWW")!=-1:
           signal="G_{bulk} #rightarrow WW"
    if label.find("BulkZZ")!=-1:
           signal="G_{bulk} #rightarrow ZZ"
    if label.find("Zprime")!=-1:
           signal="Z' #rightarrow WW"
    if label.find("WZ")!=-1:
           signal="W' #rightarrow WZ"
    if label.find("qW")!=-1:
           signal="q* #rightarrow qW"
    if label.find("qZ")!=-1:
           signal="q* #rightarrow qZ"
    
    addInfo.AddText(signal)
    if(label.find("WW_high_purity")!=-1):addInfo.AddText("WW enriched")
    if(label.find("WZ_high_purity")!=-1):addInfo.AddText("WZ enriched")
    if(label.find("ZZ_high_purity")!=-1):addInfo.AddText("ZZ enriched")
    if(label.find("VVnew_high_purity")!=-1):addInfo.AddText("WW+WZ+ZZ combined")
    if(label.find("VVold_high_purity")!=-1):addInfo.AddText("VV enriched")
    if(label.find("WW_low_purity")!=-1):addInfo.AddText("WW enriched")
    if(label.find("WZ_low_purity")!=-1):addInfo.AddText("WZ enriched")
    if(label.find("ZZ_low_purity")!=-1):addInfo.AddText("ZZ enriched")
    if(label.find("VVnew_low_purity")!=-1):addInfo.AddText("WW+WZ+ZZ combined")
    if(label.find("VVold_low_purity")!=-1):addInfo.AddText("VV category")
    if(label.find("_combined_old")!=-1):addInfo.AddText("VV category")
    if(label.find("_combined_new")!=-1):addInfo.AddText("WW+WZ+ZZ categories")
    if(label.find("low_purity")!=-1):addInfo.AddText("Low-purity")
    if(label.find("high_purity")!=-1):addInfo.AddText("High-purity")
    addInfo.Draw()
    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
    c1.Update()
    
    c1.Update()
    c1.SaveAs("pValues/pvalue_%s_wPDF.pdf" %label)
    time.sleep(10)

def PlotMu(muFILENAME, label):
    
    fileMU = open(muFILENAME)
    muPairs = eval(fileMU.readline())

    mass = []
    mu = []
    muplus = []
    muminus = []
    for entry in muPairs:
        mass.append(entry[0]/1000.)
        mu.append(entry[1])
        muminus.append(entry[2]+entry[1])
        muplus.append(entry[3]+entry[1])
        if entry[1]<-150:
	    mu[-1]=-150
	    muminus[-1]=-150
	    if muplus[-1]<-150:
	       muplus[-1]=150
        if entry[1]>150:
	    mu[-1]=150
	    muplus[-1]=150
	    if muminus[-1]>150:
	       muminus[-1]=-150

    #nominal
    muGraph = rt.TGraph(len(mass), array('d',mass), array('d',mu))

    # green band
    muBAND = []
    massBAND = []
    for i in range(0, len(mass)):
        muBAND.append(muplus[i])
        massBAND.append(mass[i])
    for i in range(1, len(mass)+1):
        muBAND.append(muminus[len(mass)-i])
        massBAND.append(mass[len(mass)-i])

    print massBAND
    print muBAND

    muGraphBAND = rt.TGraph(len(massBAND), array('d',massBAND), array('d',muBAND))
    c1 = rt.TCanvas("c1","c1", 630, 600)
    muGraphBAND.SetFillStyle(1001)
    muGraphBAND.SetFillColor(rt.kGreen)
    muGraphBAND.Draw("AF")
    htemp = muGraphBAND.GetHistogram()
    setStyle(c1,htemp)
    htemp.GetXaxis().SetTitle("Resonance mass (TeV)")
    htemp.GetYaxis().SetTitle("Best-fit #sigma #times BR(X #rightarrow "+label.split("_")[0].replace("RS1","").replace("Bulk","")+") (pb)")
    htemp.SetMinimum(-150)
    htemp.SetMaximum(150)
    muGraph.Draw("PLSAME")
    l=rt.TLine(1000,0,2300,0)
    l.SetLineColor(2)
    l.Draw("same")

    PlotPValue(combinedplots_old,chan+"_combined_old")
    PlotPValue(combinedplots_new,chan+"_combined_new")
    

    c1.Update()
    c1.SaveAs("mu_%s.pdf" %label)
    time.sleep(100)

if __name__ == '__main__':

  channels=["ZprimeWW","WZ","qW","qZ","BulkWW","BulkZZ"]
  #channels=["BulkZZ","WZ","ZprimeWW"]
  #channels=["WZ","BulkWW","BulkZZ"]
  #channels=["qW","qZ"]

  for chan in channels:
      
    print "chan =",chan
    if "q" in chan:
       cat="qV"
    else:
       cat="VV"
    
    qWHPplots="CMS_jj_"+chan+"_13TeV_CMS_jj_qWHP_pvalue.txt"
    qWLPplots="CMS_jj_"+chan+"_13TeV_CMS_jj_qWLP_pvalue.txt"
    
    qZHPplots="CMS_jj_"+chan+"_13TeV_CMS_jj_qZHP_pvalue.txt"
    qZLPplots="CMS_jj_"+chan+"_13TeV_CMS_jj_qZLP_pvalue.txt"
    
    
    WWHPplots="CMS_jj_"+chan+"_13TeV_CMS_jj_WWHP_pvalue.txt"
    WWLPplots="CMS_jj_"+chan+"_13TeV_CMS_jj_WWLP_pvalue.txt"
    
    WZHPplots="CMS_jj_"+chan+"_13TeV_CMS_jj_WZHP_pvalue.txt"
    WZLPplots="CMS_jj_"+chan+"_13TeV_CMS_jj_WZLP_pvalue.txt"
    
    ZZHPplots="CMS_jj_"+chan+"_13TeV_CMS_jj_ZZHP_pvalue.txt"
    ZZLPplots="CMS_jj_"+chan+"_13TeV_CMS_jj_ZZLP_pvalue.txt"
    
    combinedplots_old="CMS_jj_"+chan+"_13TeV_CMS_jj_VV_pvalue.txt"
    combinedplots_new="CMS_jj_"+chan+"_13TeV_CMS_jj_"+cat+"new_pvalue.txt"
    
    # HPnewplots="CMS_jj_"+chan+"_13TeV_CMS_jj_VVHPnew_pvalue.txt"
    # HPoldplots="CMS_jj_"+chan+"_13TeV_CMS_jj_VVHP_pvalue.txt"
    # LPnewplots="CMS_jj_"+chan+"_13TeV_CMS_jj_VVLPnew_pvalue.txt"
    # LPoldplots="CMS_jj_"+chan+"_13TeV_CMS_jj_VVLP_pvalue.txt"

    #PlotPValue(WWHPplots,chan+"inWW_high_purity")
    #PlotPValue(WWLPplots,chan+"inWW_low_purity")

    #PlotPValue(WZHPplots,chan+"inWZ_high_purity")
    #PlotPValue(WZLPplots,chan+"inWZ_low_purity")

    #PlotPValue(ZZHPplots,chan+"inZZ_high_purity")
    #PlotPValue(ZZLPplots,chan+"inZZ_low_purity")
    
    #PlotPValue(qZHPplots,chan+"inqZ_high_purity")
    #PlotPValue(qZLPplots,chan+"inqZ_low_purity")
    
    #PlotPValue(qWHPplots,chan+"inqW_high_purity")
    #PlotPValue(qWLPplots,chan+"inqW_low_purity")

    #PlotPValue(HPnewplots,chan+"inVVnew_high_purity")
    #PlotPValue(LPnewplots,chan+"inVVnew_low_purity")
    # PlotPValue(HPoldplots,chan+"inVVold_high_purity")
    # PlotPValue(LPoldplots,chan+"inVVold_low_purity")

    #PlotPValue(combinedplots_old,chan+"in_combined_old")
    PlotPValue(combinedplots_new,chan+"in_combined_new")
