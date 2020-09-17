#!/bin/bash

audioPath=$1
audioLength=$2
outputFile=$3
line=`ls $audioPath | wc -l`
randomNumber=$((RANDOM%line))
audioFile=$audioPath/`ls $audioPath | head -n $randomNumber | tail -n1`
length=`exiftool $audioFile | grep Duration | head -n1 | awk '{print $3}'`
seconds=$(echo $length | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }')
randomStart=$((RANDOM%seconds))

