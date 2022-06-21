#!/bin/bash

# check parameter
if [ $# -ne 1 ]; then
	echo "Usage: $0 hostlist"
	exit -1
fi

hostlist=$1
ansible -i ${hostlist} all -s -m copy -a "src=../ceph_ops dest=/root/"
ansible -i ${hostlist} all -s -m shell -a "chmod 755 /root/ceph_ops/get_last_key.sh"
