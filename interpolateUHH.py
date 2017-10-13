from ROOT import *
import ROOT as r
import sys
import array

def fnc_dscb(xx,pp):
  x   = xx[0];
  N   = pp[0];
  mu  = pp[1];
  sig = pp[2];
  a1  = pp[3];
  p1  = pp[4];
  a2  = pp[5];
  p2  = pp[6];

  u   = (x-mu)/sig;
  A1  = TMath.Power(p1/TMath.Abs(a1),p1)*TMath.Exp(-a1*a1/2);
  A2  = TMath.Power(p2/TMath.Abs(a2),p2)*TMath.Exp(-a2*a2/2);
  B1  = p1/TMath.Abs(a1) - TMath.Abs(a1);
  B2  = p2/TMath.Abs(a2) - TMath.Abs(a2);

  result=N;
  if (u<-a1):
      result *= A1*TMath.Power(B1-u,-p1);
  elif (u<a2):
      result *= TMath.Exp(-u*u/2);
  else:
      result *= A2*TMath.Power(B2+u,-p2);
  return result;

frac1 = 0.8 
frac2 = 1.2

inputRoot = sys.argv[1]
# print "INPUT = %s"%inputRoot
outmjj = int( sys.argv[2] )
# print "outmjj = %s"%outmjj
if len(sys.argv)>3:
   suffix=sys.argv[3]
else:
   suffix=""


# print "suffix = %s"%suffix
histnames= [
            "_invMass", # inclusive
            "_invMass_afterVBFsel", # vbf selection
            ]

if "graviton" in inputRoot:
  masses=[1500,2000,2500]

if "radion" in inputRoot:
  masses=[1500,2000,2500]
  
for i in range(len(masses)-1):
   if outmjj>=masses[i] and outmjj<masses[i+1]:
       mjjlow = masses[i]
       mjjhigh = masses[i+1]
if outmjj>=masses[-1]:
   mjjlow = masses[-2]
   mjjhigh = masses[-1]

inputlow = TFile( inputRoot + str(mjjlow) + suffix + '.root' )
inputhigh = TFile( inputRoot + str(mjjhigh) + suffix +  '.root' )
output = TFile( inputRoot +'Interpolated' + str(outmjj) + suffix + '.root', 'recreate')
# print "inputlow = %s"%inputlow
# print "inputhigh = %s"%inputhigh
# print "output = %s"%output

print sys.argv[1], outmjj, mjjlow, mjjhigh

hists=[]

for histname in histnames:
 hname=inputRoot.split("/")[-1]+histname
 flow = inputlow.Get( hname )
 flow.SetName( 'low' )
 fhigh = inputhigh.Get( hname )
 fhigh.SetName( 'high' ) 
 
 output.cd()
 #su = 0.
 foutmjj = TH1F(histname, histname, 13000, 0, 13000 )
 hists += [foutmjj]

 old_interpolation=False

 if old_interpolation:
   # interpolate the shape linearly
   su = 0
   su1 = 0.0
   for i in range(13001) :
     x = 0.0 + i/13000.0*2.0 # interpolation range: [0*mass,2*mass]
     masslow = x*mjjlow
     masshigh = x*mjjhigh
     #print masshigh
     massout = x*outmjj
     prob1 = flow.GetBinContent( flow.FindBin(masslow) ) 
     prob2 = fhigh.GetBinContent( fhigh.FindBin(masshigh) ) 
     #print x, prob1, prob2
     prob = prob1 + (prob2 - prob1)*(massout - mjjlow)/float(mjjhigh - mjjlow)
     #print x, prob
     #foutmjjfrac.SetBinContent(i+1, max(0,prob))
     foutmjj.SetBinContent( foutmjj.FindBin(massout), max(0,prob))
     su += prob
     su1 += prob2
   #print su
   #print su1

   # interpolate the peak height smoothly
   xvalues=r.vector('double')()
   yvalues=r.vector('double')()
   for x in masses:
     inputf = TFile( inputRoot + str(x) + suffix + '.root' )
     f = inputf.Get( hname )
     xvalues.push_back(x)
     yvalues.push_back(f.Integral(f.FindBin(x*0.8),f.FindBin(x*1.2))*10.) #100 000 is 2015 default, test 10 000
   interpolator=r.Math.Interpolator(xvalues,yvalues)
   integral=interpolator.Eval(outmjj)
   foutmjj.Scale( integral/foutmjj.Integral(foutmjj.FindBin(outmjj*0.8),foutmjj.FindBin(outmjj*1.2)) )
 else:
   # interpolate the peak height+shape smoothly
   xvalues=r.vector('double')()
   yvalues=[]
   npoints=20000
   rebin=1
   for i in range(npoints+1) :
     yvalues+=[r.vector('double')()]
   for m in masses:
     inputf = TFile( inputRoot + str(m) + suffix + '.root' )
     f = inputf.Get( hname )
     xvalues.push_back(m)
     for i in range(npoints+1):
       x=0.0 + i/float(npoints)*2.0
       yvalues[i].push_back(f.Integral(f.FindBin(m*x)-rebin+1,f.FindBin(m*x)+rebin-1)/float(2*rebin-1)*10.) #100 000 is 2015 default, test 10 000
   for i in range(npoints+1):
     x=0.0 + i/float(npoints)*2.0
     inter=r.Math.Interpolator(xvalues,yvalues[i])
     if outmjj>=masses[-1]:
         interpolation = inter.Eval(xvalues[-2]) + (inter.Eval(xvalues[-1]) - inter.Eval(xvalues[-2]))*(outmjj - xvalues[-2])/float(xvalues[-1] - xvalues[-2])
     else:
         interpolation=inter.Eval(outmjj)
     foutmjj.SetBinContent(foutmjj.FindBin(outmjj*x),max(0,interpolation))

 print foutmjj.Integral(foutmjj.FindBin(outmjj*0.8),foutmjj.FindBin(outmjj*1.2)), flow.Integral(flow.FindBin(mjjlow*0.8),flow.FindBin(mjjlow*1.2)), fhigh.Integral(fhigh.FindBin(mjjhigh*0.8),fhigh.FindBin(mjjhigh*1.2))


output.cd()
output.Write()
output.Close()
 
