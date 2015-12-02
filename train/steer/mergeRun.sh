#! /bin/bash

SCRIPTNAME=`readlink -f $0`
TRAINBASE=`dirname $SCRIPTNAME`
outputbase=$1

currentdir=`pwd`
cd $outputbase
runs=($(ls -1))
for r in ${runs[@]}; do
        echo Merging $r
        cd $outputbase/$r
        mergefilelist=`pwd`/filestomerge.txt
        find `pwd` -name AnalysisResults.root >> $mergefilelist
        $TRAINBASE/merge.sh $mergefilelist
done
cd $currentdir
