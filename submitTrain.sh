#! /bin/bash

function showHelp()
{
        echo "Usage: ./submitTrain.sh OUTPUTDIR VERSION MACRO [OPTIONs]"
        echo ""
        echo "Options:"
        echo " -t: Run test mode (only one job per sample)"
        echo " -n: Number of files per chunk"
        echo " -h: Show help"
}


OUTDIR=$1
VERSION=$2
MACRO=$3
TESTMODE=0
SPLITLEVEL=100

OPTIND=1
while getopts "n:th" opt; do
        echo $opt
        case "$opt" in
        h|?)
                echo Help called
                showHelp
                exit 0
                ;;
        t)
                echo Testmode called
                TESTMODE=1
                ;;
        n)
                SPLITLEVEL=$OPTARG
                ;;
        esac
done

if [ $# -lt 4 ]; then
        showHelp
        exit 1
fi

FILENAME=`readlink -f $0`
TRAIN_ROOT=`dirname $FILENAME`

filelistdir=$TRAIN_ROOT/filelists
filelists=($(ls -1 $filelistdir))
for f in ${filelists[@]}; do
        echo Submitting $f
        filebase=`echo $f | cut -d '.' -f1`
        RUNSTRING=`echo $filebase | cut -d '_' -f2`
        command=$(printf "python %s/steer/submit.py -i %s/%s -o %s/%s/%s -m %s -n %d" $TRAIN_ROOT $filelistdir $f $OUTDIR $VERSION $RUNSTRING $MACRO $SPLITLEVEL)
        if [ $TESTMODE -gt 0 ]; then
                command=$(printf "%s -t" "$command")
        fi
        eval $command
done
