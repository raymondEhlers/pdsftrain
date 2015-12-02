'''
Created on 01.12.2015

@author: markusfasel
'''

import os, time
from train.steer.config import ConfigHandler
from train.steer.submit import Submitter

def GetTag():
    config = ConfigHandler.GetConfig()
    return "%s%s_%s" %(config.GetVersion(), config.GetName(), time.strftime("%y%m%d_%H%M%S", time.localtime()));

def FindList(listname):
    dirs = listname.split("/")
    currentdir = ConfigHandler.GetTrainRoot()
    hasfound = False
    for mydir in dirs:
        content = os.listdir(currentdir)
        if not len(content):
            break
        if mydir in content:
            currentdir = os.path.join(currentdir, mydir)
            if os.path.isfile(currentdir): 
                hasfound = True
                break
    return hasfound

def FindFiles(inputdir):
    result = []
    mypath, mydirs, myfiles = os.walk(inputdir)
    for f in myfiles:
        result.append(os.path.join(mypath, f))
    for d in mydirs:
        found = FindFiles(os.path.join(mypath, d))
        for f in found:
            result.append(f)
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
