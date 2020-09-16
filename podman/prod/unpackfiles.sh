#!/bin/bash

while getopts t:o: flag
do
    case "${flag}" in
        t) TARFILE=${OPTARG};;
        o) OUTPUT_DIR=${OPTARG};;
    esac
done


# check for non empty dir 
if [ "$(ls -A $OUTPUT_DIR)" ]; then
    echo "$OUTPUT_DIR is not empty, skipping this tarfile"
    exit
else
    echo "unpacking $TARFILE ..."
    tar -C $OUTPUT_DIR -xf $TARFILE
    echo "finished"
fi
	
