#!/usr/bin/env python
import os,glob,sys
sys.path.append('/afs/desy.de/user/a/albrechs/aQGCVVjj/python')
from ROOT import TFile
import PointName as PN 
def update_progress(iteration,complete):
    barLength = 30
    status = ""
    progress=float(iteration)/float(complete)
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rFiles processed: %i/%i [%s] %s"%(int(iteration),int(complete),"#"*block+"-"*(barLength-block),status) 
    sys.stdout.write(text)
    sys.stdout.flush()

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
            # couplings=["210p00","210p00_SignalInjection","210p00_SidebandData"]
            # couplings=["6p00","6p00_SignalInjection","6p00_SidebandData"]
            # couplings=["6p00","6p02","6p01"]
            # couplings=["m21p00_SignalInjection"]
            # queue_str='"Queue Arguments From ( \n'
            #queue_str='(\n'
            queue_str=''
            for coupling in couplings:
                queue_str+=signal+' '+coupling+'\n'
                # print coupling
                #submit_command='qsub -l distro=sld6 -l h_vmem=10G -l h_rt=15:59:59 -cwd -N '+signal+'_'+coupling+'_4 submitwrapper.sh '+signal+' '+coupling+''
                # submit_command=' condor_submit jobChannelPoint.submit -append "arguments = '+signal+' '+coupling+'" -append "error='+signal+'_'+coupling+'.error" -append "output='+signal+'_'+coupling+'.out" -append "log='+signal+'_'+coupling+'.log"'
                # print submit_command
                # os.system(submit_command)
            # python submitLimits.py ${channels[$i]}_${parameters[$j]}
            # queue_str=queue_str[:-1]
            queue_str+=')'

            # Args = -i $(Item)
            # Queue Item in (pasta, chicken
            submitfile=open(signal+'.submit','w')
            submitfile.write(
                """executable          = submitwrapper.sh
transfer_executable = False
universe            = vanilla
requirements            = (OpSysAndVer == "SL6" || OpSysAndVer == "CentOS7")
error="""+signal+""".error
output="""+signal+""".out
log="""+signal+""".log
Args= $(var1) $(var2)
queue var1,var2 from (
""")
            submitfile.write(queue_str)
            submitfile.close()
            # submit_command=' condor_submit jobChannelPoint.submit -append "error='+signal+'.error" -append "output='+signal+'.out" -append "log='+signal+'.log"' + ' -append '+queue_str
            submit_command='condor_submit '+signal+'.submit -batch-name '+signal
            if('-d' in args):
                submit_command+=' -dry-run submit_dryrun.log'            # submit_command='condor_submit '+signal+'.submit -batch-name '+signal+'_'+parameter+' -dry-run test.log'
            # submit_command='condor_submit jobChannelPoint.submit -dry-run test.log -append "error='+signal+'.error" -append "output='+signal+'.out" -append "log='+signal+'.log"' + ' -append "queue var1,var2 from '+queue_str
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
            # print("checking for failed jobs..") 
            queue_str=''
            for i in range(len(couplings)):
                coupling=couplings[i]
                if(testFileForLimits(postfix+"CMS_jj_0_"+chan+'_'+parameter+"_"+str(coupling)+"_13TeV_"+region+"_asymptoticCLs_new.root")):
                    success.append(postfix+"CMS_jj_0_"+chan+'_'+parameter+"_"+str(coupling)+"_13TeV_"+region+"_asymptoticCLs_new.root")
                    success_couplings.append(coupling)
                else:
                    # print 'skipping', coupling
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
error="""+signal+"""_resub.error
output="""+signal+"""_resub.out
log="""+signal+"""_resub.log
Args= $(var1) $(var2)
queue var1,var2 from (
""")
            resubmitfile.write(queue_str)
            resubmitfile.close()
            # submit_command=' condor_submit jobChannelPoint.submit -append "error='+signal+'.error" -append "output='+signal+'.out" -append "log='+signal+'.log"' + ' -append '+queue_str
            # resubmit_command='condor_submit '+signal+'.resubmit -dry-run test.log -batch-name '+signal+'_'+parameter+'_resub'
            resubmit_command='condor_submit '+signal+'.resubmit -batch-name '+signal+'_resub'
            if('-d' in args):
                resubmit_command+=' -dry-run resubmit_dryrun.log'
            print resubmit_command
            os.system(resubmit_command)
            
def local(channels,parameters,coupling=''):
    for channel in channels:
        for parameter in parameters:
            signal=channel+'_'+parameter
            if coupling=='':
                coupling="m21p00_SignalInjection"
            submit_command='./submitwrapper.sh '+signal+' '+coupling
            print submit_command
            os.system(submit_command)
    
if (__name__=='__main__'):
    # channels=['VV','ssWW','ZZ']
    # channels=['VV','ssWW']
    # channels=['ssWW','VV','WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
    channels=['VV']
    parameters=["M7"]
    # parameters=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]
    # parameters=['S0']
    # parameters=['M6']
    args=sys.argv[1:]
    if('-s' in args):
        print 'submit'
        submit(channels,parameters)
    elif('-r' in args):
        print 'resubmit'
        resubmit(channels,parameters)
    else:
        print 'nothing'
    # channels=["VV"]
    # parameters=["M7"]
    # coupling='4p00'
    # local(channels,parameters,coupling)
