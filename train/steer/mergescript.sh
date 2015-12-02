#! /bin/bash

SCRIPTNAME=`readlink -f $0`
TRAIN_ROOT=`dirname $SCRIPTNAME`

INPUTDIR=$1
FILENAME=$2
SPLITLEVEL=${3:-10}

WORKDIR=$(printf "%s/merge_tmp" $INPUTDIR)
OUTPUTDIR=$(printf "%s" $INPUTDIR)
if [ -f $WORKDIR ]; then mkdir -p $WORKDIR; fi
FILELIST=$WORKDIR/filestomerge.txt
find $INPUTDIR -name $FILENAME >> $FILELIST

source /usr/share/Modules/init/bash
module use /project/projectdirs/alice/mfasel/modulefiles
module load mfasel/AliPhysics/master

# run actual merging process
python $TRAIN_ROOT/recursive_merge.py $FILELIST $INPUTDIR $WORKDIR -n $SPLITLEVEL -f $FILENAME

# done
if [ -d $WORKDIR ]; then rm -rf $WORKDIR; fi
echo Done
