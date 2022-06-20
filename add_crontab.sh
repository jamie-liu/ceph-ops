#!/bin/bash

# check parameter
if [ $# -ne 1 ]; then
	echo "Usage: $0 hostlist"
	exit -1
fi
hostlist=$1

ansible -i ${hostlist} all -s -m shell -a "cd /root/ceph_ops && sh local_add_crontab.sh"
echo "Done add crontab!"
exit 0
