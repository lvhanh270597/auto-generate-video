#!/bin/bash

inputFile=$1
tmpFile1=${1}.tmp1.mp4
tmpFile2=${1}.tmp2.mp4
outputFile=$2
trashDirectory=$3
width=720; height=1280

length=`exiftool $inputFile | grep Duration | head -n1 | awk '{print $3}'`
length=`./convert.py $length`
if [[ -f $tmpFile1 ]]; then /bin/rm -rf $tmpFile1; fi
if [[ -f $tmpFile2 ]]; then /bin/rm -rf $tmpFile2; fi
ffmpeg -ss 00:00:00 -i $inputFile -t $length -vcodec copy -acodec copy $tmpFile1 > /dev/null
ffmpeg -i $tmpFile1 -vf scale=$width:$height -c:a copy $tmpFile2
ffmpeg -i $tmpFile2 > info.txt 2>&1
/bin/rm -rf $tmpFile1
output=`./getSAR.py info.txt`
if [[ $? -eq 0 ]]; then
    if [[ $output == "1:1" ]]; then 
        if [[ -f $outputFile ]]; then /bin/rm -rf $outputFile; fi
        /bin/mv $tmpFile2 $outputFile
    else 
        /bin/mv $tmpFile2 $trashDirectory
        exit 1
    fi
else 
    /bin/mv $tmpFile2 $trashDirectory/
    exit 1
fi