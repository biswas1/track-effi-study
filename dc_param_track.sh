#!/usr/bin/bash


#source /apps/root/6.10.02/setroot_CUE.sh

#max_chi=4000000.


#while true; do
#   echo " $j "
#   ((j++))
#   max_chi=`expr "$j * 100"` # ` run the command and return the result `
#   echo " $max_chi " 
#   if ($j>=2) break
#done

for i in `seq 1 5`;
do 
    #echo $i
#    max_chi=$(($i * 1000))
#    echo "$max_chi"

#    xstub=$(($i * 10))
#    echo "$xstub"

#    ystub=$(($i * 10))
#    echo "$ystub"  
    
#    ypstub=$(($i * 0.1 )) 
#    echo "$ypstub"
       
    xstub=$(bc <<< "scale=2;$i*10.0" )
    echo "$xstub"


#    x= 1.1 + i | bc  
#    echo"$x"    


   cd /w/hallc-scifs17exp/xem2/biswas/fallback-replay/hallc-replay-f2xem/
#  for the chisq criteria  
#   sed -i "40s/.*/psel_chi2_fpperdegmax = $max_chi/" /w/hallc-scifs17exp/xem2/biswas/fallback-replay/hallc-replay-f2xem/PARAM/SHMS/GEN/ptracking.param  
#  for the X stub criteria 
#   sed -i "27s/.*/pxt_track_criterion = $xstub/" /w/hallc-scifs17exp/xem2/biswas/fallback-replay/hallc-replay-f2xem/PARAM/SHMS/GEN/ptracking.param
# for the Y stub criteria 
#   sed -i "28s/.*/pyt_track_criterion = $ystub/" /w/hallc-scifs17exp/xem2/biswas/fallback-replay/hallc-replay-f2xem/PARAM/SHMS/GEN/ptracking.param

sed -i "27s/.*/pxt_track_criterion = $xstub/" /w/hallc-scifs17exp/xem2/biswas/fallback-replay/hallc-replay-f2xem/PARAM/SHMS/GEN/ptracking.param

#sed -i "/*  hsel_chi2_fpperdegmax =*/  chsel_chi2_fpperdegmax = ${max_chi}" ../hallc-replay-f2xem/PARAM/SHMS/GEN/htracking.param

   cd /w/hallc-scifs17exp/xem2/biswas/hcana/
    
   source setup.sh
    
   cd /w/hallc-scifs17exp/xem2/biswas/fallback-replay/hallc-replay-f2xem/
    
   source setup.sh 
     
   ./hcana -q  "SCRIPTS/SHMS/PRODUCTION/replay_production_all_shms.C(2548,100000)" 
    
   
   cd /lustre/expphy/volatile/hallc/xem2/biswas/ROOTfiles
   mv shms_replay_production_all_2548_100000.root shms_replay_production_all_2548_100000_x_stub_${xstub}.root 
    
   cd /lustre/expphy/volatile/hallc/xem2/biswas/REPORT_OUTPUT/SHMS/PRODUCTION/
   mv summary_all_production_2548_100000.report summary_all_production_2548_100000_x_stub_${xstub}.report
   mv replay_shms_all_production_2548_100000.report replay_shms_all_production_2548_100000_x_stub_${xstub}.report

echo "done"

done 


