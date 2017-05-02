import ROOT as rt
from array import *
import time
import CMS_lumi, tdrstyle
from heapq import nsmallest


tdrstyle.setTDRStyle()
rt.gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4

#ROOT.gSystem.Load(options.inPath+"/PDFs/HWWLVJRooPdfs_cxx.so")

rt.gStyle.SetOptFit(1)

massBins =[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 955, 1000, 1058, #944 to 955!
             1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 
             4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808]

xbins = array('d',massBins)
outdir = "/mnt/t3nfs01/data01/shome/dschafer/AnalysisOutput/figures/bkgfit/ReReco2016/"

fileIN = rt.TFile.Open("/mnt/t3nfs01/data01/shome/dschafer/ExoDiBosonAnalysis/results/ReRecoData_VVdijet.root")

alphas    = [8.34260e-01,2.26698,1.53339,1.17580,2.99999,2.2626,0.663441,0.800000]                       #WWHP,WWLP,WZHP,WZLP,ZZHP,ZZLP,VVHP (forBulkZZ),VVLP(forBulkZZ)
sigfracs  = [4.58877e-01,3.00000e-01,2.94266e-07,1.64950e-02,0.867402,0.278371,6.42551e-01,5.00000e-01]     #WWHP,WWLP,WZHP,WZLP,ZZHP,ZZLP,VVHP (forBulkZZ),VVLP(forBulkZZ)
gsigmas   = [7.27898e+01,1.06220e+02,49.3526,6.92449e+02,1.04783e+02,127.174,6.78921e+01,7.40979e+03]         #WWHP,WWLP,WZHP,WZLP,ZZHP,ZZLP,VVHP (forBulkZZ),VVLP(forBulkZZ)
means     = [2.03797e+03,2.03398e+03,2045.73,2.01137e+03,2.05889e+03,2071.45,2.02521e+03,2.00000e+03]           #WWHP,WWLP,WZHP,WZLP,ZZHP,ZZLP,VVHP (forBulkZZ),VVLP(forBulkZZ)
signs     = [1.28383e+02,2.01148e+00,32.3031,1.34384e+02,8.63245e+01,131.438,1.33056e+02,1.30000e+02]            #WWHP,WWLP,WZHP,WZLP,ZZHP,ZZLP,VVHP (forBulkZZ),VVLP(forBulkZZ)
sigmas    = [5.73275e+01,6.08280e+01,67.4016,8.25785e+01,6.54552e+01,59.7554,1.03704e+02,1.00000e+02]           #WWHP,WWLP,WZHP,WZLP,ZZHP,ZZLP,VVHP (forBulkZZ),VVLP(forBulkZZ)

# signalrate      = [1.68221,1.95172,3.38452,2.95105,1.26099,0.928928,3.00421,2.86817]#8TeV
signalrate      = [9.41966,15.6241,29.0534,34.6518,26.9728,24.441] #2016 exp expected signalrate for signal with 0.01pb xSec in each category (#WWHP,WWLP,WZHP,WZLP,ZZHP,ZZLP)
scaleToExcluded = [2.,2.,0.9,0.9,0.8,0.8]#2016 exp


# xsec=[0.01437920,0.01437920,0.029456,0.029456,0.019470,0.019470,0.019470,0.019470] #8TeV
xsec=[0.02,0.02,0.009,0.009,0.008,0.008] #2016 exp excluded xsec in combined category!
categories = ["WW, high-purity","WW, low-purity","WZ, high-purity","WZ, low-purity","ZZ, high-purity","ZZ, low-purity"]#,"VV, high-purity","VV, low-purity"]
legends=["G(2 TeV)#rightarrowWW","G(2 TeV)#rightarrowWW","W'(2 TeV)#rightarrowWZ","W'(2 TeV)#rightarrowWZ","G(2 TeV)#rightarrowZZ","G(2 TeV)#rightarrowZZ"]         
histos = ["DijetMassHighPuriWW","DijetMassLowPuriWW","DijetMassHighPuriWZ", "DijetMassLowPuriWZ", "DijetMassHighPuriZZ","DijetMassLowPuriZZ"]#,"DijetMassHighPuriVV","DijetMassLowPuriVV"]
histos = ["DijetMassLowPuriWW"]
lumi = 35867.
maxVals =[2659,2895,2895,3416,3147,3600,3416,3416]

alternative_func = "lExp"#"lExp"




#
ii = -1        
for h in histos:
    ii += 1
    # if ii !=4: continue
    title = h.replace("DijetMass","")
    print fileIN.GetName()
    print h
    htmp = fileIN.Get(h)
    
    firstbin = 1058.
    lastbin = htmp.GetBinCenter(htmp.FindLastBinAbove(0.99999))
    lower = (nsmallest(2, massBins, key=lambda x: abs(x-lastbin)))[0]
    higher  = (nsmallest(2, massBins, key=lambda x: abs(x-lastbin)))[1]
    if lower > higher:
      fFitXmax = lower
    if higher > lower:
      fFitXmax = higher
      
    print "Last non-zero bin is at x=%f. Closest dijet mass bins are L = %i  H = %i" %(lastbin,lower,higher)
    print "Using x max = %i" %lastbin
    print "Using x min = %i" %firstbin
    


    dataDistOLD = htmp.Rebin(len(xbins)-1,"hMass_rebinned",xbins)
    minVal = firstbin
    maxVal = fFitXmax


    bins = []
    for i in range(0, dataDistOLD.GetXaxis().GetNbins()):
        thisVal = dataDistOLD.GetXaxis().GetBinLowEdge(i+1)
        if thisVal >= minVal and thisVal <= maxVal:
          bins.append(dataDistOLD.GetXaxis().GetBinLowEdge(i+1))

    dataDist = htmp #rt.TH1F("dataDist", "dataDist", len(xbins)-1, array('d',xbins))
    # for i in range(0, dataDistOLD.GetXaxis().GetNbins()):
 #        binCenter = dataDistOLD.GetXaxis().GetBinCenter(i+1)
 #        binContent = dataDistOLD.GetBinContent(i+1)
 #        binWidth = dataDistOLD.GetBinWidth(i+1)
 #        if binCenter > minVal:
 #            iBin =  dataDist.GetXaxis().FindBin(binCenter)
 #            dataDist.SetBinContent(iBin, binContent)


    p0 = rt.RooRealVar("p0", "p0", 8.5 , 0. , 2200.)
    p1 = rt.RooRealVar("p1", "p1", 0.0, -100. , 1000.)
    p2 = rt.RooRealVar("p2", "p2", 7.85115, 0., 1000.)
    p3 = rt.RooRealVar("p3", "p3", 0., -12., 12.)
    
    a0= 0
    a1= 0
    a2= 0
    a3= 0
    a3max=12.
    a3min=-12.
    a0max=20.
    a0min= -10.
    
    if h.find("WW") != -1 and h.find("High") != -1:     
      a0  =  1.31274e-02
      a1  = -2.42314e+00
      a2  =  4.70224e+00
      a3  =  5.41163e+02
      a3max = 1000.
      a3min =-1000.

      a0min = -100.
      a0max = 100.
    if h.find("WW") != -1 and h.find("Low") != -1:
      a0 =  4.48531e-07 
      a1 =  -7.96655e-01
      a2 =  7.43952e+00 
      a3 = 0.
    if h.find("ZZ") != -1 and h.find("Low") != -1:
      a0  =  4.48531e-07 
      a1  =  -7.96655e-01
      a2  =  7.43952e+00 
      a3  = 0. 
    if h.find("ZZ") != -1 and h.find("High") != -1:
      a0 =  9.66361e-07
      a1 = -1.15120e+01
      a2 =  6.63440e+00
      a3 =  1.04241e+01
      a3max = 100.
      a3min = -100.
      
    if h.find("WZ") != -1 and h.find("High") != -1:
      a0  =  1.31274e-02
      a1  = -2.42314e+00
      a2  =  4.70224e+00
      a3  =  5.41163e+02
      a3max = 1000.
      
    if h.find("WZ") != -1 and h.find("Low") != -1:
      a0 = 4.48531e-07 
      a1 = -7.96655e-01
      a2 = 7.43952e+00 
      a3 =  0.0
    
    
    
    
    p0_alt = rt.RooRealVar("p0_alt", "p0_alt", a0 , a0min , a0max)
    p1_alt = rt.RooRealVar("p1_alt", "p1_alt", a1, -100. , 100.)
    p2_alt = rt.RooRealVar("p2_alt", "p2_alt", a2, 0., 50.)
    p3_alt = rt.RooRealVar("p3_alt", "p3_alt", a3, a3min, a3max)
    
    
    m_lExp = rt.RooRealVar("mean_lExp","mean_lExp",100.,-5000.,5000)
    p1_lExp   = rt.RooRealVar("p1_lExp","p1_lExp",1.,0.,700.)
    p2_lExp   = rt.RooRealVar("p2_lExp","p2_lExp",1.,0.,500.)
    if h.find("LowPuri")!=-1:
        m_lExp = rt.RooRealVar("mean_lExp","mean_lExp",100.,-5000.,5000)
        p1_lExp   = rt.RooRealVar("p1_lExp","p1_lExp",100.,0.,700.)
        p2_lExp   = rt.RooRealVar("p2_lExp","p2_lExp",1.,0.,500.)
    if h.find("LowPuriZZ")!=-1:
        m_lExp = rt.RooRealVar("mean_lExp","mean_lExp",100.,-5000.,5000)    
        p1_lExp   = rt.RooRealVar("p1_lExp","p1_lExp",10.,0.,700.)    
        p2_lExp   = rt.RooRealVar("p2_lExp","p2_lExp",1.,0.,500.)    
        
    if h.find("LowPuriVV")!=-1:
        m_lExp = rt.RooRealVar("mean_lExp","mean_lExp",100.,-5000.,5000)      
        p1_lExp   = rt.RooRealVar("p1_lExp","p1_lExp",10.,0.,700.)        
        p2_lExp   = rt.RooRealVar("p2_lExp","p2_lExp",1.,0.,500.)        

    mjj = rt.RooRealVar("mjjCMS","Dijet invariant mass (GeV)",len(bins)-1, bins[0], bins[-1])

    #bkg_fit = rt.RooGenericPdf("bkg_fitCMS", "pow(1-@0/13000., @1)/pow(@0/13000., @2)", rt.RooArgList(mjj, p1, p2))
    bkg_fit_alt = rt.RooGenericPdf("bkg_fit_levelledExp", "exp(-(@0-@1)/(@2+@3*(@0-@1)))" ,rt.RooArgList(mjj,m_lExp,p1_lExp,p2_lExp))
    
    if alternative_func.find("alt")!=-1:
        bkg_fit_alt = rt.RooGenericPdf("bkg_fit_alt","( @1*pow(1-@0/13000 + @4*pow(@0/13000,2),@2) ) / ( pow(@0/13000,@3) )", rt.RooArgList(mjj,p0_alt,p1_alt,p2_alt,p3_alt))
    
    
    
    print title
    print "Setting parameter 1 constant"
    bkg_fit = rt.RooGenericPdf("bkg_fitCMS", "(1-@0/13000.)/pow(@0/13000., @1)", rt.RooArgList(mjj, p2))

    alpha = rt.RooRealVar("alpha","alpha",alphas[ii], 0., 4)
    sigfrac = rt.RooRealVar("sigfrac","sigfrac",sigfracs[ii], 0.3, .90)
    gsigma = rt.RooRealVar("gsigma","gsigma",gsigmas[ii], 0., 130)
    mean = rt.RooRealVar("mean","mean",means[ii], 1900., 2100.)
    sign = rt.RooRealVar("sign","sign",signs[ii], 0.0, 150)
    sigma = rt.RooRealVar("sigma","sigma",sigmas[ii], 10., 100.)

    gauss = rt.RooGaussian("gauss", "gauss", mjj, mean, gsigma)
    cb    = rt.RooCBShape("cb", "cb",mjj, mean, sigma, alpha, sign)
    sig_fit = rt.RooAddPdf("sigP", "sigP",gauss, cb, sigfrac)

    sigfrac.setConstant(rt.kTRUE)
    alpha.setConstant(rt.kTRUE)
    sign.setConstant(rt.kTRUE)
    mean.setConstant(rt.kTRUE)
    sigma.setConstant(rt.kTRUE)
    gsigma.setConstant(rt.kTRUE)

    syield = signalrate[ii]*scaleToExcluded[ii]
    nsig = rt.RooRealVar("NsExp", "Expected signal yield",syield, 0, 10)
    signalPDF = rt.RooExtendPdf("mysig","mysig",sig_fit,nsig)
    nsig.setConstant(rt.kTRUE)

    s = rt.RooRealVar("Ns", "signal yield",0., 0., 0.)
    b = rt.RooRealVar("Nb", "background yield", dataDist.Integral(), 0, dataDist.Integral()*10.)

    sumPDF = rt.RooAddPdf("sum", "gaussian plus exponential PDF",
                          rt.RooArgList(sig_fit, bkg_fit), rt.RooArgList(s, b))

    s.setConstant(rt.kTRUE)

    mjjbins = rt.RooBinning(len(bins)-1, array('d',bins), "mjjbins")
    mjj.setBinning(mjjbins)

    ws = rt.RooWorkspace("ws","ws")
    getattr(ws,'import')(p0)
    getattr(ws,'import')(p1)
    getattr(ws,'import')(p2)
    getattr(ws,'import')(mjj)
    getattr(ws,'import')(mean)
    getattr(ws,'import')(sigma)
    getattr(ws,'import')(s)
    getattr(ws,'import')(b)
    getattr(ws,'import')(sign)
    getattr(ws,'import')(alpha)
    getattr(ws,'import')(sigfrac)
    getattr(ws,'import')(sumPDF)
    getattr(ws,'import')(signalPDF)


    dataset = rt.RooDataHist("dataCMS", "dataCMS", rt.RooArgList(mjj), rt.RooFit.Import(dataDist))
    getattr(ws,'import')(dataset)

    fr = sumPDF.fitTo(dataset,rt.RooFit.Save())
    fr2 = bkg_fit_alt.fitTo(dataset,rt.RooFit.Save())
    #fr3 = bkg_fit_alt.fitTo(dataset, rt.RooFit.Save())
    print fr2


    frame = mjj.frame()
    dataset.plotOn(frame,rt.RooFit.DataError(rt.RooAbsData.Poisson), rt.RooFit.Binning(mjjbins),rt.RooFit.Name("data"),rt.RooFit.Invisible())
    
    bkg_fit_alt.plotOn(frame, rt.RooFit.VisualizeError(fr2,1),rt.RooFit.FillColor(rt.kBlue-7),rt.RooFit.LineColor(rt.kBlue-7),rt.RooFit.Name("fiterr2"), rt.RooFit.Binning(mjjbins))
    bkg_fit_alt.plotOn(frame,rt.RooFit.LineColor(rt.kBlue+1),rt.RooFit.Name(alternative_func))
    
    #bkg_fit_alt.plotOn(frame,rt.RooFit.LineColor(rt.kGreen+1),rt.RooFit.Name("alt"))
    
    sumPDF.plotOn(frame, rt.RooFit.VisualizeError(fr,1),rt.RooFit.FillColor(rt.kRed-7),rt.RooFit.LineColor(rt.kRed-7),rt.RooFit.Name("fiterr"), rt.RooFit.Binning(mjjbins))
    sumPDF.plotOn(frame,rt.RooFit.LineColor(rt.kRed+1),rt.RooFit.Name("sumPDF"))
    
    frame3 = mjj.frame()
    hpull = frame.pullHist("data","sumPDF",True)
    hpull.SetMarkerColor(rt.kRed)
    hpull2 = frame.pullHist("data",alternative_func,True)
    print hpull2
    hpull2.SetMarkerColor(rt.kBlue)
    frame3.addPlotable(hpull,"X0 P E1")
    frame3.addPlotable(hpull2,"X0 P E1")
    
    dataset.plotOn(frame,rt.RooFit.DataError(rt.RooAbsData.Poisson), rt.RooFit.Binning(mjjbins),rt.RooFit.Name("data"),rt.RooFit.XErrorSize(0))

    mjj.setRange("sigRegion",2000*0.8,2000*1.2) ;
    signalPDF.plotOn(frame,rt.RooFit.LineColor(rt.kBlack),rt.RooFit.LineStyle(rt.kDashed),rt.RooFit.Binning(mjjbins),rt.RooFit.Name("sig"),rt.RooFit.Normalization(1, rt.RooAbsReal.RelativeExpected),rt.RooFit.Range("sigRegion"))

    c1 =rt.TCanvas("c1","",800,800)
    c1.SetLogy()
    c1.Divide(1,2,0,0,0)
    c1.SetLogy()
    c1.cd(1)
    p11_1 = c1.GetPad(1)
    p11_1.SetPad(0.01,0.26,0.99,0.98)
    p11_1.SetLogy()
    p11_1.SetRightMargin(0.05)
    p11_1.SetTopMargin(0.1)
    p11_1.SetBottomMargin(0.02)
    p11_1.SetFillColor(0)
    p11_1.SetBorderMode(0)
    p11_1.SetFrameFillStyle(0)
    p11_1.SetFrameBorderMode(0)
    frame.GetYaxis().SetTitleSize(0.06)
    frame.GetYaxis().SetTitleOffset(0.98)
    # frame.GetYaxis().SetLabelSize(0.09)
    frame.SetMinimum(0.2)
    frame.SetMaximum(1E5)
    frame.SetName("mjjFit")
    frame.GetYaxis().SetTitle("Events / 100 GeV")
    frame.SetTitle("")
    frame.Draw()

    legend = rt.TLegend(0.52097293,0.64183362,0.6681766,0.879833)
    legend2 = rt.TLegend(0.52097293,0.64183362,0.6681766,0.879833)
    legend.SetTextSize(0.042)
    legend.SetLineColor(0)
    legend.SetShadowColor(0)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetMargin(0.35)
    legend2.SetTextSize(0.042)
    legend2.SetLineColor(0)
    legend2.SetShadowColor(0)
    legend2.SetLineStyle(1)
    legend2.SetLineWidth(1)
    legend2.SetFillColor(0)
    legend2.SetFillStyle(0)
    legend2.SetMargin(0.35)
    legend.AddEntry(frame.findObject("data"),"CMS data","lpe")
    if alternative_func.find("lExp")!=-1:
        legend.AddEntry(frame.findObject("lExp"),"levelled exponential","l")
    elif alternative_func.find("alt")!=-1:
        legend.AddEntry(frame.findObject("alt"),"alt. 4 param. fit","l")
    legend.AddEntry(frame.findObject("sumPDF"),"2 par. background fit","l")
    legend.AddEntry(frame.findObject("sig"),"%s (#sigma = %.3f pb)"%(legends[ii],xsec[ii]),"l")
    legend2.AddEntry("","","")
    legend2.AddEntry(frame.findObject("fiterr2"),"","f")
    legend2.AddEntry(frame.findObject("fiterr"),"","f")
    legend2.AddEntry("","","")

    legend2.Draw("same")
    legend.Draw("same")

    addInfo = rt.TPaveText(0.6110112,0.4166292,0.8502143,0.6123546,"NDC")
    addInfo.AddText(categories[ii])
    addInfo.AddText("|#eta| #leq 2.5, p_{T} > 200 GeV")
    addInfo.AddText("M_{jj} > 1050 GeV, |#Delta#eta_{jj}| #leq 1.3")
    addInfo.SetFillColor(0)
    addInfo.SetLineColor(0)
    addInfo.SetFillStyle(0)
    addInfo.SetBorderSize(0)
    addInfo.SetTextFont(42)
    addInfo.SetTextSize(0.045)
    addInfo.SetTextAlign(12)
    addInfo.Draw()
    CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)
    c1.Update()



    c1.cd(2)
    p11_2 = c1.GetPad(2)
    p11_2.SetPad(0.01,0.02,0.99,0.27)
    p11_2.SetBottomMargin(0.35)
    p11_2.SetRightMargin(0.05)
    # p11_2.SetGridx()
    # p11_2.SetGridy()
    frame3.SetMinimum(-2.9)
    frame3.SetMaximum(2.9)
    frame3.SetTitle("")
    frame3.SetXTitle("Dijet invariant mass (GeV)")
    frame3.GetXaxis().SetTitleSize(0.06)
    frame3.SetYTitle("#frac{Data-Fit}{#sigma_{data}}")
    frame3.GetYaxis().SetTitleSize(0.15)
    frame3.GetYaxis().CenterTitle()
    frame3.GetYaxis().SetTitleOffset(0.30)
    frame3.GetYaxis().SetLabelSize(0.15)
    frame3.GetXaxis().SetTitleSize(0.17)
    frame3.GetXaxis().SetTitleOffset(0.91)
    frame3.GetXaxis().SetLabelSize(0.12)
    frame3.GetXaxis().SetNdivisions(906)
    frame3.GetYaxis().SetNdivisions(305)
    frame3.Draw("same")
    line = rt.TLine(minVal,0,frame3.GetXaxis().GetXmax(),0)
    line1  = rt.TLine(minVal,1,frame3.GetXaxis().GetXmax(),1)
    line2  = rt.TLine(minVal,-1,frame3.GetXaxis().GetXmax(),-1)
    line1.SetLineStyle(2)
    line1.SetLineWidth(2)
    line2.SetLineStyle(2)
    line2.SetLineWidth(2)
    line.Draw("same")
    line1.Draw("same")
    line2.Draw("same")
    c1.Update()

    print title
    canvname = outdir+"MLBkgFit_%s_%s.pdf"%(histos[ii],alternative_func)
    c1.SaveAs(canvname)
    c1.SaveAs(canvname.replace("pdf","C"),"C")

    time.sleep(5)
    del c1, frame, frame3, legend, legend2, bkg_fit, sumPDF, htmp
