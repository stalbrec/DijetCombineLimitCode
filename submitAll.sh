#!/bin/bash

#HTC: condor_submit jobChannelPoint.submit -append "arguments = test1 test2"

# channels=(VV ssWW ZZ)					  
# channels=(VV)						
channels=(ZZ)
# parameters=(T0)
# parameters=(S0 S1)
parameters=(S0 S1 M0 M1 M2 M3 M4 M5 M6 M7 T0 T1 T2 T5 T6 T7 T8 T9)

for ((i=0;i<${#channels[@]};i+=1))
do
  for ((j=0;j<${#parameters[@]};j+=1))
  do
    # qsub -l distro=sld6 -l h_vmem=10G -l h_rt=15:59:59 -cwd -N ${channels[$i]}_${parameters[$j]}_4 submitwrapper.sh ${channels[$i]} ${parameters[$j]}
		condor_submit jobChannelPoint.submit -append "arguments = ${channels[$i]} ${parameters[$j]}" -append "error=${channels[$i]}_${parameters[$j]}.error" -append "output=${channels[$i]}_${parameters[$j]}.out" -append "log=${channels[$i]}_${parameters[$j]}.log"
    # python submitLimits.py ${channels[$i]}_${parameters[$j]}
  done
done
