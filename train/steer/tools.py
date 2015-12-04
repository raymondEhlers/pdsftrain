'''
Created on 01.12.2015

@author: markusfasel
'''

import os, time
from train.steer.config import ConfigHandler
from train.steer.submit import Submitter
from __builtin__ import True

def GetTag():
    config = ConfigHandler.GetConfig()
    return "%s%s_%s" %(config.GetVersion(), config.GetName(), time.strftime("%y%m%d_%H%M%S", time.localtime()));

def FindList(listname):
    currentdir = ConfigHandler.GetTrainRoot()
    files = FindFiles(os.path.join(currentdir, "filelists"))
    hasfound = False
    for f in files:
        if listname in f:
            hasfound = True
            break
    return hasfound

def FindFiles(inputdir):
    result = []
    for mypath, mydirs, myfiles in os.walk(inputdir):
        for f in myfiles:
            result.append(os.path.join(os.path.abspath(mypath), f))
    return result

def GetLists(mode):
    filelists = []
    trainroot = ConfigHandler.GetTrainRoot()
    currentdir = os.path.join(trainroot, mode)
    found = FindFiles(currentdir)
    # strip away train root
    for f in found:
        test = f.replace(trainroot, "")
        test = test.rstrip().lstrip()
        if test[0] == "/":
            filelists.append(test)
    return filelists
    
def SubmitBatch(outputdir, filelist, splitlevel, chunks, macro):
    submitter = Submitter(filelist, outputdir, splitlevel, macro)
    if chunks >= 0:
        submitter.SetNchunk(chunks)
    submitter.Split()
    submitter.Submit()
        

def GetWorkdir(doGlobal):
    return os.path.join(ConfigHandler.GetConfig().GetTrainOutputPath(doGlobal), GetTag())
