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
parser.add_option("-p", "--path", dest="path", action='store',default="/usr/users/dschaefer/CMSSW_7_4_7/src/DijetCombineLimitCode/",
                              help="set input path")
(opts, args) = parser.parse_args(argv) 

systhp = 0.11 
systlp = 0.23

def get_SF_VV():
 fsys = []
 #systhp = 0.1
 fsys.append( (1+systhp)*(1+systhp) )
 fsys.append( (1-systhp)*(1-systhp) )
 #systlp = 0.219
 fsys.append( (1+systhp)*(1-systlp) )
 fsys.append( (1-systhp)*(1+systlp) )
 return fsys

def get_SF_qV():
 fsys = []
 
 fsys.append( (1+systhp) )
 fsys.append( (1-systhp) )
 fsys.append( (1-systlp) )
 fsys.append( (1+systlp) )
 return fsys


indir = opts.path+'datacards/'
outdir = opts.path+'datacards/'

signals  = ["MCBulkZZ"]#,"altBulkZZ"]
signals  = ["altBulkWW","altBulkZZ"]#,"altBulkZZ"]#
#signals=["altBulkWW","BulkWW"]
#signals  = ["BulkZZ","BulkWW","WZ","ZprimeWW","qW","qZ"]
#signals  = ["qW","qZ"]
purities = ["LP","HP"]
if opts.batch:
    signals = [opts.signal]

for signal in signals:  
  masses =[m*100 for m in range(11,42+1)]
  channels = ["WW","WZ","ZZ"]
  if signal.find("q")!=-1:
    masses =[m*100 for m in range(12,62+1)]
    channels = ["qW","qZ"]
  if opts.batch:
      masses=[int(opts.mass)]
  for purity in purities:
    for ch in channels:
       for m in masses:
         
         
         fname_datacard_in  = indir  + "CMS_jj_%s_%i"%(signal,m)+"_13TeV_CMS_jj_"+ch+purity+".txt"
         fname_datacard_out = outdir + "CMS_jj_%s_%i"%(signal,m)+"_13TeV_CMS_jj_"+ch+purity+".txt"

         lines = []
         
         print "For input datacard:" ,fname_datacard_in
 
         newline  = '\nCMS_eff_vtag_tau21_sf_13TeV        lnN     '
           
         if signal.find("q")!=-1:
          
           sysqV = get_SF_qV()
           if   purity.find("HP") !=-1: 
            
             print "%.3f/%.3f           %.3f/%.3f        -" %( sysqV[0] ,sysqV[1] ,sysqV[0] ,sysqV[1] )
             newline += "%.3f/%.3f           %.3f/%.3f        -" %( sysqV[0] ,sysqV[1] ,sysqV[0] ,sysqV[1] )
           elif purity.find("LP") !=-1: 
             
             newline += "%.3f/%.3f           %.3f/%.3f        -" %( sysqV[2] ,sysqV[3] ,sysqV[2] ,sysqV[3] )
           else: print "THIS CATEGORY DOES NOT EXIST!!"            
         else: 
        
           sysVV = get_SF_VV()                                                  
           if   purity.find("HP") !=-1: newline += "%.3f/%.3f           %.3f/%.3f        -" %( sysVV[0] ,sysVV[1] ,sysVV[0] ,sysVV[1] )
           elif purity.find("LP") !=-1: newline += "%.3f/%.3f           %.3f/%.3f        -" %( sysVV[2] ,sysVV[3] ,sysVV[2] ,sysVV[3] )
           else: print "THIS CATEGORY DOES NOT EXIST!!"
         newline  +='\n'
         print newline   
         
     

        
         try:
           print " Opening " , fname_datacard_in
           with open(fname_datacard_in) as infile:
             for line in infile:
               if not line.find("CMS_eff_vtag_tau21_sf_13TeV")!=-1:
                 lines.append(line)
             lines.append(newline)

             with open(fname_datacard_out, 'w') as outfile:
               print " Writing to " , fname_datacard_out
               for line in lines:
                 outfile.write(line)
         except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
             print 'oops, datacard not found!'
