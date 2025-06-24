#!/bin/bash

export inputFiles=$1
export outputFolder=$2
#export maxevents=$3
#export maxfiles=$4

#if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
#  echo "Warning, not all inputs specified!!"
#fi

maxevents=-1
maxfiles=-1
chunksize=10


mkdir -p /work/pahwagne/gen/CMSSW_10_6_37/src/rds/gen/$outputFolder/logs/
mkdir -p /work/pahwagne/gen/CMSSW_10_6_37/src/rds/gen/$outputFolder/errs/
echo "output folder is $outputFolder" 

#input file is .txt format

#read line by line from input file and restrict to $k files

if [ "$maxfiles" -eq -1 ]; then
  #redirect ALL inputfiles to read
  input_stream=$(cat "$inputFiles")
else
  #redirect only head of $k inputfiles to read
  input_stream=$(head -n "$maxfiles" "$inputFiles")
fi

total_lines=$(echo "$input_stream" | wc -l)

echo "Total lines to process: $total_lines"
echo "Chunk size: $chunksize"

count=0
file_count=0
chunk=0
list=""

echo "$input_stream" | while read -r line; do

  #echo $line
  #remove whitespaces etc from line
  path=$(echo "$line" | sed -E 's/^[[:space:]]*[0-9]+[[:space:]]+//')
  #echo $path

  if [ "$count" -eq 0 ]; then
    #start list with path
    list="$path"
  else
    #append path to chunk
    list="$list $path"
  fi

  #increase counter
  count=$((count + 1))
  file_count=$((file_count + 1))


  if [ "$count" -eq "$chunksize" ]; then
    #list is full
    #list="[$list]"
    #echo $list
    #echo "$list $outputFolder $maxevents"
    chunk=$((chunk+1))
    #echo "sbatch -p short -o ./$outputFolder/logs/chunk_${chunk}.txt -e ./$outputFolder/errs/chunk_${chunk}.txt printMiniAODContent.sh $list $outputFolder $maxevents $chunk"
    sbatch -p short -o ./$outputFolder/logs/chunk_${chunk}.txt -e ./$outputFolder/errs/chunk_${chunk}.txt printMiniAODContent.sh "$list" $outputFolder $maxevents $chunk
    count=0
    list=""
  fi
  #echo $count

  if [ "$file_count" -eq "$total_lines" ] && [ "$count" -ne 0 ] ; then
    #echo "last iteration!"
    #list="[$list]"
    #echo "$list"
    chunk=$((chunk+1))
    #echo "sbatch -p short -o ./$outputFolder/logs/chunk_${chunk}.txt -e ./$outputFolder/errs/chunk_${chunk}.txt printMiniAODContent.sh $list $outputFolder $maxevents $chunk"
    sbatch -p short -o ./$outputFolder/logs/chunk_${chunk}.txt -e ./$outputFolder/errs/chunk_${chunk}.txt printMiniAODContent.sh "$list" $outputFolder $maxevents $chunk
  fi

  #if (( ($file_count % 10) == 0 )); then
  #  echo $file_count
  #  echo "sleep until next submission"
  #  sleep 2
  #fi

done

