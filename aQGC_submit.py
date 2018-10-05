#!/usr/bin/env python
import os,glob,sys
sys.path.append('/afs/desy.de/user/a/albrechs/aQGCVVjj/python')
from ROOT import TFile
import PointName as PN 
from backup import backup_point
def testFileForLimits(filename):
    if(not os.path.isfile(filename)):
        # print filename, 'does not exists!'
        return False
    file=TFile(filename)
    tree=file.Get('limit')
    if(not tree):
        # print filename,'does not have any trees!'
        return False
    N_limits=tree.GetEntries()
    # file.Close()
    if(not (N_limits==6)):
        # print filename, 'is not complete!'
        return False
    else:
        return True

def submit(channels,parameters):
    for channel in channels:
        for parameter in parameters:
            signal=channel+'_'+parameter
            couplings=PN.OpList(parameter)
            # couplings=['m8p00','m4p00','4p00','8p00']
            queue_str=''
            for coupling in couplings:
                queue_str+=signal+' '+coupling+'\n'
                # queue_str+=signal+' '+coupling+'_SignalInjection\n'
            queue_str+=')'
            submitfile=open(signal+'.submit','w')
            submitfile.write(
                """executable          = submitwrapper.sh
transfer_executable = False
universe            = vanilla
requirements            = (OpSysAndVer == "SL6" || OpSysAndVer == "CentOS7")
error="""+signal+"""_$(var2)_$(ClusterId).$(Process).error
output="""+signal+"""_$(var2)_$(ClusterId).$(Process).out
log="""+signal+""".log
Args=fit $(var1) $(var2)
queue var1,var2 from (
""")
            submitfile.write(queue_str)
            submitfile.close()
            submit_command='condor_submit '+signal+'.submit -batch-name '+signal
            if('-d' in args):
                submit_command+=' -dry-run submit_dryrun.log'
            print submit_command
            os.system(submit_command)

def resubmit(channels, parameters):
    postfix = "Limits/"

    # regions=["_invMass","_invMass_afterVBFsel","_invMass_combined"]
    region="_invMass_combined"
    for chan in channels:
        for parameter in parameters:
            signal=chan+'_'+parameter
            couplings=PN.OpList(parameter)
            success=[]    
            failed=[]
            failed_couplings=[]
            success_couplings=[]
            queue_str=''
            for i in range(len(couplings)):
                coupling=couplings[i]
                if(testFileForLimits(postfix+"CMS_jj_0_"+chan+'_'+parameter+"_"+str(coupling)+"_13TeV_"+region+"_asymptoticCLs_new.root")):
                    success.append(postfix+"CMS_jj_0_"+chan+'_'+parameter+"_"+str(coupling)+"_13TeV_"+region+"_asymptoticCLs_new.root")
                    success_couplings.append(coupling)
                else:
                    failed.append(postfix+"CMS_jj_0_"+chan+'_'+parameter+"_"+str(coupling)+"_13TeV_"+region+"_asymptoticCLs_new.root")
                    failed_couplings.append(coupling)
                    queue_str+=signal+' '+coupling+'\n'
            queue_str+=')'

            resubmitfile=open(signal+'.resubmit','w')
            resubmitfile.write(
                """executable          = submitwrapper.sh
transfer_executable = False
universe            = vanilla
requirements            = (OpSysAndVer == "SL6" || OpSysAndVer == "CentOS7")
error="""+signal+"""_$(var2)_resub_$(ClusterId).$(Process).error
output="""+signal+"""_$(var2)_resub_$(ClusterId).$(Process).out
log="""+signal+"""_resub.log
Args=fit $(var1) $(var2)
queue var1,var2 from (
""")
            resubmitfile.write(queue_str)
            resubmitfile.close()
            resubmit_command='condor_submit '+signal+'.resubmit -batch-name '+signal+'_resub'
            if('-d' in args):
                resubmit_command+=' -dry-run resubmit_dryrun.log'
            print resubmit_command
            os.system(resubmit_command)
            
def submitPlots(channels,parameters):
    for channel in channels:
        queue_str=''
        for parameter in parameters:
            signal=channel+'_'+parameter
            queue_str+=signal+'\n'
        queue_str+=')'
        submitfile=open(channel+'.submit','w')
        submitfile.write(
            """executable          = submitwrapper.sh
transfer_executable = False
universe            = vanilla
requirements            = (OpSysAndVer == "SL6" || OpSysAndVer == "CentOS7")
error=$(var1)_$(ClusterId).$(Process).error
output=$(var1)_$(ClusterId).$(Process).out
log="""+channel+""".log
Args=plot $(var1)
queue var1 from (
""")
        submitfile.write(queue_str)
        submitfile.close()
        submit_command='condor_submit '+channel+'.submit -batch-name '+channel+'_LastStep'
        if('-d' in args):
            submit_command+=' -dry-run resubmit_dryrun.log'
        print submit_command
        os.system(submit_command)

def local(channels,parameters,coupling=''):
    for channel in channels:
        for parameter in parameters:
            signal=channel+'_'+parameter
            if coupling=='':
                # coupling="m21p00_SignalInjection"
                coupling="m15p40_SignalInjection"
            submit_command='./submitwrapper.sh '+signal+' '+coupling
            print submit_command
            os.system(submit_command)

def backup_local(channels,parameters):
    for channel in channels:
        for parameter in parameters:
            signal=channel+'_'+parameter
            couplings=PN.OpList(parameter)
            for i in range(len(couplings)):
                coupling=couplings[i]
                backup_point(signal,coupling,'fit')
                backup_point(signal,coupling,'plot')    
    
if (__name__=='__main__'):
    # channels=['VV','ssWW','ZZ']
    # channels=['VV','ssWW']
    # channels=['ssWW','VV','WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
    channels=['VV']
    parameters=["T8"]
    # channels=['WPWP','WPWM','WMWM','WPZ','WMZ']
    # channels=['ZZ']
    # parameters=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]
    # parameters=["T0"]
    # parameters=['S0']
    # parameters=['M6']
    args=sys.argv[1:]
    if('-s' in args):
        print 'submit'
        submit(channels,parameters)
    elif('-r' in args):
        print 'resubmit'
        resubmit(channels,parameters)
    elif('-p' in args):
        submitPlots(channels,parameters)
    elif('-b' in args):
        backup_local(channels,parameters)
    else:
        print 'nothing'
    # channels=["VV"]
    # parameters=["M7"]
    # coupling='4p00'
    # local(channels,parameters,coupling)
