'''
Created on 01.12.2015

@author: markusfasel
'''

import getopt, os, sys
import shutil

if __name__ == "__main__":
    sys.path.append(os.path.dirname(sys.argv[0]))

from train.steer.tools import GetWorkdir, SubmitBatch, FindList, GetLists
from train.steer.config import ConfigHandler
from train.steer.runAnalysis import runAnalysis

def Usage():
    print "Usage: ./run.py [MODE] [OPITONS]"
    print ""
    print "  Modes:"
    print "    train: Run the full train"
    print "    local: Run local tests"
    print "    merge: Merge output from a given train run"
    print " "
    print "  Options:"
    print "    -u|--user: Run for a special user"
    print "    -l|--list: Run on a special file list"
    print "    -s|--splitlevel: Number of files per job"
    print "    -n|--nchunk: Number of chunks"
    print "    -m|--minchunk: Minimum chunk (local running mode)"
    print "    -i|--inputdir: Inputdir (for merging)"
    print "    -f|--filename: Filename: (for merging)"
    print "    -h|--help: Print help"
    

def main(argc, argv):
    
    modes = ["train", "batch", "local", "merge"]
    mode = argv[1]
    if not mode in modes:
        Usage()
        sys.exit(1)

    opt, arg = getopt.getopt(argv, "u:c:l:s:n:i:f:h", ["user=", "configuration=", "list=", "splitlevel=" , "nchunk=" "inputdir=", "filename=", "help"]) 
    
    userdir = "all"
    filelist=""
    inputdir=""
    splitlevel=-1
    config = ""
    filename = ""
    nchunk = -1
    filemin = 0
    for o,a in opt:
        if o in ("-u", "--user"):
            userdir = str(a)
        elif o in ("-c", "--config"):
            config = str(a)
        elif o in ("-l", "--list"):
            filelist = str(a)
        elif o in ("-i", "--input"):
            inputdir = str(a)
        elif o in ("-f", "--filename"):
            filename = str(a)
        elif o in ("-s", "--splitlevel"):
            splitlevel = int(a)
        elif o in ("-n", "--nchunck"):
            nchunk = int(a)
        elif o in ("-h", "--help"):
            Usage()
            sys.exit(1)
    
    if not config:
        print "Config not specified. Please specify either PbPb, pPb, pp or the corresponding MC"
        sys.exit(1)
        
    ConfigHandler.LoadConfiguration(config)
    
    if splitlevel < 0:
        splitlevel = ConfigHandler.GetConfig().GetSplitLevel()

    if mode in modes[0:1]:
        # prepare job submission
        workdir = GetWorkdir(True if mode == "train" else False)
        if len(filelist): # run over one file
            if FindList(FindList):
                # create outputdir and copy train_root to that localtion
                os.makedirs(workdir, 0755)
                jobtrainroot = os.path.join(workdir, "TRAIN")
                shutil.copy(ConfigHandler.GetTrainRoot(), jobtrainroot)
                tags = filelist.split("/")
                outputdir = workdir
                for tag in tags:
                    if tag == config:
                        continue
                    if ".txt" in tag:
                        break
                    outputdir = os.path.join(outputdir, tag)
                os.makedirs(outputdir, 0755)
                SubmitBatch(outputdir, jobtrainroot, filelist, splitlevel, nchunk, userdir)
            else:
                print "List %s not found in your TRAIN_ROOT installation"
        else:
            os.makedirs(workdir, 0755)
            jobtrainroot = os.path.join(workdir, "TRAIN")
            shutil.copy(ConfigHandler.GetTrainRoot(), jobtrainroot)
            
            # run over all files
            filelists = GetLists(config)
            for myfilelist in filelists:
                tags = myfilelist.split("/")
                outputdir = workdir
                for tag in tags:
                    if ".txt" in tag:
                        break
                    outputdir = os.path.join(outputdir, tag)
                os.makedirs(outputdir, 0755)
                SubmitBatch(outputdir, jobtrainroot, myfilelist, splitlevel, nchunk, userdir)
    elif mode == "merge":
        pass
    elif mode == "local":
        if not os.environ["ALICE_PHYSICS"]:
            os.system("source %s/train/config/env" %(ConfigHandler.GetTrainRoot()))
        runAnalysis(userdir, config, filelist, filemin, filemin+nchunk)    
                

if __name__ == '__main__':
    ConfigHandler.SetTrainRoot(os.path.dirname(os.path.abspath(sys.argv[0])))
    main(len(sys.argv), sys.argv)