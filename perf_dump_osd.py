import json
import sys
import os
import commands

file = open('/etc/ceph/.osd_dump', 'w')
lastfile = open('/etc/ceph/.last_osd_dump', 'w')

for filename in os.listdir("/var/lib/ceph/osd"):
	osd_id = filename.split("-")[1]
	if not osd_id:
		continue

	perf_dump = os.popen("ceph daemon osd.{0} perf dump".format(osd_id))
	data = json.load(perf_dump)

	### messenger dispatch throttle ###
	#client
	val=data['throttle-msgr_dispatch_throttler-client']['val']
	max=data['throttle-msgr_dispatch_throttler-client']['max']
	file.write("{0}.throttle-msgr_dispatch_throttler-client-avail {1:.6f}\n".format(osd_id, max - val))
	avgcount=data['throttle-msgr_dispatch_throttler-client']['wait']['avgcount']
	sum=data['throttle-msgr_dispatch_throttler-client']['wait']['sum']
	file.write("{0}.throttle-msgr_dispatch_throttler-client-latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#cluster
	val=data['throttle-msgr_dispatch_throttler-cluster']['val']
	max=data['throttle-msgr_dispatch_throttler-cluster']['max']
	file.write("{0}.throttle-msgr_dispatch_throttler-cluster-avail {1:.6f}\n".format(osd_id, max - val))
	avgcount=data['throttle-msgr_dispatch_throttler-cluster']['wait']['avgcount']
	sum=data['throttle-msgr_dispatch_throttler-cluster']['wait']['sum']
	file.write("{0}.throttle-msgr_dispatch_throttler-cluster-latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#hb_back_server
	val=data['throttle-msgr_dispatch_throttler-hb_back_server']['val']
	max=data['throttle-msgr_dispatch_throttler-hb_back_server']['max']
	file.write("{0}.throttle-msgr_dispatch_throttler-hb_back_server-avail {1:.6f}\n".format(osd_id, max - val))
	avgcount=data['throttle-msgr_dispatch_throttler-hb_back_server']['wait']['avgcount']
	sum=data['throttle-msgr_dispatch_throttler-hb_back_server']['wait']['sum']
	file.write("{0}.throttle-msgr_dispatch_throttler-hb_back_server-latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#hb_front_server
	val=data['throttle-msgr_dispatch_throttler-hb_front_server']['val']
	max=data['throttle-msgr_dispatch_throttler-hb_front_server']['max']
	file.write("{0}.throttle-msgr_dispatch_throttler-hb_front_server-avail {1:.6f}\n".format(osd_id, max - val))
	avgcount=data['throttle-msgr_dispatch_throttler-hb_front_server']['wait']['avgcount']
	sum=data['throttle-msgr_dispatch_throttler-hb_front_server']['wait']['sum']
	file.write("{0}.throttle-msgr_dispatch_throttler-hb_front_server-latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#hbclient
	val=data['throttle-msgr_dispatch_throttler-hbclient']['val']
	max=data['throttle-msgr_dispatch_throttler-hbclient']['max']
	file.write("{0}.throttle-msgr_dispatch_throttler-hbclient-avail {1:.6f}\n".format(osd_id, max - val))
	avgcount=data['throttle-msgr_dispatch_throttler-hbclient']['wait']['avgcount']
	sum=data['throttle-msgr_dispatch_throttler-hbclient']['wait']['sum']
	file.write("{0}.throttle-msgr_dispatch_throttler-hbclient-latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#ms_objecter
	val=data['throttle-msgr_dispatch_throttler-ms_objecter']['val']
	max=data['throttle-msgr_dispatch_throttler-ms_objecter']['max']
	file.write("{0}.throttle-msgr_dispatch_throttler-ms_objecter-avail {1:.6f}\n".format(osd_id, max - val))
	avgcount=data['throttle-msgr_dispatch_throttler-ms_objecter']['wait']['avgcount']
	sum=data['throttle-msgr_dispatch_throttler-ms_objecter']['wait']['sum']
	file.write("{0}.throttle-msgr_dispatch_throttler-ms_objecter-latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))


	### objecter op throttle ###
	#objecter_bytes
	val=data['throttle-objecter_bytes']['val']
	max=data['throttle-objecter_bytes']['max']
	file.write("{0}.throttle-objecter_bytes-avail {1:.6f}\n".format(osd_id, max - val))
	avgcount=data['throttle-objecter_bytes']['wait']['avgcount']
	sum=data['throttle-objecter_bytes']['wait']['sum']
	file.write("{0}.throttle-objecter_bytes-latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#objecter_ops
	val=data['throttle-objecter_ops']['val']
	max=data['throttle-objecter_ops']['max']
	file.write("{0}.throttle-objecter_ops-avail {1:.6f}\n".format(osd_id, max - val))
	avgcount=data['throttle-objecter_ops']['wait']['avgcount']
	sum=data['throttle-objecter_ops']['wait']['sum']
	file.write("{0}.throttle-objecter_ops-latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))


	### osd client policy throttle (ms_public messenger)###
	#throttle-osd_client_bytes
	val=data['throttle-osd_client_bytes']['val']
	max=data['throttle-osd_client_bytes']['max']
	file.write("{0}.throttle-osd_client_bytes-avail {1:.6f}\n".format(osd_id, max - val))
	avgcount=data['throttle-osd_client_bytes']['wait']['avgcount']
	sum=data['throttle-osd_client_bytes']['wait']['sum']
	file.write("{0}.throttle-osd_client_bytes-latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#throttle-osd_client_messages
	val=data['throttle-osd_client_messages']['val']
	max=data['throttle-osd_client_messages']['max']
	file.write("{0}.throttle-osd_client_messages-avail {1:.6f}\n".format(osd_id, max - val))
	avgcount=data['throttle-osd_client_messages']['wait']['avgcount']
	sum=data['throttle-osd_client_messages']['wait']['sum']
	file.write("{0}.throttle-osd_client_messages-latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))


	### osd ###
	#op_wip
	op_wip=data['osd']['op_wip']
	file.write("{0}.osd-op_wip {1:.6f}\n".format(osd_id, op_wip))

	#op
	op=data['osd']['op']
	last_op=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-op".format(osd_id))
	file.write("{0}.osd-op {1}\n".format(osd_id, op - int(last_op)))
	lastfile.write("{0}.osd-op {1}\n".format(osd_id, op))

	#op_in_bytes
	oib=data['osd']['op_in_bytes']
	last_oib=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-op_in_bytes".format(osd_id))
	file.write("{0}.osd-op_in_bytes {1}\n".format(osd_id, oib - int(last_oib)))
	lastfile.write("{0}.osd-op_in_bytes {1}\n".format(osd_id, oib))

	#op_out_bytes
	oob=data['osd']['op_out_bytes']
	last_oob=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-op_out_bytes".format(osd_id))
	file.write("{0}.osd-op_out_bytes {1}\n".format(osd_id, oob - int(last_oob)))
	lastfile.write("{0}.osd-op_out_bytes {1}\n".format(osd_id, oob))

	#op_latency
	avgcount=data['osd']['op_latency']['avgcount']
	sum=data['osd']['op_latency']['sum']
	file.write("{0}.osd-op_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_process_latency
	avgcount=data['osd']['op_process_latency']['avgcount']
	sum=data['osd']['op_process_latency']['sum']
	file.write("{0}.osd-op_process_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_prepare_latency
	avgcount=data['osd']['op_prepare_latency']['avgcount']
	sum=data['osd']['op_prepare_latency']['sum']
	file.write("{0}.osd-op_prepare_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_r
	opr=data['osd']['op_r']
	last_opr=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-op_r".format(osd_id))
	file.write("{0}.osd-op_r {1}\n".format(osd_id, opr - int(last_opr)))
	lastfile.write("{0}.osd-op_r {1}\n".format(osd_id, opr))

	#op_r_out_bytes
	orob=data['osd']['op_r_out_bytes']
	last_orob=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-op_r_out_bytes".format(osd_id))
	file.write("{0}.osd-op_r_out_bytes {1}\n".format(osd_id, orob - int(last_orob)))
	lastfile.write("{0}.osd-op_r_out_bytes {1}\n".format(osd_id, orob))

	#op_r_latency
	avgcount=data['osd']['op_r_latency']['avgcount']
	sum=data['osd']['op_r_latency']['sum']
	file.write("{0}.osd-op_r_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_r_process_latency
	avgcount=data['osd']['op_r_process_latency']['avgcount']
	sum=data['osd']['op_r_process_latency']['sum']
	file.write("{0}.osd-op_r_process_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_r_prepare_latency
	avgcount=data['osd']['op_r_prepare_latency']['avgcount']
	sum=data['osd']['op_r_prepare_latency']['sum']
	file.write("{0}.osd-op_r_prepare_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_w
	opw=data['osd']['op_w']
	last_opw=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-op_w".format(osd_id))
	file.write("{0}.osd-op_w {1}\n".format(osd_id, opw - int(last_opw)))
	lastfile.write("{0}.osd-op_w {1}\n".format(osd_id, opw))

	#op_w_in_bytes
	owib=data['osd']['op_w_in_bytes']
	last_owib=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-op_w_in_bytes".format(osd_id))
	file.write("{0}.osd-op_w_in_bytes {1}\n".format(osd_id, owib - int(last_owib)))
	lastfile.write("{0}.osd-op_w_in_bytes {1}\n".format(osd_id, owib))

	#op_w_rlat
	avgcount=data['osd']['op_w_rlat']['avgcount']
	sum=data['osd']['op_w_rlat']['sum']
	file.write("{0}.osd-op_w_rlat {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_w_latency
	avgcount=data['osd']['op_w_latency']['avgcount']
	sum=data['osd']['op_w_latency']['sum']
	file.write("{0}.osd-op_w_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_w_process_latency
	avgcount=data['osd']['op_w_process_latency']['avgcount']
	sum=data['osd']['op_w_process_latency']['sum']
	file.write("{0}.osd-op_w_process_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_w_prepare_latency
	avgcount=data['osd']['op_w_prepare_latency']['avgcount']
	sum=data['osd']['op_w_prepare_latency']['sum']
	file.write("{0}.osd-op_w_prepare_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_rw
	oprw=data['osd']['op_rw']
	last_oprw=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-op_rw".format(osd_id))
	file.write("{0}.osd-op_rw {1}\n".format(osd_id, oprw - int(last_oprw)))
	lastfile.write("{0}.osd-op_rw {1}\n".format(osd_id, oprw))

	#op_rw_in_bytes
	orwib=data['osd']['op_rw_in_bytes']
	last_orwib=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-op_rw_in_bytes".format(osd_id))
	file.write("{0}.osd-op_rw_in_bytes {1}\n".format(osd_id, orwib - int(last_orwib)))
	lastfile.write("{0}.osd-op_rw_in_bytes {1}\n".format(osd_id, orwib))

	#op_rw_out_bytes
	orwob=data['osd']['op_rw_out_bytes']
	last_orwob=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-op_rw_out_bytes".format(osd_id))
	file.write("{0}.osd-op_rw_out_bytes {1}\n".format(osd_id, orwob - int(last_orwob)))
	lastfile.write("{0}.osd-op_rw_out_bytes {1}\n".format(osd_id, orwob))

	#op_rw_rlat
	avgcount=data['osd']['op_rw_rlat']['avgcount']
	sum=data['osd']['op_rw_rlat']['sum']
	file.write("{0}.osd-op_rw_rlat {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_rw_latency
	avgcount=data['osd']['op_rw_latency']['avgcount']
	sum=data['osd']['op_rw_latency']['sum']
	file.write("{0}.osd-op_rw_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_rw_process_latency
	avgcount=data['osd']['op_rw_process_latency']['avgcount']
	sum=data['osd']['op_rw_process_latency']['sum']
	file.write("{0}.osd-op_rw_process_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#op_rw_prepare_latency
	avgcount=data['osd']['op_rw_prepare_latency']['avgcount']
	sum=data['osd']['op_rw_prepare_latency']['sum']
	file.write("{0}.osd-op_rw_prepare_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	## subop ##
	#subop_w
	subopw=data['osd']['subop_w']
	last_subopw=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-subop_w".format(osd_id))
	file.write("{0}.osd-subop_w {1}\n".format(osd_id, subopw - int(last_subopw)))
	lastfile.write("{0}.osd-subop_w {1}\n".format(osd_id, subopw))

	#subop_w_in_bytes
	subowib=data['osd']['subop_w_in_bytes']
	last_subowib=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.osd-subop_w_in_bytes".format(osd_id))
	file.write("{0}.osd-subop_w_in_bytes {1}\n".format(osd_id, subowib - int(last_subowib)))
	lastfile.write("{0}.osd-subop_w_in_bytes {1}\n".format(osd_id, subowib))

	#subop_w_latency
	avgcount=data['osd']['subop_w_latency']['avgcount']
	sum=data['osd']['subop_w_latency']['sum']
	file.write("{0}.osd-subop_w_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))


	### filestore  ###
	#journal_queue_ops
	jqo=data['filestore']['journal_queue_ops']
	file.write("{0}.filestore-journal_queue_ops {1:.6f}\n".format(osd_id, jqo))

	#journal_queue_bytes
	jqb=data['filestore']['journal_queue_bytes']
	file.write("{0}.filestore-journal_queue_bytes {1:.6f}\n".format(osd_id, jqb))

	#journal_ops
	jo=data['filestore']['journal_ops']
	last_jo=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.filestore-journal_ops".format(osd_id))
	file.write("{0}.filestore-journal_ops {1}\n".format(osd_id, jo - int(last_jo)))
	lastfile.write("{0}.osd-filestore-journal_ops {1}\n".format(osd_id, jo))

	#journal_bytes
	jb=data['filestore']['journal_bytes']
	last_jb=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.filestore-journal_bytes".format(osd_id))
	file.write("{0}.filestore-journal_bytes {1}\n".format(osd_id, jb - int(last_jb)))
	lastfile.write("{0}.filestore-journal_bytes {1}\n".format(osd_id, jb))

	#journal_latency
	avgcount=data['filestore']['journal_latency']['avgcount']
	sum=data['filestore']['journal_latency']['sum']
	file.write("{0}.filestore-journal_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#journal_wr
	jw=data['filestore']['journal_wr']
	last_jw=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.filestore-journal_wr".format(osd_id))
	file.write("{0}.filestore-journal_wr {1}\n".format(osd_id, jw - int(last_jw)))
	lastfile.write("{0}.osd-filestore-journal_wr {1}\n".format(osd_id, jw))

	#journal_wr_bytes
	avgcount=data['filestore']['journal_wr_bytes']['avgcount']
	sum=data['filestore']['journal_wr_bytes']['sum']
	file.write("{0}.filestore-journal_wr_bytes {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#journal_full
	jf=data['filestore']['journal_full']
	last_jf=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.filestore-journal_full".format(osd_id))
	file.write("{0}.filestore-journal_full {1}\n".format(osd_id, jf - int(last_jf)))
	lastfile.write("{0}.filestore-journal_full {1}\n".format(osd_id, jf))

	#op_queue_max_ops
	oqmo=data['filestore']['op_queue_max_ops']
	file.write("{0}.filestore-op_queue_max_ops {1:.6f}\n".format(osd_id, oqmo))

	#op_queue_ops
	oqo=data['filestore']['op_queue_ops']
	file.write("{0}.filestore-op_queue_ops {1:.6f}\n".format(osd_id, oqo))

	#ops
	ops=data['filestore']['ops']
	last_ops=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.filestore-ops".format(osd_id))
	file.write("{0}.filestore-ops {1}\n".format(osd_id, ops - int(last_ops)))
	lastfile.write("{0}.filestore-ops {1}\n".format(osd_id, ops))

	#op_queue_max_bytes
	oqmb=data['filestore']['op_queue_max_bytes']
	file.write("{0}.filestore-op_queue_max_bytes {1:.6f}\n".format(osd_id, oqmb))

	#op_queue_bytes
	oqb=data['filestore']['op_queue_bytes']
	file.write("{0}.filestore-op_queue_bytes {1:.6f}\n".format(osd_id, oqb))

	#bytes
	bytes=data['filestore']['bytes']
	last_bytes=commands.getoutput("/root/ceph_ops/get_last_key.sh /etc/ceph/last_osd_dump {0}.filestore-bytes".format(osd_id))
	file.write("{0}.filestore-bytes {1}\n".format(osd_id, bytes - int(last_bytes)))
	lastfile.write("{0}.filestore-bytes {1}\n".format(osd_id, bytes))

	#apply_latency
	avgcount=data['filestore']['apply_latency']['avgcount']
	sum=data['filestore']['apply_latency']['sum']
	file.write("{0}.filestore-apply_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	#queue_transaction_latency_avg
	avgcount=data['filestore']['queue_transaction_latency_avg']['avgcount']
	sum=data['filestore']['queue_transaction_latency_avg']['sum']
	file.write("{0}.filestore-queue_transaction_latency_avg {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))


	### finisher ###
	## JournalObjectStore ##
	#queue_len
	qlen=data['finisher-JournalObjectStore']['queue_len']
	file.write("{0}.finisher-JournalObjectStore-queue_len {1:.6f}\n".format(osd_id, qlen))
	#complete_latency
	avgcount=data['finisher-JournalObjectStore']['complete_latency']['avgcount']
	sum=data['finisher-JournalObjectStore']['complete_latency']['sum']
	file.write("{0}.finisher-JournalObjectStore-complete_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	## filestore-apply-0 ##
	#queue_len
	qlen=data['finisher-filestore-apply-0']['queue_len']
	file.write("{0}.finisher-filestore-apply-0-queue_len {1:.6f}\n".format(osd_id, qlen))
	#complete_latency
	avgcount=data['finisher-filestore-apply-0']['complete_latency']['avgcount']
	sum=data['finisher-filestore-apply-0']['complete_latency']['sum']
	file.write("{0}.finisher-filestore-apply-0-complete_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))

	## filestore-ondisk-0 ##
	#queue_len
	qlen=data['finisher-filestore-ondisk-0']['queue_len']
	file.write("{0}.finisher-filestore-ondisk-0-queue_len {1:.6f}\n".format(osd_id, qlen))
	#complete_latency
	avgcount=data['finisher-filestore-ondisk-0']['complete_latency']['avgcount']
	sum=data['finisher-filestore-ondisk-0']['complete_latency']['sum']
	file.write("{0}.finisher-filestore-ondisk-0-complete_latency {1:.6f}\n".format(osd_id, avgcount and sum / avgcount or 0))


# save data
file.close()
lastfile.close()

# copy data
os.system("cp /etc/ceph/.osd_dump /etc/ceph/osd_dump")
os.system("cp /etc/ceph/.last_osd_dump /etc/ceph/last_osd_dump")
