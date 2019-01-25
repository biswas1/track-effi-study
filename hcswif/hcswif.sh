#!/usr/bin/bash
ARGC=$#
if [[ $ARGC -ne 4 ]]; then
    echo Usage: hcswif.sh SCRIPT RUN EVENTS PARAM
    exit 1
fi;
script=$1
run=$2
evt=$3
param=$4

# Setup environment
hcswif_dir=$(dirname $(readlink -f $0))
source $hcswif_dir/setup.sh

# Check environment
if ! [ $(command -v hcana) ]; then
    echo Could not find hcana! Please edit $hcswif_dir/setup.sh appropriately
    exit 1
fi

# Replay the run
runHcana="./hcana -q \"$script($run,$evt,$param)\""
cd $hallc_replay_dir
echo pwd: $(pwd)
echo $runHcana
eval $runHcana
