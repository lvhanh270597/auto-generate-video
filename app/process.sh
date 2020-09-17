#!/bin/bash
videoPath=$1; outputFile=$2; 
echo 'cacascsac'
echo $videoPath
echo 'ascascsacsacsa'
files=""; count=0;
for item in `ls $videoPath`; do
    files="$files -i $videoPath/$item "
    count=$((count+1))
done
echo -ne $files > xx.txt
ffmpeg $files -filter_complex "[0:v][0:a][1:v][1:a]concat=n=$count:v=1:a=1" $outputFile.sound.mp4
ffmpeg -i $outputFile.sound.mp4 -c copy -an $outputFile