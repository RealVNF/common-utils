#!/bin/bash

# reads the network_files.txt, service_files.txt, and config_files.txt line by line
# runs multiple simultaneous instances of Simulator
# run from project root! (where Readme is)

networks='scripts/network_files.txt'
service_functions='scripts/service_files.txt'
configs='scripts/config_files.txt'
# (un)comment the Algorithm you want to use
#algo='rs'
#algo='lb'
algo='sp'

printf "\n\n-----------------------Running Non-RL Algo-------------------------\n\n"
  
paste $networks $service_functions $configs | while IFS="$(printf '\t')" read -r f1 f2 f3
do
  $algo -n $f1 -sf $f2 -c $f3 -i 200
done

printf "\n\n---------------------Finished running Non-RL Algo-------------------\n\n"