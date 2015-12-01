#! /usr/bin/env python
import os, sys, getopt

def Split(filelist, outputdir, nfiles, testmode):
  chunk = 1
  chunkfile = 0
  outputpath = os.path.join(outputdir, "job%d" %chunk)
  os.makedirs(outputpath, 0755)
  outputfile = os.path.join(outputpath, "files.txt")
  reader = open(filelist, 'r')
  writer = open(outputfile, 'w')
  for line in reader:
    writer.write(line)
    chunkfile += 1
    if chunkfile >= nfiles:
      writer.close()
      chunk += 1
      if testmode:
         reader.close()
         writer = None
         reader = None
         break
      outputpath = os.path.join(outputdir, "job%d" %chunk)
      os.makedirs(outputpath, 0755)
      outputfile = os.path.join(outputpath, "files.txt")
      writer = open(outputfile, 'w')
      chunkfile = 0
  if reader:
    reader.close()
  if writer:
    writer.close()
  return chunk

def main(argc, argv):
  basepath = os.path.dirname(argv[0])
  inputfilelist = ""
  macro = ""
  outputdir = ""
  splitlevel = 0
  testmode=False
  
  opt,arg = getopt.getopt(argv[1:], "i:o:n:m:t", ["input=", "output=", "nfiles=", "macro=", "test"])
  for o, a in opt:
    if o in ("-i", "--input"):
      inputfilelist = str(a)
    elif o in ("-o", "--output"):
      outputdir = str(a)
    elif o in ("-n", "--nfiles"):
      splitlevel = int(a)
    elif o in ("-m", "--macro"):
      macro = str(a)
    elif o in ("-t", "--test"):
      testmode=True
      
  print "Inputfilelist: %s" %inputfilelist
  print "Outputdir: %s" %outputdir
  print "Macro: %s" %macro
  print "Splitlevel: %d" %splitlevel
  
  if not len(inputfilelist) or not len(outputdir) or not len(macro) or splitlevel == 0:
    print "Cannot submit job"
    sys.exit(1)
    
  jobs = Split(inputfilelist, outputdir, splitlevel, testmode)
  qsub = "qsub -l \"projectio=1,h_vmem=4G\" -t 1:%d -j y -o %s/job\$TASK_ID/joboutput.log %s/jobscript.sh %s %s" %(jobs, outputdir, basepath, outputdir, macro)
  os.system(qsub)

if __name__ == "__main__":
  main(len(sys.argv), sys.argv)
