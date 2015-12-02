#! /bin/bash

TRAIN_ROOT=$1
OUTPUT=$2
MACRO=$3

starttime=$(date +%s)
outputdir=$(printf "%s/job%d" $OUTPUT $SGE_TASK_ID)
cd $outputdir
echo $PWD

source $TRAIN_ROOT/train/config/env

cmd=$(printf "root -b -q \'%s(\"files.txt\")\' &> analysis.log" $MACRO)
echo $cmd
eval $cmd 
endtime=$(date +%s)
jobtime=$(echo "$endtime-$starttime" | bc)
echo Done after $jobtime sec
