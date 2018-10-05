#!/usr/local/bin/python2.7
import ROOT as rt
from ROOT import *
import time,os,glob,math,array,sys,csv,random
import numpy as np
sys.path.append('/nfs/dust/cms/user/zoiirene/CombineTutorial/CMSSW_8_1_0/src/DijetCombineLimitCode/Limits')
import CMS_lumi                                                                                        
sys.path.append('/afs/desy.de/user/a/albrechs/aQGCVVjj/python')           
import PointName as PN
import TGraphTools as TGT


def Plot(couplings=[1],results=[1]):
    if(len(couplings)!=len(results)):
        print 'Number of x and y Points does not match'
        return 0
    
    grmean = rt.TGraphErrors(len(couplings))
    grmean.SetLineColor(1)
    grmean.SetLineWidth(4)
    grmean.SetLineStyle(2) #irene
    grmean.SetMarkerStyle(20) #irene
    
    for j in range(0,len(couplings)):
        grmean.SetPoint(j, couplings[j], results[j][0])

    canv=TCanvas('test','test',600,600)
    grmean.Draw()
    canv.Print('test.eps')
    # return 'sdf'

if __name__ == '__main__':
    postfix = "Limits/"
    gROOT.SetBatch(True)
    
    channel=sys.argv[1]
    parameter=sys.argv[2]
    
    results=[]
    
    path='/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/HTC/fit/'+channel+'/'+parameter+'/'
    couplings=PN.OpList(parameter)
    combinedplots=[]    
    couplings_f=[]
    for coupling in couplings:
        stmp = coupling.replace("p",".")
        stmp = stmp.replace("m","-")
        filename=path+coupling+'_current/CMS_jj_'+channel+'_'+parameter+'_'+coupling+'_0_13TeV__invMass_combined_MaxLikelihoodFit.out'
        if(os.path.isfile(filename)):
            best_r=[]
            with open(filename,'r') as infile:                
                for line in infile:
                    if('Best fit r:' in line):
                        best_r.append(float(line.split(' ')[3]))
                        best_r.append(float(line.split(' ')[5].split('/')[0]))
                        best_r.append(float(line.split(' ')[5].split('/')[1]))            
            if(best_r[0]<5):
                results.append(best_r)
                couplings_f.append(float(stmp)) 
    Plot(couplings_f,results)
