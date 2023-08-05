#!/usr/bin/python
# Script to write nagios status in csv format for nagios audit
# @ Arun prasath

# Usage: Run generate_nagios.sh

import re
import datetime
import os.path

def checkFile(PATH):
    try:
        if os.path.isfile(PATH):
            return True
        else:
            raise IOError("File not found.")

    except IOError,e:
        print "Nagios status file (status.dat) is not found in current or specified location. Please specify a file using '--input_file' in your command."
        exit()

def getDate(epoch):
    if epoch != None:
        epoch = int(epoch)
        return datetime.datetime.fromtimestamp(epoch).strftime('%c')
    return None

def parseConf(source):
    conf = {}
    patID=re.compile(r"(?:\s*define)?\s*(\w+)\s+{")
    patAttr=re.compile(r"\s*(\w+)(?:=|\s+)(.*)")
    patEndID=re.compile(r"\s*}")
    for line in source.splitlines():
        line=line.strip()
        matchID = patID.match(line)
        matchAttr = patAttr.match(line)
        matchEndID = patEndID.match( line)
        if len(line) == 0 or line[0]=='#':
            pass
        elif matchID:
            identifier = matchID.group(1)
            cur = [identifier, {}]
        elif matchAttr:
            attribute = matchAttr.group(1)
            value = matchAttr.group(2).strip()
            cur[1][attribute] = value
        elif matchEndID and cur:
            conf.setdefault(cur[0],[]).append(cur[1])
            del cur
    return conf


#hostlist=[host['host_name'] for host in nagcfg['hoststatus']
#          if host['host_name'].startswith('alln01-2-csm-p')]
#print hostlist

def getServiceDowntime(nagcfg,host,service):
    for srv_downtime in nagcfg['servicedowntime']:
        if srv_downtime['host_name'] == host and srv_downtime['service_description'] == service:
            return srv_downtime['start_time'],srv_downtime['end_time'],srv_downtime['duration'],srv_downtime['is_in_effect'],srv_downtime['author'],srv_downtime['comment']
    return None

def getServiceComment(nagcfg,host,service):
    for srv_comment in nagcfg['servicecomment']:
        if srv_comment['host_name'] == host and srv_comment['service_description'] == service:
            return srv_comment['entry_time'], srv_comment['author'], srv_comment['comment_data']
    return None


def getHostDowntime(nagcfg,host):
    for host_downtime in nagcfg['hostdowntime']:
        if host_downtime['host_name'] == host:
            return host_downtime['start_time'],host_downtime['end_time'],host_downtime['duration'],host_downtime['is_in_effect'],host_downtime['author'],host_downtime['comment']
    return None

def getHostComment(nagcfg,host):
    for host_comment in nagcfg['hostcomment']:
        if host_comment['host_name'] == host:
            return host_comment['entry_time'], host_comment['author'], host_comment['comment_data']

def getNagiosServiceStatus(num):
    if num == '0':
        return 'OK'
    elif num == '1':
        return "WARN"
    elif num == '2':
        return "CRITICAL"
    elif num == '3':
        return "UNKNOWN"
    else:
        return "UNKNOWN"


def getNagiosHostStatus(num):
    if num == '0':
        return "OK"
    elif num == '1':
        return "CRITICAL"
    else:
        return "UNKNOWN"

def getNagiosObject(PATH):
    checkFile(PATH)
    str1 = open(PATH, 'r').read()
    nagcfg=parseConf(str1)
    return nagcfg
'''
print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("Component",
                                                                         "HOST",
                                                                         "Service",
                                                                         "STATE",
                                                                         "OUPUT",
                                                                         "NOTIFICATION_STATUS",
                                                                         "COMMENT_ENTRY_TIME",
                                                                         "COMMENT_AUTHOR",
                                                                         "COMMENT_DATA",
                                                                         "DOWNTIME_START",
                                                                         "DOWNTIME_END",
                                                                         "DOWNTIME_DURATION",
                                                                         "IS_DOWNTIME",
                                                                         "IS_ACKNOWLEDGED",
                                                                         "DOWNTIME_AUTHOR",
                                                                         "DOWNTIME_COMMENT"))
'''
def checkIssue(object):
    status = False
    if object['current_state'] != '0' or \
                    object['problem_has_been_acknowledged'] != '0' or \
                    object['notifications_enabled'] != '1' or \
                    object['scheduled_downtime_depth'] != '0':
        status = True
    return status

def get_servicestatus_list(nagcfg):
    service_status_list = []
    for service in nagcfg['servicestatus']:
        #if service['current_state'] != '0':
        if checkIssue(service):
            if getServiceDowntime(nagcfg,service['host_name'],service['service_description']) != None:
                start_time,end_time,duration,is_in_effect,author,comment = getServiceDowntime(nagcfg,service['host_name'],service['service_description'])
            else:
                start_time = end_time = duration = is_in_effect = author = comment = None
            if getServiceComment(nagcfg,service['host_name'],service['service_description']) != None :
                c_entry_time, c_author, c_comment = getServiceComment(nagcfg,service['host_name'],service['service_description'])
            else:
                c_entry_time = c_author = c_comment = None
            service_status_list.append(("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t"  % ( "Servicestatus",
                                                                                      service['host_name'],
                                                                                      service['service_description'],
                                                                                      getNagiosServiceStatus(service['current_state']),
                                                                                      service['plugin_output'],
                                                                                      "ENABLED" if service['notifications_enabled']== "1" else "DISABLED",
                                                                                      getDate(c_entry_time),
                                                                                      c_author,
                                                                                      c_comment,
                                                                                      getDate(start_time),
                                                                                      getDate(end_time),
                                                                                      duration,
                                                                                      is_in_effect,
                                                                                      "ACKNOWLEDGED" if service['problem_has_been_acknowledged']=='1' else "NOT_ACKNOWLEDGED",
                                                                                      author,
                                                                                      comment)))
    return service_status_list

def get_hoststatus_list(nagcfg):
    host_status_list = []
    for host in nagcfg['hoststatus']:
        #if host['current_state'] != '0' or host['host_name'] in str(nagcfg['hostdowntime']):
        if checkIssue(host):
            if host['host_name'] in str(nagcfg['hostdowntime']):
                start_time, end_time, duration, is_in_effect, author, comment = getHostDowntime(nagcfg,
                                                                                                   host['host_name'])
            else:
                start_time = end_time = duration = is_in_effect = author = comment = None
            if host['host_name'] in str(nagcfg['hostcomment']):
                c_entry_time, c_author, c_comment = getHostComment(nagcfg, host['host_name'])
            else:
                c_entry_time = c_author = c_comment = None
            host_status_list.append(("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("Hoststatus",
                                                                                     host['host_name'],
                                                                                     "NA",
                                                                                     getNagiosHostStatus(host['current_state']),
                                                                                     host['plugin_output'],
                                                                                     "ENABLED" if host['notifications_enabled'] == "1" else "DISABLED",
                                                                                     getDate(c_entry_time),
                                                                                     c_author,
                                                                                     c_comment,
                                                                                     getDate(start_time),
                                                                                     getDate(end_time),
                                                                                     duration,
                                                                                     is_in_effect,
                                                                                     "ACKNOWLEDGED" if host ['problem_has_been_acknowledged'] == '1' else "NOT_ACKNOWLEDGED",
                                                                                     author,
                                                                                     comment)))

    return host_status_list
