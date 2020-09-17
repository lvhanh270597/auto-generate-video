#!/bin/bash
inputFile=$1
exiftool $inputFile | grep Duration | head -n1 | awk '{print $3}'