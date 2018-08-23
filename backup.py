import os,glob,tarfile,sys
from time import gmtime, strftime
sys.path.append('/afs/desy.de/user/a/albrechs/aQGCVVjj/python')
import PointName as PN

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    tar.close()

def backup_point(signal,point,mode='fit'):
    channel=signal.split('_')[0]
    parameter=signal.split('_')[1]
    name=signal+'_'+point

    # backup_dir='HTC/'+mode+'/'+channel+'/'+parameter+'/'+point+'_0'
    if(mode=='fit'):
            backup_dir='HTC/'+mode+'/'+channel+'/'+parameter+'/'+point+'_current'
    elif(mode=='fit'):
        backup_dir='HTC/'+mode+'/'+channel+'/'+parameter+'_current'
    i=0
    old_backup_dir=backup_dir
    while(os.path.exists(old_backup_dir)):        
        old_backup_dir=''.join(old_backup_dir.split('_')[:-1])+'_%i'%i
        print ''.join(old_backup_dir.split('_')[:-1])+'_%i'%i
        i+=1
    if(os.path.exists(backup_dir)):
        os.system('mv '+backup_dir+' '+old_backup_dir)
    os.makedirs(backup_dir)

    basedir_files=[
        #base:
        'CMS_jj_'+name+'_0_13TeV__invMass_combined_asymptoticCLs.out',
        'CMS_jj_'+name+'_0_13TeV__invMass_combined_MaxLikelihoodFit.out',
        'higgsCombine'+name+'0_invMass_combined.MaxLikelihoodFit.mH0.root',
        name+'*.error',
        signal+'*.log',
        name+'*.out',
        signal+'*.submit',
        signal+'*.resubmit',
        # workspaces:
        'workspaces/CMS_jj_bkg_VV_'+name+'_0_13TeV.root',
        'workspaces/CMS_jj_'+name+'_0_13TeV.root',
        # plots:
        'plots/backgrounds_log_'+name+'.pdf',
        'plots/backgrounds_'+name+'.pdf',
        # 'plots/both_pretty.pdf',
        # 'plots/ch1_mgg13TeV_fit_b.png',
        # 'plots/ch1_mgg13TeV_fit_s.png',
        # 'plots/ch1_mgg13TeV_prefit.png',
        # 'plots/ch2_mgg13TeV_fit_b.png',
        # 'plots/ch2_mgg13TeV_fit_s.png',
        # 'plots/ch2_mgg13TeV_prefit.png',
        # 'plots/covariance_fit_b.png',
        # 'plots/covariance_fit_s.png',
        'plots/'+name,
        # 'plots/fitDiagnostics'+name+'0_invMass_combined.root',
        'plots/sigmodel_'+name+'0__invMass_afterVBFsel.pdf',
        'plots/sigmodel_'+name+'0__invMass_afterVBFsel.root',
        'plots/sigmodel_'+name+'0__invMass.pdf',
        'plots/sigmodel_'+name+'0__invMass.root',
        # MiniTrees:
        'MiniTrees/DataUHH/dijetUHH_13TeV_miniTree_'+name+'.root',
        'MiniTrees/SignalUHH/dijetUHH_13TeV_'+name+'_miniTree.root',
        # datacards:
        'datacards/CMS_jj_'+name+'_0_13TeV__invMass_afterVBFsel.txt',
        'datacards/CMS_jj_'+name+'_0_13TeV__invMass_combined_limit1_submit.src',
        'datacards/CMS_jj_'+name+'_0_13TeV__invMass_combined.txt',
        'datacards/CMS_jj_'+name+'_0_13TeV__invMass.txt',
    ]

    limitdir_files=[
        # Limits:
        signal+'*.submit',
        signal.split('_')[0]+'*.submit',
        signal+'*.error',
        signal+'*.out',
        signal+'*.log',
        'Limits/CMS_jj_0_'+signal+'*_13TeV__invMass_combined_asymptoticCLs_new.root',
        'Limits/'+signal+'__invMass_combined_new_combined_limits.csv',
        'Limits/brazilianFlag_'+signal+'__invMass_combined_new_combined_13TeV.C',
        'Limits/brazilianFlag_'+signal+'__invMass_combined_new_combined_13TeV.pdf',
    ]
    
    
    basedir_command='mv'
    limitdir_command ='mv'
    # basedir_command='cp -rf'
    # limitdir_command='cp -rf'
    for item in basedir_files:
        basedir_command+=' '+item
    basedir_command+=' '+backup_dir
    for item in limitdir_files:
        limitdir_command+=' '+item
    limitdir_command+=' '+backup_dir
    if(mode=='fit'):
        print basedir_command
        os.system(basedir_command)
    elif(mode=='plot'):
        plot_move_command='cp Limits/brazilianFlag_'+signal+'__invMass_combined_new_combined_13TeV.pdf /afs/desy.de/user/a/albrechs/aQGCVVjj/LimitPlots/'
        print plot_move_command
        os.system(plot_move_command)
        print limitdir_command
        os.system(limitdir_command)
    else:
        print 'Please select BackupMode'
    
def backup(move=False,tar=True):
    backup_dir=strftime("%m_%d_%H_%M_%S",gmtime())
    backup_path='backup/'+backup_dir+'/'
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)    
        print 'created dir:',backup_path
    basedir_files=[#'*.out',
                  '*.root',
                  '*.o*',
                  '*.e*',
                  '*.log',
                  'MiniTrees/',
                  'workspaces/',
                  'plots/',
                  'datacards/'
    ]
    limitdir_files=['Limits/*asymptoticCLs_new.root',
                    'Limits/*_new_combined_13TeV.pdf',
                    'Limits/*_new_combined_13TeV.C',
                    'Limits/*.csv'
    ]

    # limits_files=glob.glob('Limits/*_asymptoticCLs_new.root')
    # for file in glob.glob('Limits/*_new_combined_13TeV.C'):
    #     limits_files.append(file)
    # for file in glob.glob('Limits/*_new_combined_13TeV.pdf'):
    #     limits_files.append(file)

    
    if(move):
        basedir_command='mv'
        limitdir_command ='mv'
    else:
        basedir_command='cp -rf'
        limitdir_command='cp -rf'
    
    for item in basedir_files:
        basedir_command+=' '+item

    for item in limitdir_files:
         limitdir_command+=' '+item

    basedir_command+=' '+backup_path
    print 'basedir_command',basedir_command

    limitdir_command+=' '+backup_path
    print 'limitdir_command',limitdir_command

    os.system(basedir_command)
    os.system(limitdir_command)
    
    print 'moved files to backup_dir'
    os.chdir('backup')
    if(tar):
        make_tarfile(backup_dir+'.tar.gz',backup_dir)
        os.system('rm -rf '+backup_dir)
    os.chdir('../')

    directories=['MiniTrees/SignalUHH','MiniTrees/DataUHH','workspaces','plots','datacards']
    for dir in directories:
        if not os.path.exists(dir):
            os.makedirs(dir)


if(__name__=='__main__'):

    # backup(True,False)
    backup_point('VV_M7','m8p00','plot')
    
