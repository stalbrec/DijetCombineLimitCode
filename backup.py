import os,glob,tarfile,sys
from time import gmtime, strftime
sys.path.append('/afs/desy.de/user/a/albrechs/aQGCVVjj/python')
import PointName as PN

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    tar.close()



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

    backup(True,False)

    
