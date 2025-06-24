#!/bin/bash

export inputFiles=$1
export outputFolder=$2
export maxevents=$3
export chunk=$4

echo "parsing inputfiles as: $inputFiles"
cd /work/pahwagne/gen/CMSSW_10_6_37/src/rds/gen/
#scramv1 runtime -sh
cmsenv
for file in $inputFiles; do
  echo "printMiniAODContent.py --inputFiles $file --outputFolder=$outputFolder --maxevents=$maxevents"
  python printMiniAODContent.py --inputFiles "$file" --outputFolder=$outputFolder --maxevents=$maxevents --chunk=$chunk 
done



