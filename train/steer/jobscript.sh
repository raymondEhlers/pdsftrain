#! /bin/bash

TRAIN_ROOT=$1
OUTPUT=$2
USER=$3
FILELIST=$4
NFILES=$5

counter=$(echo "$SGE_TASK_ID - 1 | bc")
MIN=$("echo $SGE_TASK_ID * $NFILES | bc")
MAX=$("echo ($SGE_TASK_ID+1) * $NFILES | bc")

starttime=$(date +%s)
outputdir=$(printf "%s/job%d" $OUTPUT $SGE_TASK_ID)
cd $outputdir
echo $PWD

source $TRAIN_ROOT/train/config/env

export TRAIN_ROOT=$TRAIN_ROOT
cmd=$(printf "python %s/train/steer/runAnalysis.py %s %s %s %s &> analysis.log" $TRAIN_ROOT $USER $FILELIST $MIN $MAX)
echo $cmd
eval $cmd 
endtime=$(date +%s)
jobtime=$(echo "$endtime-$starttime" | bc)
echo Done after $jobtime sec
