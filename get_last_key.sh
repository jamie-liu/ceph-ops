#!/bin/bash

# check parameter
if [ $# -ne 2 ]; then
	echo "Usage: $0 filename key"
	exit -1
fi

filename=$1
key=$2

if [ ! -e ${filename} ]; then
	echo 0
	exit
fi

value=`grep -w "${key}" ${filename} | awk '{ print $2 }'`
if [ -z ${value} ]; then
	echo 0
	exit
fi

echo ${value}
