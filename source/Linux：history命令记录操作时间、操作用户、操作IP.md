---
title: history命令记录操作时间、操作用户、操作IP
date: 2017-09-26 21:00:05
categories: linux
tags: 
---
### Linux：history命令记录操作时间、操作用户、操作IP
1、/etc/profile文件中加入以下内容

2、执行：source /etc/profile


```
export HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S "
echo 'export HISTTIMEFORMAT="%F %T `whoami` "'
USER_IP=`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'` 
xport HISTTIMEFORMAT="[%F %T][`whoami`][${USER_IP}] "  

USER_IP=`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'` 
export HISTTIMEFORMAT="[%F %T][`whoami`][${USER_IP}] "
#history 
LOGIP=`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'` 
LOG_DIR=/var/log/history 
if [ -z $LOGIP ] 
then 
LOGIP=`hostname` 
fi 
if [ ! -d $LOG_DIR ] 
then 
mkdir -p $LOG_DIR 
chmod 777 $LOG_DIR 
fi
if [ ! -d $LOG_DIR/${LOGNAME} ] 
then 
mkdir -p $LOG_DIR/${LOGNAME} 
chmod 777 $LOG_DIR/${LOGNAME} 
fi
export HISTSIZE=4096 
LOGTM=`date +"%Y%m%d_%H%M%S"` 
export HISTFILE="$LOG_DIR/${LOGNAME}/${LOGIP}-$LOGTM" 
chmod 777 $LOG_DIR/${LOGNAME}/*-* 2>/dev/null
```
