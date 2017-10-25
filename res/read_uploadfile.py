#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import subprocess
from datetime import datetime, timedelta
import calendar


send_file_to_path = "/root/uploadfile/"
upload_file_path = "/usr/local/bluedon/bdwaf/tmp/uploaddir/"
modsecurity_debug_path = "/usr/local/bluedon/bdwaf/logs/modsec_debug.log"


def get_sid (my_filename):
    sh_cmd = "grep %s %s  | awk -F 'sid#' '{printf $2}' | awk -F ']' '{printf $1}'" % (
        my_filename, modsecurity_debug_path)
    result = subprocess.check_output(sh_cmd, shell=True)
    # print result, type(result)
    return result


def get_unid(my_filename):
    return my_filename.split("-")[2]


def get_time1(unid):
    sh_cmd = "grep \"%s\" %s |awk -F ']' 'NR==1{printf $1}' | awk -F ' ' '{printf $1}' | awk -F '[' '{printf $2}'" % (
        unid, modsecurity_debug_path)
    result = subprocess.check_output(sh_cmd, shell=True)
#    print "check the shell result is: ", result
    return result

def get_time2(unid):
    sh_cmd = "grep \"%s\" %s |grep \"Multipart: Created temporary\"|awk -F ']' 'NR==1{printf $1}' | awk -F ' ' '{printf $1}' | awk -F '[' '{printf $2}'" % (
        unid, modsecurity_debug_path)
    result = subprocess.check_output(sh_cmd, shell=True)
#    print "check the shell result is: ", result
    return result


def get_filename(time_string, sid):
    sh_cmd = "grep \"%s\" %s| grep \"sid#%s\"|awk -F 'Content-Disposition filename: ' '{printf $2}'" % (
        time_string, modsecurity_debug_path, sid)
    result = subprocess.check_output(sh_cmd, shell=True).strip()
#    print "check the shell result is: ", result
    return result


def get_uploadhost(time_string, sid):
    sh_cmd = "grep \"%s\" %s| grep \"sid#%s\"  |awk -F 'upload_host:' '{printf $2}'|awk -F '\"' '{printf $1}'" % (
        time_string, modsecurity_debug_path, sid)
    result = subprocess.check_output(sh_cmd, shell=True).strip()
#    print "check the shell result is: ", result
    return result


def get_url(unid):
    sh_cmd = "sed -n '/%s/p' %s| awk -F ']' 'NR==1{printf $4}'| awk -F '[' '{printf $2}'" % (unid, modsecurity_debug_path)
    result = subprocess.check_output(sh_cmd, shell=True)
#    print "check the shell result is: ", result
    return result

def date_time_2_timestap(date_str, use_utc=True):
    date = datetime.strptime(date_str, "%d/%b/%Y:%H:%M:%S")
    if use_utc:
        date = date + timedelta(hours=-8)
    timestamp = calendar.timegm(date.timetuple())
    #print "check timestap---", timestamp
    return timestamp

def send_file(local_filename,timestamp,url,filename):
   handle_url = url.replace('/','\\\\')
   sh_cmd = "mv %s%s %s%s__%s__%s" % ( 
           upload_file_path,local_filename,send_file_to_path,timestamp,handle_url,filename)
   result = subprocess.check_output(sh_cmd, shell=True)
   if os.path.exists(upload_file_path+local_filename):
        sh_cmd2 = "rm %s%s" % ( 
            upload_file_path,local_filename)

        result2 = subprocess.check_output(sh_cmd2, shell=True)
 #  print "check the shell result is: ", result
   return result

if __name__ == "__main__":
    try:
        local_filename = sys.argv[1]
        print "local_filename=" , local_filename
        #local_filename="20170418-142053-AcAOAcZcVlAcAfAiAcAGAcIe-file-oDAr7v"
        sid = get_sid(local_filename)
        print "sid=" , sid
        unid= get_unid(local_filename)
        print "unid=" , unid
#logtime1 logtime2 中间偶尔存在时间间隔，当取filename时，采用logtime2较准确，取uploadhost时采用logtime1较准确
        logtime1 = get_time1(unid)
        logtime2 = get_time2(unid)
        print "logtime1=" , logtime1
        print "logtime2=" , logtime2
        timestamp=date_time_2_timestap(logtime1)
        print "timestamp=" , timestamp
        filename= get_filename(logtime2, sid)
        print "filename=" , filename
        z_filename = eval('"'+filename+'"')
        uploadhost= get_uploadhost(logtime1, sid)
        print "uploadhost=" , uploadhost
        url= get_url(unid)
        print "url=" , url
        all_url = uploadhost + url
        print "all_url=" , all_url
        send_file(local_filename,timestamp,all_url,z_filename)
    except Exception,e:
        print "read_uploadfile.py have exception , please check!" + str(e)
