#! /usr/bin/env python

import os, sys, getopt, getpass, shutil

def recursive_merge(intputlist, splitlevel, outputfilename, workdir):
        result = []
        outputfilebase = outputfilename.split(".")[0]
        nbucket = 0
        nchunk = 0
        bucketfilename = os.path.join(workdir, "%s_%d.root" %(outputfilebase, nchunck))
        cmd = "hadd -f %s" %bucketfilename 
        for line in inputlist:
                cmd += " %s" %line 
                nbucket += 1
                if nbucket >= splitlevel:
                        print "Merging bunch %d" %nchunk
                        os.system(cmd)
                        result.append(bucketfilename)

                        #prepare next
                        nbucket=0
                        nchunk += 1
                        bucketfilename = os.path.join(workdir, "%s_%d.root" %(outputfilebase, nchunck))
                        cmd = "hadd -f %s" %bucketfilename 

        # Merge last bunch
        if nbucket:
                os.system(cmd)
                result.append(bucketfilename)
        return result

def read_input_files(filename):
        result=[]
        reader = open(inputlist, "r")
        for line in reader:
                tmp = line.split("\n")[0].lstrip().rstrip()
                if not len(tmp):
                        continue
                result.append(tmp)
        reader.close()
        return result

def main(argc, argv):
        filelist = argv[1]
        outputdir = argv[2]
        workdirbase = argv[3]
        splitlevel=10
        filename=None

        # check ingredients
        if not filelist:
                print "Input filelist missing"
                sys.exit(1)
        if not outputdir:
                print "Output directory missing"
                sys.exit(1)
        if not workdirbase:
                print "Working directory missing"
                sys.exit(1)

        opt,arg = getopt.getopt(argv[4:], ":n:f", ["nfiles=", "filename="])
        for o,a in opt:
                if o in ("-n", "--nfiles"):
                        splitlevel=int(a)
                elif o in ("-f", "--filename"):
                        filename=str(a)

        currentdir = os.getcwd()
        if not os.path.exists(workdirbase)
        os.chdir(workdirbase)

        iteration = 0
        workdir_source = None
        workdir_target = None
        filelist = read_input_files(filelist)
        if not filename:
                # determin filename from the merge input
                filename = os.path.basename(filelist[0])
        isDone = True if len(filelist) <= 1 else False
        while not isDone:
                if workdir_source:
                        shutil.rmtree(workdir_source)
                if workdir_target:
                        workdir_source = workdir_target
                workdir_target = os.path.join(workdirbase, "iteration_%d" %iteration)
                os.makedirs(workdir_target, 0744)
                filelist = recursive_merge(filelist, splitlevel, filename, workdir_target)
                # prepare next recursion step
                iteration += 1
                isDone = True if len(filelist) <= 1 else False

        # Move output to its destination
        shutil.copy(os.path.join(workdir_target, filelist[0]) os.path.join(outputdir, filename))
        shutil.rmtree(workdirbase)
        os.chdir(currentdir)

if __name__ == "__main__":
        main(sys.argc, sys.argv)
