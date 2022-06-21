#!/usr/bin/env python
# coding=utf-8

import sys
import os
import json

def do_local_cmd(cmd):
    #print "Do command: %s" % cmd
    if conf_debug: return

    out = os.system(cmd)
    if out:
        print "Error code: %d" % out
        sys.exit(1)
    return

def do_local_cmd_with_return(cmd):
    #print "Do command: %s" % cmd
    if conf_debug: return []

    output_list_ori = os.popen(cmd).readlines()
    output_list = []
    for item in output_list_ori:
        output_list.append(item.strip('\n'))
    return output_list

def  deal_ceph_latency_value(latency):
    """ Deal with the ceph latency value, return the value we needed
    """
    sum_value = latency["sum"]
    avgc_value = latency["avgcount"]

    ret_value = 0
    if avgc_value != 0:
        ret_value = sum_value*1000/avgc_value
    return ret_value

def get_rgw_perf_dump_info():
    # Get the radosgw daemons in this node
    rgws = do_local_cmd_with_return("ps ax | grep radosgw | grep -v 'grep' | awk '{print $10}'")
    #print "rgws: %s" % rgws
    if not rgws: return

    file = open('/etc/ceph/.rgw_dump', 'w')
    # Get each radosgw daemon dump info
    for rgw in rgws:
        perf_dump = os.popen("ceph daemon {0} perf dump".format(rgw))
        data = json.load(perf_dump)

        ##cct
        total_workers = data['cct']['total_workers']
        unhealthy_workers = data['cct']['unhealthy_workers']
        file.write("{0}.cct.total_workers {1}\n".format(rgw, total_workers))
        file.write("{0}.cct.unhealthy_workers {1}\n".format(rgw, unhealthy_workers))

        ##rgw
        rgwinfo = data[rgw]

        #req
        req = rgwinfo['req']
        failed_req = rgwinfo['failed_req']
        file.write("{0}.req {1}\n".format(rgw, req))
        file.write("{0}.failed_req {1}\n".format(rgw, failed_req))

        #get
        get = rgwinfo['get']
        get_b = rgwinfo['get_b']
        file.write("{0}.get {1}\n".format(rgw, get))
        file.write("{0}.get_b {1}\n".format(rgw, get_b))
        file.write("{0}.get_initial_lat {1}\n".format(rgw, deal_ceph_latency_value(rgwinfo['get_initial_lat'])))

        #put
        put = rgwinfo['put']
        put_b = rgwinfo['put_b']
        file.write("{0}.put {1}\n".format(rgw, put))
        file.write("{0}.put_b {1}\n".format(rgw, put_b))
        file.write("{0}.put_initial_lat {1}\n".format(rgw, deal_ceph_latency_value(rgwinfo['put_initial_lat'])))

        #cache
        cache_hit = rgwinfo['cache_hit']
        cache_miss = rgwinfo['cache_miss']
        file.write("{0}.cache_hit {1}\n".format(rgw, cache_hit))
        file.write("{0}.cache_miss {1}\n".format(rgw, cache_miss))

    # save data
    file.close()

    # copy data
    os.system("cp /etc/ceph/.rgw_dump /etc/ceph/rgw_dump")

def main(argv):
    get_rgw_perf_dump_info()

# Configurations of this script
conf_debug = False

if __name__ == '__main__':
    main(sys.argv)
