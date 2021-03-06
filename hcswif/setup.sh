#!/usr/bin/bash

# -----------------------------------------------------------------------------
#  Change these if this if not where hallc_replay and hcana live
export hcana_dir=/w/hallc-scifs17exp/xem2/$USER/hcana
export hallc_replay_dir=/w/hallc-scifs17exp/xem2/$USER/fallback-replay/hallc-replay-f2xem

# -----------------------------------------------------------------------------
#  Change if this gives you the wrong version of root, evio, etc
source /site/12gev_phys/production.sh 2.1

# -----------------------------------------------------------------------------
# Source setup scripts
curdir=`pwd`
cd $hcana_dir
source setup.sh
export PATH=$hcana_dir/bin:$PATH
echo Sourced $hcana_dir/setup.sh

cd $hallc_replay_dir
source setup.sh
echo Sourced $hallc_replay_dir/setup.sh

echo cd back to $curdir
cd $curdir

