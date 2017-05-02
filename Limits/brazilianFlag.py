import ROOT as rt
import time
import CMS_lumi, tdrstyle
from ROOT import TChain, TTree, kWhite
import os
import glob
import math
from math import exp, log
import array
import sys
import time
import random


tdrstyle.setTDRStyle()
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4
#rt.gROOT.ProcessLine("struct limit_t {Double_t limit;};")

def Plot(files, label, obs, postfix = "."):


    radmasses = []
    for f in files:
      if not postfix:
        radmasses.append(float(f.replace("CMS_jj_","").split("_")[0])/1000.)
      else:
        stmp = f.replace("CMS_jj_","").split("_")[0]
        print stmp
        stmp2 = stmp.split("/")[1]
        print stmp2
        radmasses.append(float(stmp2)/1000.)
    #print radmasses

    efficiencies={}
    for mass in radmasses:
      efficiencies[mass]=0.01# assume 10/fb signal cross section #FOR Wprime=
      if "WZ" in label.split("_")[0]:
        print "Taking care of WZ hadronic branching fractions for exclusive samples: 0.6991*0.6760!"
        efficiencies[mass]=0.01/((0.6991*0.6760)) #assume 10/fb signal and get rid of hadronic branching fraction)

      elif "BulkWW" in label.split("_")[0] or "Zprime" in label.split("_")[0]:
        print "Taking care of WW hadronic branching fractions for inclusive samples: 1.!"
        efficiencies[mass]=0.01

      elif "BulkZZ" in label.split("_")[0]:
        print "Taking care of ZZ hadronic branching fractions for exclusive samples: 0.0.6991*0.0.6991!"
        efficiencies[mass]=0.01/((0.6991*0.6991))

      elif "qZ" in label.split("_")[0]:
        print "Taking care of qZ hadronic branching fractions for inclusive samples: 1.!"
        efficiencies[mass]=0.01

      elif "qW" in label.split("_")[0]:
        print "Taking care of qW hadronic branching fractions for inclusive samples: 1.!"
        efficiencies[mass]=0.01


    # fChain = []
    rad = []
    for onefile in files:
        print "using file " + onefile
        # if onefile.find("2500")!=-1 or onefile.find("2500")!=-1: continue
        # fileIN = rt.TFile.Open(onefile)
        # fChain.append(fileIN.Get("limit;1"))
        # print fChain

        # rt.gROOT.ProcessLine("struct limit_t {Double_t limit;};")
        # from ROOT import limit_t
        # limit_branch = limit_t()
        #
        # for j in range(0,len(fChain)):
        #     chain = fChain[j]
        #     print chain
        #     chain.SetBranchAddress("limit", rt.AddressOf(limit_branch,'limit'))
        file = rt.TFile(onefile)
        tree = file.Get("limit")
        limits = []
        for quantile in tree:
            limits.append(tree.limit)
            print ">>>   %.2f" % limits[-1]

        rad.append(limits[:6])

    # for j in range(0,len(fChain)):
    #     chain = fChain[j]
    #     thisrad = []
    #     for  i in range(0,6):
    #       chain.GetTree().GetEntry(i)
    #       thisrad.append(limit_branch.limit)
    #     rad.append(thisrad)


    # we do a plot r*MR
    mg = rt.TMultiGraph()
    mg.SetTitle("X -> ZZ")
    x = []
    yobs = []
    y2up = []
    y1up = []
    y1down = []
    y2down = []
    ymean = []

    print "efficiencies"
    print efficiencies
    print "radmasses"
    print radmasses
    print "rad"
    print rad
    
    print len(files)
    print len(radmasses)
    print len(efficiencies)
    print len(rad)
    for i in range(0,len(files)):
        # print "y2up   = " ,rad[i][0]
    #     print "y1up   = " ,rad[i][1]
    #     print "ymean  = " ,rad[i][2]
    #     print "y1down = " ,rad[i][3]
    #     print "y2down = " ,rad[i][4]
    #     print "yobs   = " ,rad[i][5]
    #
        print rad[i][0], radmasses[i], efficiencies[radmasses[i]]
        y2up.append(rad[i][0]*efficiencies[radmasses[i]])
        y1up.append(rad[i][1]*efficiencies[radmasses[i]])
        ymean.append(rad[i][2]*efficiencies[radmasses[i]])
        y1down.append(rad[i][3]*efficiencies[radmasses[i]])
        y2down.append(rad[i][4]*efficiencies[radmasses[i]])
        yobs.append(rad[i][5]*efficiencies[radmasses[i]])
        # print "Yobs (before adding sigma) = %f"%rad[i][5]

    grobs = rt.TGraphErrors(1)
    grobs.SetMarkerStyle(8)
    grobs.SetMarkerSize(0.8)
    grobs.SetLineColor(rt.kBlack)
    grobs.SetLineWidth(2)
    gr2up = rt.TGraphErrors(1)
    gr2up.SetMarkerColor(0)
    gr1up = rt.TGraphErrors(1)
    gr1up.SetMarkerColor(0)
    grmean = rt.TGraphErrors(1)
    grmean.SetLineColor(1)
    grmean.SetLineWidth(2)
    grmean.SetLineStyle(3)
    gr1down = rt.TGraphErrors(1)
    gr1down.SetMarkerColor(0)
    gr2down = rt.TGraphErrors(1)
    gr2down.SetMarkerColor(0)

    for j in range(0,len(files)):
        grobs.SetPoint(j, radmasses[j], yobs[j])
        gr2up.SetPoint(j, radmasses[j], y2up[j])
        gr1up.SetPoint(j, radmasses[j], y1up[j])
        grmean.SetPoint(j, radmasses[j], ymean[j])
        gr1down.SetPoint(j, radmasses[j], y1down[j])
        gr2down.SetPoint(j, radmasses[j], y2down[j])
        # print "------------"
        # print label.split("_")[0]
        # print " observed %f %f" %(radmasses[j],yobs[j])

    mg.Add(gr2up)#.Draw("same")
    mg.Add(gr1up)#.Draw("same")
    mg.Add(grmean,"L")#.Draw("same,AC*")
    mg.Add(gr1down)#.Draw("same,AC*")
    mg.Add(gr2down)#.Draw("same,AC*")
    # if obs: mg.Add(grobs,"L")#.Draw("AC*")


    H_ref = 600;
    W_ref = 800;
    W = W_ref
    H  = H_ref

    T = 0.08*H_ref
    B = 0.12*H_ref
    L = 0.12*W_ref
    R = 0.04*W_ref

    c1 = rt.TCanvas("c1","c1",50,50,W,H)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( L/W )
    c1.SetRightMargin( R/W )
    c1.SetTopMargin( T/H )
    c1.SetBottomMargin( B/H )
    c1.SetTickx(0)
    c1.SetTicky(0)
    c1.GetWindowHeight()
    c1.GetWindowWidth()
    c1.SetLogy()
    c1.SetGrid()
    c1.SetLogy()
    c1.cd()

    frame = c1.DrawFrame(1.1,0.001, 4.2, 10)
    if "qZ" in label.split("_")[0] or label.find("qW")!=-1: frame = c1.DrawFrame(1.1,0.001, 6.2, 800.)
    frame.GetYaxis().CenterTitle()
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetTitleOffset(1.15)
    frame.GetXaxis().SetTitleOffset(1.05)
    frame.GetXaxis().CenterTitle()
    frame.SetMinimum(0.001)
    frame.SetMaximum(50)
    if "WZ" in label.split("_")[0] and ( label.find("_WZ")!=-1 or label.find("_VV")!=-1):
      frame.SetMinimum(0.0001)
      frame.SetMaximum(9)
    if label.find("_new_combined")!=-1:
      frame.SetMinimum(0.0001)
      frame.SetMaximum(109.)
    if (label.find("new")!=-1) and label.find("qW")!=-1 or label.find("qZ")!=-1:
      frame.SetMinimum(0.0002)
      frame.SetMaximum(300.)
    frame.GetXaxis().SetNdivisions(508)
    frame.GetYaxis().CenterTitle(True)

  # mg.SetTitle("")
    # mg.Draw("P")
 #
 #    mg.GetYaxis().SetTitleSize(0.05)
 #    mg.GetXaxis().SetTitleSize(0.05)
 #    mg.GetYaxis().SetTitleOffset(1.15)
 #    mg.GetYaxis().SetLabelSize(0.04)
 #    mg.GetXaxis().SetLabelSize(0.04)
 #    mg.SetMinimum(0.001)
 #    mg.SetMaximum(10)
 #    mg.GetXaxis().SetNdivisions(508)


    # mg.GetXaxis().CenterTitle(True)

    if "qW" in label.split("_")[0] or "qZ" in label.split("_")[0]:
        resonance="q*"
        frame.GetXaxis().SetTitle("M_{q*} (TeV)")
    if "RS1" in label.split("_")[0]:
        resonance="G_{RS}"
    if "Bulk" in label.split("_")[0]:
        frame.GetXaxis().SetTitle("M_{G_{Bulk}} (TeV)")
        resonance="G_{Bulk}"
    if "WZ" in label.split("_")[0]:
        resonance="W'"
        frame.GetXaxis().SetTitle("M_{W'} (TeV)")
    if "ZprimeWW" in label.split("_")[0]:
        resonance="Z'"
        frame.GetXaxis().SetTitle("M_{Z'} (TeV)")
    frame.GetYaxis().SetTitle("#sigma_{95%} #times BR("+resonance+" #rightarrow "+label.split("_")[0].replace("RS1","").replace("Bulk","").replace("Zprime","")+") [pb]")



    if(label.find("q")!=-1):
        mg.GetXaxis().SetLimits(1.2,6.2)
    elif "BulkZZ" in label.split("_")[0]:
        mg.GetXaxis().SetLimits(1.1,4.0)
    else:
        mg.GetXaxis().SetLimits(1.1,4.2)


    # histo to shade
    n=len(files)

    grgreen = rt.TGraph(2*n)
    for i in range(0,n):
        grgreen.SetPoint(i,radmasses[i],y2up[i])
        grgreen.SetPoint(n+i,radmasses[n-i-1],y2down[n-i-1])

    grgreen.SetFillColor(rt.kOrange)
    grgreen.SetLineColor(rt.kOrange)
    grgreen.SetFillStyle(1001)
    grgreen.Draw("F")


    gryellow = rt.TGraph(2*n)
    for i in range(0,n):
        gryellow.SetPoint(i,radmasses[i],y1up[i])
        gryellow.SetPoint(n+i,radmasses[n-i-1],y1down[n-i-1])

    gryellow.SetFillColor(rt.kGreen+1)
    gryellow.SetLineColor(rt.kGreen+1)
    gryellow.SetFillStyle(1001)
    gryellow.Draw("Fsame")

    grmean.Draw("L")
    if obs: grobs.Draw("LPsame")

    gtheory = rt.TGraphErrors(1)
    gtheory.SetLineColor(rt.kRed)
    gtheory.SetLineWidth(3)
    
    
    ftheory=open("signalcrosssections13TeV.txt")
    j=0
    glogtheory = rt.TGraphErrors(1)
    for lines in ftheory.readlines():
     for line in lines.split("\r"):
       if label.split("_")[0] in line:
        split=line.split(":")
        # print split[1]
        # print split[0][-4:]
        gtheory.SetPoint(j, float(split[0][-4:])/1000., float(split[1]))
        glogtheory.SetPoint(j, float(split[0][-4:])/1000., log(float(split[1])))
        j+=1

    mg.Add(gtheory,"L")
    gtheory.Draw("L")
    if "qZ" in label.split("_")[0]:
      ltheory="#sigma_{TH}#timesBR(q*#rightarrowqZ)"
    if "qW" in label.split("_")[0]:
      ltheory="#sigma_{TH}#timesBR(q*#rightarrowqW)"
    if "WZ" in label.split("_")[0]:
      ltheory="#sigma_{TH}#timesBR(W'#rightarrowWZ) HVT_{B}"
    if "BulkWW" in label.split("_")[0]:
      ltheory="#sigma_{TH}#timesBR(G_{Bulk}#rightarrowWW) #tilde{k}=0.5"
    if "BulkZZ" in label.split("_")[0]:
      ltheory="#sigma_{TH}#timesBR(G_{Bulk}#rightarrowZZ) #tilde{k}=0.5"
    if "ZprimeWW" in label.split("_")[0]:
      ltheory="#sigma_{TH}#timesBR(Z'#rightarrowWW) HVT_{B}"
    crossing=0
    for mass in range(int(radmasses[0]*1000.),int(radmasses[-1]*1000.)):
        if exp(glogtheory.Eval(mass/1000.))>grmean.Eval(mass/1000.) and crossing>=0:
          # print label,"exp crossing",mass
          crossing=-1
        if exp(glogtheory.Eval(mass/1000.))<grmean.Eval(mass/1000.) and crossing<=0:
          # print label,"exp crossing",mass
          crossing=1
          crossing=0
    for mass in range(int(radmasses[0]*1000.),int(radmasses[-1]*1000.)):
        if exp(glogtheory.Eval(mass/1000.))>grobs.Eval(mass/1000.) and crossing>=0:
          # print label,"obs crossing",mass
          crossing=-1
        if exp(glogtheory.Eval(mass/1000.))<grobs.Eval(mass/1000.) and crossing<=0:
          # print label,"obs crossing",mass
          crossing=1

    # if "WW" in label.split("_")[0] or "ZZ" in label.split("_")[0]:
    #    leg = rt.TLegend(0.43,0.65,0.95,0.89)
    #    leg2 = rt.TLegend(0.43,0.65,0.95,0.89)
    # else:
    leg = rt.TLegend(0.498995,0.6602591,0.9446734,0.9011917)
    leg2 = rt.TLegend(0.498995,0.6602591,0.9446734,0.9011917)
    leg.SetTextSize(0.028)
    leg.SetLineColor(1)
    leg.SetShadowColor(0)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(kWhite)
    # leg.SetFillStyle(0)
    leg.SetMargin(0.35)
    leg2.SetTextSize(0.028)
    leg2.SetLineColor(1)
    leg2.SetShadowColor(0)
    leg2.SetLineStyle(1)
    leg2.SetLineWidth(1)
    leg2.SetFillColor(0)
    leg2.SetFillStyle(0)
    leg2.SetMargin(0.35)
    leg.SetBorderSize(1)

    if obs: leg.AddEntry(grobs, "Observed", "Lp")
    leg.AddEntry(gryellow, "Expected #pm 1 std. deviation", "f")
    leg.AddEntry(grgreen , "Expected #pm 2 std. deviation", "f")
    leg.AddEntry(gtheory, ltheory, "L")

    if obs: leg2.AddEntry(grobs, " ", "")
    leg2.AddEntry(grmean, " ", "L")
    leg2.AddEntry(grmean, " ", "L")
    leg2.AddEntry(gtheory, " ", "")




    # addInfo = rt.TPaveText(0.548995,0.1830769,0.9346734,0.2897203,"NDC")
    addInfo = rt.TPaveText(0.6946309,0.5437063,0.795302,0.6363636,"NDC")
    if (label.find("new")!=-1) and label.find("qW")!=-1 or label.find("qZ")!=-1:addInfo = rt.TPaveText(0.7846309,0.5437063,0.825302,0.6363636,"NDC")
    addInfo.SetFillColor(0)
    addInfo.SetLineColor(0)
    addInfo.SetFillStyle(0)
    addInfo.SetBorderSize(0)
    addInfo.SetTextFont(42)
    addInfo.SetTextSize(0.040)
    addInfo.SetTextAlign(12)


    # addInfo.AddText("Pruned mass sideband")
    if(label.find("HP")!=-1):
      if(label.find("_WW")!=-1):addInfo.AddText("WW enriched")
      elif(label.find("_WZ")!=-1):addInfo.AddText("WZ enriched")
      elif(label.find("_ZZ")!=-1):addInfo.AddText("ZZ enriched")
      elif(label.find("_VV_new")!=-1):addInfo.AddText("WW+WZ+ZZ")
      elif(label.find("_VVHP_new")!=-1):addInfo.AddText("WW+WZ+ZZ")
      elif(label.find("_VV_old")!=-1):addInfo.AddText("VV category")
      elif(label.find("_qW")!=-1):addInfo.AddText("qW enriched")
      elif(label.find("_qZ")!=-1):addInfo.AddText("qZ enriched")
      elif(label.find("_qV")!=-1):addInfo.AddText("qW+qZ")
      addInfo.AddText("High-purity")
    elif(label.find("LP")!=-1):
      if(label.find("_WW")!=-1):addInfo.AddText("WW enriched")
      elif(label.find("_WZ")!=-1):addInfo.AddText("WZ enriched")
      elif(label.find("_ZZ")!=-1):addInfo.AddText("ZZ enriched")
      elif(label.find("_VV_new")!=-1):addInfo.AddText("WW+WZ+ZZ")
      elif(label.find("_VVLP_new")!=-1):addInfo.AddText("WW+WZ+ZZ")
      elif(label.find("_VV_old")!=-1):addInfo.AddText("VV category")

      elif(label.find("_qW")!=-1):addInfo.AddText("qW enriched")
      elif(label.find("_qZ")!=-1):addInfo.AddText("qZ enriched")
      elif(label.find("_qV")!=-1):addInfo.AddText("qW+qZ")
      addInfo.AddText("Low-purity")
    else:
      if label.find("old")!=-1:
        addInfo.AddText("VV category")
        addInfo.AddText("HP+LP")
      elif (label.find("new")!=-1) and label.find("qW")!=-1 or label.find("qZ")!=-1:
        addInfo.AddText("qW+qZ")
        addInfo.AddText("HP+LP")

      elif label.find("new_combined")!=-1:
        addInfo.AddText("WW+WZ+ZZ")
        addInfo.AddText("HP+LP")

    addInfo.Draw()
    c1.Update()
    frame = c1.GetFrame()
    frame.Draw()
    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
    c1.cd()
    c1.Update()
    c1.RedrawAxis()
    c1.RedrawAxis("g")
    c1.cd()
    c1.Update()

    c1.cd()
    c1.Update()

    leg.Draw()
    leg2.Draw("same")

    fname = "%s/brazilianFlag_%s_13TeV.pdf" %(postfix, label)
    c1.SaveAs(fname)
    c1.SaveAs(fname.replace(".pdf" ,".C"  ))

    # del c1
 #    del leg
 #    del leg2
 #    del addInfo
 #    del mg

    # f = rt.TFile("VVnoLP_graphs.root", "recreate")
    # gr2up  .SetName("gr2up  ")
    # gr1up  .SetName("gr1up  ")
    # grmean .SetName("grmean ")
    # gr1down.SetName("gr1down")
    # gr2down.SetName("gr2down")
    #
    # gr2up  .Write()
    # gr1up  .Write()
    # grmean .Write()
    # gr1down.Write()
    # gr2down.Write()
    # if obs:
    #   grobs.SetName("grobs")
    #   grobs.Write()
    # f.Close()


    time.sleep(5)

if __name__ == '__main__':
  postfix = "withoutPDFandScale/"

  channels=["RS1WW","RS1ZZ","WZ","qW","qZ","BulkWW","BulkZZ"]
  channels=["ZprimeWW","WZ","BulkWW","BulkZZ"]
  channels=["qW"]
  # channels=["qZ","qW"]
  for chan in channels:
    masses =[m*100 for m in range(12,43+1)]
    #masses =[1400,1800,2000,2500,3000]

    #if chan.find("BulkZZ") != -1: masses =[m*100 for m in range(14,40+1)]
    if chan.find("q") != -1: masses =[m*100 for m in range(12,60+1)]
    
    # if chan.find("qZHPplots") != -1:
    # masses =[1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000,2100 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4100, 4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900, 5000, 5100, 5200, 5300, 5400, 5500, 5600, 5700, 5800, 5900, 6000, 6100, 6200]

    HPplots=[]
    LPplots=[]
    WWHPplots=[]
    WZHPplots=[]
    ZZHPplots=[]
    WWLPplots=[]
    WZLPplots=[]
    ZZLPplots=[]
    combinedplots_old=[]
    combinedplots=[]

    qVHPplots=[]
    qVLPplots=[]
    qWHPplots=[]
    qZHPplots=[]
    qWLPplots=[]
    qZLPplots=[]
    combinedplots_qV=[]

    for mass in masses:
       if mass == 5500:
        continue
       # HPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_VVHPnew_asymptoticCLs.root"]
     #   LPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_VVLPnew_asymptoticCLs.root"]
       combinedplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_qVnew_asymptoticCLs_new.root"]
     #   combinedplots_old+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_VV_asymptoticCLs.root"]
     #   WWHPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_WWHP_asymptoticCLs.root"]
     #   WZHPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_WZHP_asymptoticCLs.root"]
     #   ZZHPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_ZZHP_asymptoticCLs.root"]
     #   WWLPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_WWLP_asymptoticCLs.root"]
     #   WZLPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_WZLP_asymptoticCLs.root"]
     #   ZZLPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_ZZLP_asymptoticCLs.root"]
     #
     #   qVHPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_qVHPnew_asymptoticCLs.root"]
     #   qVLPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_qVLPnew_asymptoticCLs.root"]
     #   qWHPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_qWHP_asymptoticCLs.root"]
     #   qZHPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_qZHP_asymptoticCLs.root"]
     #   qWLPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_qWLP_asymptoticCLs.root"]
     #   qZLPplots+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_qZLP_asymptoticCLs.root"]
       # combinedplots_qV+=[postfix+"CMS_jj_"+str(mass)+"_"+chan+"_13TeV_CMS_jj_qVnew_asymptoticCLs.root"]
     #

    # Plot(WWHPplots,chan+"_WWHP", obs=True)
#     Plot(WWLPplots,chan+"_WWLP", obs=True)
#     Plot(WZHPplots,chan+"_WZHP", obs=True)
#     Plot(WZLPplots,chan+"_WZLP", obs=True)
#     Plot(ZZHPplots,chan+"_ZZHP", obs=True)
#     Plot(ZZLPplots,chan+"_ZZLP", obs=True)
    # Plot(LPplots,chan+"_VVLP_new_combined_purity", obs=True)
    # Plot(HPplots,chan+"_VVHP_new_combined_purity", obs=True)
    Plot(combinedplots,chan+"_new_combined", True, postfix)




    # Plot(qWHPplots,chan+"_qWHP", obs=True)
    # Plot(qWLPplots,chan+"_qWLP", obs=True)
    # Plot(qZHPplots,chan+"_qZHP", obs=True)
    # Plot(qZLPplots,chan+"_qZLP", obs=True)
    # # # Plot(qVLPplots,chan+"_qVLP_new_combined_purity", obs=True)
    # # Plot(qVHPplots,chan+"_qVHP_new_combined_purity", obs=True)
    # Plot(combinedplots_qV,chan+"_new_combined", obs=True)
