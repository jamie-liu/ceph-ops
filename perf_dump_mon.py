import json
import sys
import os
import commands
from decimal import *

file = open('/etc/ceph/.mon_dump', 'w')

for filename in os.listdir("/var/lib/ceph/mon"):
	mon_id = filename[5:]
	if not mon_id:
		continue

	perf_dump = os.popen("ceph daemon mon.{0} perf dump".format(mon_id))
	data = json.load(perf_dump)


	### messenger throttle policy ###
	#throttle-mon_client_bytes
	val=data['throttle-mon_client_bytes']['val']
	max=data['throttle-mon_client_bytes']['max']
	file.write("{0}.throttle-mon_client_bytes-avail {1:.6f}\n".format(mon_id, max - val))
	avgcount=data['throttle-mon_client_bytes']['wait']['avgcount']
	sum=data['throttle-mon_client_bytes']['wait']['sum']
	file.write("{0}.throttle-mon_client_bytes-latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))

	#throttle-mon_daemon_bytes
	val=data['throttle-mon_daemon_bytes']['val']
	max=data['throttle-mon_daemon_bytes']['max']
	file.write("{0}.throttle-mon_daemon_bytes-avail {1:.6f}\n".format(mon_id, max - val))
	avgcount=data['throttle-mon_daemon_bytes']['wait']['avgcount']
	sum=data['throttle-mon_daemon_bytes']['wait']['sum']
	file.write("{0}.throttle-mon_daemon_bytes-latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))


	### messenger throttle dispatch ###
	#throttle-msgr_dispatch_throttler-mon
	val=data['throttle-msgr_dispatch_throttler-mon']['val']
	max=data['throttle-msgr_dispatch_throttler-mon']['max']
	file.write("{0}.throttle-msgr_dispatch_throttler-mon-avail {1:.6f}\n".format(mon_id, max - val))
	avgcount=data['throttle-msgr_dispatch_throttler-mon']['wait']['avgcount']
	sum=data['throttle-msgr_dispatch_throttler-mon']['wait']['sum']
	file.write("{0}.throttle-msgr_dispatch_throttler-mon-latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))


	### finisher-monstore ###
	#queue_len
	ql=data['finisher-monstore']['queue_len']
	file.write("{0}.finisher-monstore-queue_len {1:.6f}\n".format(mon_id, ql))
	#complete_latency
	avgcount=data['finisher-monstore']['complete_latency']['avgcount']
	sum=data['finisher-monstore']['complete_latency']['sum']
	file.write("{0}.finisher-monstore-complete_latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))


	### leveldb ###
	#leveldb_get_latency
	avgcount=data['leveldb']['leveldb_get_latency']['avgcount']
	sum=data['leveldb']['leveldb_get_latency']['sum']
	file.write("{0}.leveldb_get_latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))
	#leveldb_submit_latency
	avgcount=data['leveldb']['leveldb_submit_latency']['avgcount']
	sum=data['leveldb']['leveldb_submit_latency']['sum']
	file.write("{0}.leveldb_submit_latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))
	#leveldb_submit_sync_latency
	avgcount=data['leveldb']['leveldb_submit_sync_latency']['avgcount']
	sum=data['leveldb']['leveldb_submit_sync_latency']['sum']
	file.write("{0}.leveldb_submit_sync_latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))


	### paxos ###
	#refresh_latency
	avgcount=data['paxos']['refresh_latency']['avgcount']
	sum=data['paxos']['refresh_latency']['sum']
	file.write("{0}.paxos-refresh_latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))
	#begin_latency
	avgcount=data['paxos']['begin_latency']['avgcount']
	sum=data['paxos']['begin_latency']['sum']
	file.write("{0}.paxos-begin_latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))
	#commit_latency
	avgcount=data['paxos']['commit_latency']['avgcount']
	sum=data['paxos']['commit_latency']['sum']
	file.write("{0}.paxos-commit_latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))
	#collect_latency
	avgcount=data['paxos']['collect_latency']['avgcount']
	sum=data['paxos']['collect_latency']['sum']
	file.write("{0}.paxos-collect_latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))
	#store_state_latency
	avgcount=data['paxos']['store_state_latency']['avgcount']
	sum=data['paxos']['store_state_latency']['sum']
	file.write("{0}.paxos-store_state_latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))
	#new_pn_latency
	avgcount=data['paxos']['new_pn_latency']['avgcount']
	sum=data['paxos']['new_pn_latency']['sum']
	file.write("{0}.paxos-new_pn_latency {1:.6f}\n".format(mon_id, avgcount and sum / avgcount or 0))


# save data
file.close()

# copy data
os.system("cp /etc/ceph/.mon_dump /etc/ceph/mon_dump")
