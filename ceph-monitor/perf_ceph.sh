#!/bin/bash

cd /root/ceph_ops && python ./perf_dump_osd.py
cd /root/ceph_ops && python ./perf_dump_mon.py
cd /root/ceph_ops && python ./perf_dump_rgw.py

cat /etc/ceph/osd_dump > /etc/ceph/perf
cat /etc/ceph/mon_dump >> /etc/ceph/perf
cat /etc/ceph/rgw_dump >> /etc/ceph/perf
