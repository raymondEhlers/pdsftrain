#! /bin/bash

SCRIPTNAME=`readlink -f $0`
TRAINBASE=`dirname $SCRIPTNAME`
outputbase=$1
filename=AnalysisResults.root
SPLITLEVEL=

OPTIND=1
while getopts "f:n:" opt: do
        case "$opt" in
        h|?)
                show_help
                exit 0
                ;;
        n)
                SPLITLEVEL=$OPTARG
                ;;
        f)
                filename=$OPTARG
                ;;
        esac
done


runs=($(ls -1 $outputbase))
for r in ${runs[@]}; do
        echo Merging $r
        inputdir=$outputbase/$r
        cmd=$(printf "qsub -l projectio=1 -o %s/merge.log -j y %s/mergescript.sh %s %s" $inputdir $trainbase $inputdir $filename)
        if [ "x$SPLITLEVEL" != "x" ]; then
                cmd=$(printf "%s %d" "$cmd" $SPLITLEVEL)
        fi
        echo "Submitting $cmd"
        eval $cmd
done
