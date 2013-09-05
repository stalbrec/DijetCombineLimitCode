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

channels=["HHcounting"]

for chan in channels:

    masses =[1000.0, 1500.0, 2000.0]

    for mass in masses:
        print "mass = ",mass

        bin0="ch0=datacards/Xvv.mX"+str(mass)+"_" + chan + "_8TeV_channel0.txt "
        bin1="ch1=datacards/Xvv.mX"+str(mass)+"_" + chan + "_8TeV_channel1.txt "
        
        bin01="datacards/Xvv.mX"+str(mass)+"_" + chan + "_8TeV_channel01.txt "

        comb01 = "combineCards.py " + bin0 + bin1 + " >" + bin01

        print comb01
        os.system( comb01  )