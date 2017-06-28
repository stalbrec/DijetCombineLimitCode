from ROOT import *
import time
import CMS_lumi, tdrstyle
import time
from array import *

tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "  Simulation "
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

W = 800
H = 800
H_ref = 700 
W_ref = 600 
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

def getCanvas(name):
  c = TCanvas(name,name,W,H)
  c.SetTitle("")
  c.SetLeftMargin( L/W + 0.10)
  c.SetRightMargin( R/W +0.02)
  c.SetTopMargin( T/H )
  c.SetBottomMargin( B/H +0.02)
  c.SetTickx(0)
  c.SetTicky(0)
  return c
  


def doFit(hSignal, MASS, m,frame,color,mmax):
    data = RooDataHist("dh","dh", RooArgList( m), RooFit.Import(hSignal)) ;
    
    #binmax_pre = hPRE.GetMaximumBin();
    #x_pre = hPRE.GetXaxis().GetBinCenter(binmax_pre);
    #binmax_post = hPOST.GetMaximumBin();
    #x_post = hPOST.GetXaxis().GetBinCenter(binmax_post);
    # C r e a t e   m o d e l   a n d   d a t a s e t
    # -----------------------------------------------


    
    m0 = RooRealVar( "mean0", "mean0", MASS, 0.8*MASS, 1.2*MASS);
    gm0= RooRealVar( "gm0", "gm0", MASS, 0.8*MASS, 1.2*MASS);
    sigma = RooRealVar( "sigma" , "sigma", MASS*0.05 ,20., 700.);
    scalesigma = RooRealVar( "scalesigma", "scalesigma", 2., 1.2, 10.);
    alpha      = RooRealVar( "alpha", "alpha", 1.85288, 0.0, 20);
    sig_n      = RooRealVar( "sig_n"  , "sign", 129.697, 0., 300);
    frac       = RooRealVar( "frac", "frac", 0.0, 0.0, 0.35);
    
    gsigma  = RooFormulaVar( "gsigma","@0*@1", RooArgList( sigma, scalesigma ));
    
    gaus   = RooGaussian( "gauss", "gauss", m ,m0 , gsigma);
    cb     = RooCBShape ( "cb", "cb", m , m0 , sigma, alpha, sig_n);
    sigmodel = RooAddPdf  ( "model_"+str(MASS), "model_"+str(MASS), RooArgList( gaus, cb ), RooArgList(frac),1);
    
    sigmodel.fitTo(data,RooFit.Range(MASS*0.8,MASS*1.2),RooFit.SumW2Error(kTRUE),RooFit.PrintEvalErrors(-1),RooFit.Save(kTRUE));
    sigmodel.plotOn(frame,RooFit.Range(995,mmax),RooFit.LineColor(color))
    #data.plotOn(frame,RooFit.Binning(100),RooFit.Rescale(data.sumEntries()))
       
    return 0


def checkFit(hSignal, MASS, m,frame,color,mmax):
    data = RooDataHist("dh","dh", RooArgList( m), RooFit.Import(hSignal)) ;
    
    # C r e a t e   m o d e l   a n d   d a t a s e t
    # -----------------------------------------------

    m0 = RooRealVar( "mean0", "mean0", MASS, 0.8*MASS, 1.2*MASS);
    gm0= RooRealVar( "gm0", "gm0", MASS, 0.8*MASS, 1.2*MASS);
    sigma = RooRealVar( "sigma" , "sigma", MASS*0.05 ,20., 700.);
    scalesigma = RooRealVar( "scalesigma", "scalesigma", 2., 1.2, 10.);
    alpha      = RooRealVar( "alpha", "alpha", 1.85288, 0.0, 20);
    sig_n      = RooRealVar( "sig_n"  , "sign", 129.697, 0., 300);
    frac       = RooRealVar( "frac", "frac", 0.0, 0.0, 0.35);
    
    gsigma  = RooFormulaVar( "gsigma","@0*@1", RooArgList( sigma, scalesigma ));
    
    gaus   = RooGaussian( "gauss", "gauss", m ,m0 , gsigma);
    cb     = RooCBShape ( "cb", "cb", m , m0 , sigma, alpha, sig_n);
    sigmodel = RooAddPdf  ( "model_"+str(MASS), "model_"+str(MASS), RooArgList( gaus, cb ), RooArgList(frac),1);
    
    sigmodel.fitTo(data,RooFit.Range(MASS*0.77,MASS*1.2),RooFit.SumW2Error(kTRUE),RooFit.PrintEvalErrors(-1),RooFit.Save(kTRUE));
    data.plotOn(frame,RooFit.Binning(100))#,RooFit.Rescale(data.sumEntries()))
    sigmodel.plotOn(frame,RooFit.Range(995,mmax),RooFit.LineColor(color))
    return 0
    
def get_palette(mode):
  palette = {}
  palette['gv'] = [] 
  colors = ['#40004b','#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061','#46211A','#693D3D','#BA5536','#A43820','#AEBD38','#598234','#90AFC5','#336B87','#2A3132']
  #colors = ['#ffbbcc','#de77ae','#762a83','#9970ab','#a6dba0','#7ac5cd','#003b6f']
  #colors = ['#46211A','#693D3D','#BA5536','#A43820','#AEBD38','#598234','#90AFC5','#336B87','#2A3132']
  
  for c in colors:
    palette['gv'].append(c)
  return palette[mode] 

    
        
def SetFrameStyle(frame):
    frame.SetTitle("")
    frame.GetYaxis().SetTitle("arbitrary scale")
    frame.SetMaximum(0.4)
    frame.GetXaxis().SetTitle("m_{jj} (GeV)")
    frame.GetYaxis().SetTitleOffset(1.4)
    frame.SetNdivisions(4)
    return 0

if __name__=="__main__":
    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0)
    c = getCanvas("c")
    m = RooRealVar("m","m",1000,6500)
    mmax = 6800.
    masses =[1200,1400,1800,3000,3500,4000,4500]
    masses = [1300,1600,1900,2200,2500,2800,3100,3400,3700,4000]#,4300,4600,4900,5200,5500,5800,6000]
    masses = [1300,1900,2400,3100,3700,4200,4900,5500,6000]
    #masses = [2000]
    #histoname = "DijetMassHighPuriWZ"
    #category = "category HP WZ"
    #cat = "HPWZ"
    #signalname = "WprimeWZ"
    
    histoname = "DijetMassHighPuriqZ"
    category = "category HP qZ"
    cat = "HPqZ"
    signalname = "QstarQZ"
    palette = get_palette('gv')
    col = TColor()
    
    frame = m.frame()
    outdir = "~/AnalysisOutput/figures/controlplotsSignal/"
    r = []
    i=0
    for mass in masses:
        fname = signalname+"_13TeV_10k_OUT"+str(mass)+"GeV.root"
        tfile = TFile.Open(fname,'READ')
        hSignal = tfile.Get(histoname)
        hSignal .Rebin(4)
        #r.append(hSignal.SumEntries()*35867.*0.01/(10000.))
        #hSignal.Scale(1/hSignal.Integral())
        print hSignal
        graphColor = col.GetColor(palette[i])
        doFit(hSignal,mass,m,frame,graphColor,mmax)
        i+=1
        
        ## plot some PDF shapes 
        #indir = "/shome/dschafer/ExoDiBosonAnalysis/results/"
        #fname = indir+"Signal_BulkWW_M2000_PDF.root"
        #tfile = TFile.Open(fname,'READ')
        #hSignal = tfile.Get("WWHPHP0")
        
        #hSignal .Rebin(4)
        ##r.append(hSignal.SumEntries()*35867.*0.01/(10000.))
        ##hSignal.Scale(1/hSignal.Integral())
        #print hSignal
        #graphColor = col.GetColor(palette[i])
        #doFit(hSignal,mass,m,frame,graphColor,mmax)
        #i+=3
        #hSignal2 = tfile.Get("WWHPHP2")
        #hSignal2 .Rebin(4)
        ##r.append(hSignal.SumEntries()*35867.*0.01/(10000.))
        ##hSignal.Scale(1/hSignal.Integral())
        #print hSignal2
        #graphColor = col.GetColor(palette[i])
        #doFit(hSignal2,mass,m,frame,graphColor,mmax)
        #i+=3
        
        #hSignal3 = tfile.Get("WWHPHP99")
        #hSignal3 .Rebin(4)
        ##r.append(hSignal.SumEntries()*35867.*0.01/(10000.))
        ##hSignal.Scale(1/hSignal.Integral())
        #print hSignal3
        #graphColor = col.GetColor(palette[i])
        #doFit(hSignal3,mass,m,frame,graphColor,mmax)
        #i+=1
        
    
        ## print fits over the corresponding histos:
        #c2 = getCanvas("c"+str(mass))
        #frame2 = m.frame()
        #SetFrameStyle(frame2)
        #checkFit(hSignal, mass, m,frame2,col.GetColor(palette[0]),mmax)
        ###checkFit(hSysdown, mass, m,frame2,col.GetColor(palette[1]))
        ###checkFit(hSysup, mass, m,frame2,col.GetColor(palette[2]))
        #frame2.Draw()
        #CMS_lumi.CMS_lumi(c2, iPeriod, iPos)
        #c2.Update()
        #c2.SaveAs(outdir+"test_M"+str(mass)+"_"+cat+"_.pdf")
        
        #del frame2,c2
    SetFrameStyle(frame)
    frame.Draw()
    text = TLatex()
    text.SetTextFont(43);
    text.SetTextSize(38);
    text.SetTextColor(kBlack);
    s = "#bf{#font[62]{Z' #rightarrow WW}}"
    if signalname.find("BulkWW")!=-1:
        s = "#bf{#font[62]{G_{bulk} #rightarrow WW}}"
    if signalname.find("BulkZZ")!=-1:
        s = "#bf{#font[62]{G_{bulk} #rightarrow ZZ}}"
    if signalname.find("Wprime")!=-1:
        s = "#bf{#font[62]{W' #rightarrow WZ}}"
    if signalname.find("QstarQW")!=-1:
        s = "#bf{#font[62]{q* #rightarrow qW}}"
    if signalname.find("QstarQZ")!=-1:
        s = "#bf{#font[62]{q* #rightarrow qZ}}"
    text.DrawLatex(1250,0.36,s)
    text.DrawLatex(1250,0.33,"#font[42]{"+category+"}");
    #leg =  TLegend(0.715383,0.4644522,0.8538201,0.8869464,"","NDC")
    leg =  TLegend(0.63,0.4644522,0.88,0.8869464,"","NDC")
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    # l.SetNColumns(2)
    leg.SetTextSize(0.040)
    leg.SetLineColor(kBlack)
    leg.SetTextFont(42)
    leg.SetShadowColor(0)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetMargin(0.35)
    #leg.SetTextAlign(8)
    n =[]
    for t in range(0,len(masses)):
        n.append(frame.nameOf(t))
        leg.AddEntry(frame.findObject(n[t]),"m_{X} = "+str(round(masses[t]/1000.,1))+" TeV","l")
    leg.Draw()
    CMS_lumi.CMS_lumi(c, iPeriod, iPos)
    c.Update()
    c.SaveAs(outdir+"testSignalShapes_"+signalname+"_"+cat+".pdf")
    #c.SaveAs(outdir+"test_"+signalname+"_"+cat+".pdf")
    #for i in range(0,len(masses)):
        #print str(masses[i])+ "   " + str(r[i])
    #time.sleep(1)
    
    
    

    
    

    
    
    
