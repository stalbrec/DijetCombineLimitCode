#!/usr/bin/env python
import os,glob,sys
sys.path.append('/afs/desy.de/user/a/albrechs/aQGCVVjj/python')
import PointName as PN 

if (__name__=='__main__'):
    # channels=['ssWW','VV','WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
    # channels=['ssWW','VV','WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
    # channels=['ssWW','VV']
    channels=['ZZ']
    parameters=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]
    for channel in channels:
        queue_str=''
        for parameter in parameters:
            signal=channel+'_'+parameter
            queue_str+=signal+'\n'
        queue_str+=')'
        submitfile=open(channel+'.submit','w')
        submitfile.write(
            """executable          = submitLastWrapper.sh
transfer_executable = False
universe            = vanilla
requirements            = (OpSysAndVer == "SL6" || OpSysAndVer == "CentOS7")
error="""+channel+""".error
output="""+channel+""".out
log="""+channel+""".log
Args= $(var1)
queue var1 from (
""")
        submitfile.write(queue_str)
        submitfile.close()
        submit_command='condor_submit '+channel+'.submit -batch-name '+channel+'_LastStep'
        print submit_command
        os.system(submit_command)
# #!/usr/bin/env python
# import os,glob,sys
# sys.path.append('/afs/desy.de/user/a/albrechs/aQGCVVjj/python')
# import PointName as PN 
# from backup import backup

# if (__name__=='__main__'):
#     # channels=['VV']
#     # parameters=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]

#     signal=sys.argv[1]
#     os.system('python Limits/brazilianFlag_aQTGC.py '+str(signal))
