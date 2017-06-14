import sys,os
import ROOT
from ROOT import *
import math
from optparse import OptionParser
import sys

argv = sys.argv
parser = OptionParser()   
parser.add_option("-b", "--batch", dest="batch", default=False,action="store_true",
                              help="set batch mode")
parser.add_option("-s", "--signal", dest="signal", default="BulkWW",action= "store",
                              help="set signal. only in batch mode")
parser.add_option("-m", "--mass", dest="mass", default=1200,action ="store",
                              help="set mass. only in batch mode")
parser.add_option("-p", "--path", dest="path", action='store',default="/usr/users/dschaefer/CMSSW_7_4_7/src/DijetCombineLimitCode",
                              help="set input path")




 
# new for Moriond 2017: pT HP and LP uncertainty both fitted (no scaling with v-tag uncertainties anymore)
# treat uncertainties as correlated (since the migration between mass windows is correlated) (for ICHEP anti-correlation)
# new working point of 0.35
def get_sys_pt_vv(mass):
 fsys = []
 systhp = 8.5*math.log(mass/2./200.)/100.
 fsys.append( (1+systhp)*(1+systhp) )
 fsys.append( (1-systhp)*(1-systhp) )
# tothp = math.sqrt(0.03*0.03+0.04*0.04+0.06*0.06)/1.03 # efficiency scale factor HP = 1.03 +- 0.03 (stat -> fit unc.) +- 0.04 (sys->herwig vs pythia) +- 0.06 (sys -> different fit methods)
# totlp = math.sqrt(0.12*0.12+0.17*0.17+0.12*0.12)/0.88 # same for LP category
 #systlp = systhp*totlp/tothp
 systlp = 3.9*math.log(mass/2./200.)/100.
 #fsys.append( (1+systhp)*(1-systlp) )
 #fsys.append( (1-systhp)*(1+systlp) )
 fsys.append( (1+systhp)*(1+systlp) )
 fsys.append( (1-systhp)*(1-systlp) )
 return fsys

def get_sys_pt_qv(mass):
 fsys = []
 systhp = 8.5*math.log(mass/2./200.)/100.
 print systhp
 fsys.append( (1+systhp) )
 fsys.append( (1-systhp) )
 systlp = 3.9*math.log(mass/2./200.)/100.
 print systlp
 fsys.append( (1+systlp) )
 fsys.append( (1-systlp) )
 #tothp = math.sqrt(0.03*0.03+0.04*0.04+0.06*0.06)/1.03
 #totlp = math.sqrt(0.12*0.12+0.17*0.17+0.12*0.12)/0.88
 #systlp = systhp*totlp/tothp
 #fsys.append( (1-systlp) )
 #fsys.append( (1+systlp) )
 return fsys
   
if __name__=="__main__":
    (opts, args) = parser.parse_args(argv)  
    path = opts.path
    mass = opts.mass
    sig  = opts.signal
    print mass
    print sig
    print path
    indir = path+'/datacards/'
    outdir = path+'/datacards/'

    signals=["altBulkWW","altBulkZZ"]
    masses =[m*100 for m in range(11,45+1)]

    if opts.batch:
        signals=[opts.signal]
        masses=[int(opts.mass)]
        
    #signals  = ["BulkZZ","BulkWW","WZ","ZprimeWW"]
    #signals  = ["qW","qZ"]
    purities = ["LP","HP"]

    for signal in signals:  
        channels = ["WW","WZ","ZZ","VV"]
        if signal.find("q")!=-1:
            masses =[m*100 for m in range(12,62+1)]
            if opts.batch:
                masses=[int(opts.mass)]
            channels = ["qW","qZ"]
        for purity in purities:
            for ch in channels:
                for m in masses:
                
                
                    fname_datacard_in  = indir  + "CMS_jj_%s_%i"%(signal,m)+"_13TeV_CMS_jj_"+ch+purity+".txt"
                    fname_datacard_out = outdir + "CMS_jj_%s_%i"%(signal,m)+"_13TeV_CMS_jj_"+ch+purity+".txt"

                    lines = []
                    
                    print "For input datacard:" ,fname_datacard_in
            
                    newline  = '\nCMS_eff_vtag_tau21_pt_13TeV  lnN       '
                    
                    if signal.find("q")!=-1:
                    
                        sysqV = get_sys_pt_qv(m)
                        if   purity.find("HP") !=-1: 
                        
                            print "%.3f/%.3f           %.3f/%.3f        -" %( sysqV[0] ,sysqV[1] ,sysqV[0] ,sysqV[1] )
                            newline += "%.3f/%.3f           %.3f/%.3f        -" %( sysqV[0] ,sysqV[1] ,sysqV[0] ,sysqV[1] )
                        elif purity.find("LP") !=-1: 
                        
                            newline += "%.3f/%.3f           %.3f/%.3f        -" %( sysqV[2] ,sysqV[3] ,sysqV[2] ,sysqV[3] )
                        else: print "THIS CATEGORY DOES NOT EXIST!!"            
                    else: 
                    
                        sysVV = get_sys_pt_vv(m)                                                  
                        if   purity.find("HP") !=-1: newline += "%.3f/%.3f           %.3f/%.3f        -" %( sysVV[0] ,sysVV[1] ,sysVV[0] ,sysVV[1] )
                        elif purity.find("LP") !=-1: newline += "%.3f/%.3f           %.3f/%.3f        -" %( sysVV[2] ,sysVV[3] ,sysVV[2] ,sysVV[3] )
                        else: print "THIS CATEGORY DOES NOT EXIST!!"
                    newline  +='\n'
                    print newline   
            
        

            
            try:
                print " Opening " , fname_datacard_in
                with open(fname_datacard_in) as infile:
                    for line in infile:
                        if not line.find("CMS_eff_vtag_tau21_pt_13TeV")!=-1:
                            lines.append(line)
                        lines.append(newline)

                with open(fname_datacard_out, 'w') as outfile:
                    print " Writing to " , fname_datacard_out
                    for line in lines:
                        outfile.write(line)
            except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
                print 'oops, datacard not found!'
