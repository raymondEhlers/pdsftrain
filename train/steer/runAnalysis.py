'''
Created on 04.12.2015

@author: markusfasel
'''
import os, sys
import json
import ROOT
from train.steer.config import ConfigHandler

if __name__ == "__main__":
    sys.path.append(os.environ["TRAIN_ROOT"])
    
def ReadJSON(filename):
    result = ""
    reader = open(filename, "R")
    for line in reader:
        myline = line.replace("\n").lstrip().rstrip()
        result += myline
    reader.close()
    return result

def ProcessUser(username):
    userdir = os.path.join(ConfigHandler.GetTrainRoot(), username)
    userconfig = os.path.join(userdir, "config.json")
    configs = json.loads(ReadJSON(userconfig))
    for myconf, tasks in configs.iteritems():
        if myconf == ConfigHandler.GetConfig().GetName():
            for task in tasks:
                for k,v in task.iteritems():
                    if k == "MACRO":
                        ROOT.gROOT.Macro("%s/%s", os.environ["TRAIN_ROOT"], username, v)

def CreateChain(filelist, treename):
    chain = ROOT.TChain(treename, "")
    for myfile in filelist:
        chain.AddFile(myfile)
    return chain

def CreateAnalysisManager():
    mgr = ROOT.AnalysisManager("MGR")
    mgr.SetCommonFileName("AnalysisResults.root")
    return mgr

def CreateHandlers():
    for hadler in ConfigHandler.GetConfig().GetHandlers():
        ROOT.gROOT.Macro(hadler)

def ReadFileList(inputfile, mymin, mymax):
    result = []
    reader = open(inputfile)
    counter = 0
    for line in reader:
        newline = line.replace("\n", "").lstrip().rstrip()
        if not len(line):
            continue
        if min > 0 and counter < mymin:
            counter += 1
            continue
        if max > 0 and counter >= max:
            break
        result.append(newline)
        counter += 1
    reader.close()
    return result

def runAnalysis(user, config, filelist, filemin, filemax):
    ConfigHandler.SetTrainRoot(os.environ["TRAIN_ROOT"])
    ConfigHandler.LoadConfiguration(config)
    
    # Load additional libraries
    ROOT.gROOT.Macro("%s/steer/macros/LoadLibs.C")
    
    mgr = CreateAnalysisManager()
    CreateHandlers()
    
    ProcessUser("basics")
    if user != "all":
        print "Adding user %s" %user
        ProcessUser(user)
    else:
        userreader = open(os.path.join(ConfigHandler.GetTrainRoot(), "config", "user"), "R")
        for tmpuser in userreader:
            myuser = tmpuser.replace("\n", "").lstrip().rstrip()
            if(myuser[0] == "#"):
                continue
            print "Adding user %s" %myuser
            ProcessUser(myuser)
        userreader.close()
        
    files = ReadFileList(filelist, filemin, filemax)
    if not len(files):
        print "No files found to analyze"
        return
    if mgr.InitAnalysis():
        mgr.StartAnalysis("local", CreateChain(files, "esdTree"))

if __name__ == "__main__":
    runAnalysis(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])