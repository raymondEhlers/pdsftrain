#! /bin/bash

source /usr/share/Modules/init/bash
module use /project/projectdirs/alice/mfasel/modulefiles
module load mfasel/aliroot/master

filelist=$1
outputfile=${2:-AnalysisResults.root}

cmd=$(echo "hadd -f $outputfile")
while read line; do
        cmd=$(printf "%s %s" "$cmd" "$line")
done < $filelist
#echo $cmd
eval $cmd
