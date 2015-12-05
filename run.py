'''
Created on 01.12.2015

@author: markusfasel
'''

import getopt, os, sys
from train.steer.tools import GetWorkdir, SubmitBatch, FindList, GetLists
from train.steer.config import ConfigHandler


if __name__ == "__main__":
    sys.path.append(os.path.dirname(sys.argv[0]))

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
    print "    -m|--macro: Macro to run"
    print "    -i|--inputdir: Inputdir (for merging)"
    print "    -f|--filename: Filename: (for merging)"
    print "    -h|--help: Print help"
    

def main(argc, argv):
    
    modes = ["train", "batch", "local", "merge"]
    mode = argv[1]
    if not mode in modes:
        Usage()
        sys.exit(1)

    opt, arg = getopt.getopt(argv, "u:c:l:s:m:n:i:f:h", ["user=", "configuration=", "list=", "splitlevel=" , "macro=", "nchunk=" "inputdir=", "filename=", "help"]) 
    
    userdir = ""
    filelist=""
    inputdir=""
    splitlevel=-1
    config = ""
    chunks = -1
    macro = ""
    filename = ""
    for o,a in opt:
        if o in ("-u", "--user"):
            userdir = str(a)
        elif o in ("-c", "--config"):
            config = str(a)
        elif o in ("-l", "--list"):
            filelist = str(a)
        elif o in ("-i", "--input"):
            inputdir = str(a)
        elif o in ("-m", "--macro"):
            macro = str(a)
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
                tags = filelist.split("/")
                outputdir = workdir
                for tag in tags:
                    if tag == config:
                        continue
                    if ".txt" in tag:
                        break
                    outputdir = os.path.join(outputdir, tag)
                os.makedirs(outputdir, 0755)
                SubmitBatch(outputdir, filelist, splitlevel, chunks, macro)
        else:
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
                SubmitBatch(outputdir, myfilelist, splitlevel, chunks, macro)
    elif mode == "merge":
        pass
                

if __name__ == '__main__':
    ConfigHandler.SetTrainRoot(os.path.dirname(os.path.abspath(sys.argv[0])))
    main(len(sys.argv), sys.argv)