#!/bin/bash

slow_ops_threshold=500
cluster_space_threshold=70

function check_cluster_info()
{
    local info=`ceph health detail --connect-timeout 10 2> /dev/null`

    if [ -z "${info}" ]; then
        ret=1
        msg="ceph查询集群状态超时"
    else
        local need_alarm=0

        # Get the health summary
        summary=`echo "${info}" | head -n 1 | awk '{ if ($1 != "HEALTH_OK") print $0 }'`

        if [ -z "${summary}" ] || [ "${summary}" == "HEALTH_WARN nodeep-scrub flag(s) set" ]; then
            return
        fi

        # Remove the summary, osds have slow requests and nodeep-scrub lines from health detail
        detail=`echo "${info}" | sed -e '/^HEALTH/d' | sed -e '/^nodeep-scrub/d' | sed -e '/osds have slow requests/d'`
        while read -r line; do
            slow_ops=`echo "${line}" | grep "ops are blocked > "`
            if [ -n "${slow_ops}" ]; then
                local period=`echo "$line" | awk -F ">" '{print $2}' | awk '{print $1}'`
                # Alarm if the slow request period larger than threshold
                if [ ${period%.*} -ge $slow_ops_threshold ]; then
                    need_alarm=1
                    break
                fi
            elif [ -n "${line}" ];then
                # Always alarm if there is warning except for slow request
                need_alarm=1
                break
            fi
        done <<< "${detail}"

        if [ $need_alarm -eq 1 ]; then
            ret=1
            msg="ceph集群状态异常, "${summary}
        fi
    fi
}

function check_pg_info()
{
    local info=`ceph pg dump_stuck --connect-timeout 10 2> /dev/null`

    if [ $? -ne 0 ]; then
        ret=1
        msg="ceph查询pg状态超时"
    else
        inactive=`echo "${info}" | grep inactive`
        stale=`echo "${info}" | grep stale`
        if [ -n "${inactive}" -o -n "${stale}" ]; then
            ret=1
            msg="ceph pg状态异常"
        fi
    fi
}

function check_thread_number()
{
    local thread_limit=`ulimit -u`
    thread_limit=$((thread_limit/4*3))
    thread_count=`ps -eLf | awk '{ if ($1 == "ceph") print $0 }' | wc -l`
    if [ ${thread_count} -ge ${thread_limit} ]; then
        ret=1
        msg="ceph账号线程数接近限制"
    fi
}

function check_cluster_space()
{
    local used_space_percent=`ceph df --connect-timeout 10 2> /dev/null | sed -n 3p | awk '{ print $4 }'`
    if [ $? -ne 0 ]; then
        ret=1
        msg="ceph查询df状态超时"
    elif [ ${used_space_percent%.*} -ge $cluster_space_threshold ]; then
        ret=1
        msg="ceph已用存储空间$used_space_percent%超过阀值$cluster_space_threshold%"
    fi
}

function main()
{
    ret=0
    msg=

    case "$1" in
        check_cluster_info)
            if [ $# == 2 ]; then
                slow_ops_threshold=$2
            fi
            check_cluster_info
            ;;
        check_pg_info)
            check_pg_info
            ;;
        check_thread_number)
            check_thread_number
            ;;
        check_cluster_space)
            if [ $# == 2 ]; then
                cluster_space_threshold=$2
            fi
            check_cluster_space
            ;;
        *)
            ret=1
            msg="Incorrect parameter, support parameters: check_cluster_info, check_pg_info, check_thread_number and check_cluster_space!"
            ;;
    esac

    # ret is not 0, error and please do alarm!
    if [ ${ret} -ne 0 ]; then
        echo "${msg}"
    else
        echo ${ret}
    fi
}

main $@
