#!/bin/bash

size=$#;
args=$@;
i=0
prefix=
while [ $i -lt $size ]
do 
    echo $i, $1
    if [ $1 = "--prefix" ]; then 
        shift 1;
        prefix=$1;
        echo "prefix set to " $1
        i=$((i+1))
    else 
        shift 1;
    fi 
    i=$((i+1))
done 

echo "Do you want to continue?[Y/n]"

read opt

if [ $opt = "n" ] || [ $opt = "N" ]; then
    clear;
    exit 0;
fi  
