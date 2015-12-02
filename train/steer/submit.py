import os
from train.steer.config import ConfigHandler
    
class Submitter():
    
    def __init__(self, inputlist, outputdir, splitlevel, macro):
        self.__inputlist = inputlist
        self.__outputdir = outputdir
        self.__nchunk = -1
        self.__splitlevel = splitlevel
        self.__macro = macro
        
    def SetNchunk(self, nchunk):
        self.__nchunk = nchunk
    
    def Submit(self):
        jobs = self.Split()
        qsub = "qsub -l \"projectio=1,h_vmem=4G\" -t 1:%d" %jobs
        qsub += " " + self.__GetLogging()
        qsub += " " + self.__GetExecutable()
        os.system(qsub)
        
    def __GetExecutable(self):
        return "%s %s %s %s" %(os.path.join(self.__data.GetTrainRoot(), "steer", "jobscript.sh"), ConfigHandler.GetTrainRoot(), self.__outputdir, self.__macro)
    
    def __GetLogging(self):
        return "-j y -o %s/job\$TASK_ID/joboutput.log" %self.__outputdir
        
    def Split(self):
        chunk = 1
        chunkfile = 0 
        outputpath = os.path.join(self, self.__outputdir, "job%d" %chunk)
        os.makedirs(outputpath, 0755)
        outputfile = os.path.join(outputpath, "files.txt")
        reader = open(self.__inputlist, 'r')
        writer = open(outputfile, 'w')
        for line in reader:
            writer.write(line)
            chunkfile += 1
            if chunkfile >= self.__splitlevel:
                writer.close()
                chunk += 1
                if self.__nchunk > -1 and chunk >= self.__nchunk:
                    # Stop in case we exceeded the number of chunks requested
                    reader.close()
                    writer = None
                    reader = None
                    break
                outputpath = os.path.join(self.__outputdir, "job%d" %chunk)
                os.makedirs(outputpath, 0755)
                outputfile = os.path.join(outputpath, "files.txt")
                writer = open(outputfile, 'w')
                chunkfile = 0
        if reader:
            reader.close()
        if writer:
            writer.close()
        return chunk
