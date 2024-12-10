#!/bin/bash
for e in `cat idList`
do
    echo Downloading : https://youtu.be/$e
    ./addToSorted.sh https://youtu.be/$e
done