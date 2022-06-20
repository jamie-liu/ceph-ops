#! /bin/bash

pool=$1
image=$2
snap=$3

if [ $# -lt 2 ] || [ $# -gt 3 ]; then
    echo "Example: $0 <pool-name> <image-name>"
    echo "         $0 <pool-name> <image-name> [snap-name]   # --from-snap"
    exit 1
fi

if [ $# -eq 2 ]; then
    rbd diff -p $pool $image | awk '{ SUM += $2 } END { print SUM/1024/1024 " MB" }'
else
    rbd diff -p $pool $image --from-snap $snap | awk '{ SUM += $2 } END { print SUM/1024/1024 " MB" }'
fi

