---
title: LINUX用户登录后精确命令记录
date: 2017-09-26 22:00:05
categories: linux
tags: 
---
### LINUX用户登录后精确命令记录(history 按时间、用户显示命令记录)

 
```
   # 设置保存历史命令的文件大小
   export HISTFILESIZE=10000000

   # 保存历史命令条数
   export HISTSIZE=1000000

   # 实时记录历史命令，默认只有在用户退出之后才会统一记录，很容易造成多个用户间的相互覆盖。
   export PROMPT_COMMAND="history -a"

   # 记录每条历史命令的执行时间
   export HISTTIMEFORMAT="%Y-%m-%d_%H:%M:%S "
```


 
- %Y: 4位数的年份；
- %m: 2位数的月份数；
- %d: 2位数的一个月中的日期数；
- %H：2位数的小时数（24小时制）；
- %M：2位数的分钟数；
- %S：2位数的秒数

主要功能：
- 可以记录哪个ip和时间(精确到秒)作了哪些命令
- 通过用户登录时候，重新定义HISTFILE
- HISTFILE文件名包含登录用户名，ip,登录时间(精确到秒)等
- 这样即使相同的用户从不同ip、在不同的时间登录都会被记录
- 可以记录每条命令的开始执行时间

把下面的代码直接粘贴到/etc/profile后面就可以了
　
```
#history
　　export HISTTIMEFORMAT="[%Y.%m.%d %H:%M:%S]"
　　USER_IP=`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'`
　　HISTDIR=/var/log/.hist
　　if [ -z $USER_IP ]
　　then
　　USER_IP=`hostname`
　　fi
　　if [ ! -d $HISTDIR ]
　　then
　　mkdir -p $HISTDIR
　　chmod 777 $HISTDIR
　　fi
　　if [ ! -d $HISTDIR/${LOGNAME} ]
　　then
　　mkdir -p $HISTDIR/${LOGNAME}
    chmod 300 $HISTDIR/${LOGNAME}
　　fi
　　export HISTSIZE=4096
　　DT=`date +%Y%m%d_%H%M%S`
　　export HISTFILE="$HISTDIR/${LOGNAME}/${USER_IP}.hist.$DT"
　　chmod 600 $HISTDIR/${LOGNAME}/*.hist* 2>/dev/null
```

　　得到的结果，永久保存，每个用户的命令记录分目录保存

```
# ls -l /var/log/.hist/root/
　　-rw------- 1 root root 546 2006-05-26 10:00 218.82.245.54.hist.20060526_092458
　　-rw------- 1 root root 243 2006-05-28 13:28 218.82.245.54.hist.20060528_114822
　　-rw------- 1 root root 10 2006-05-28 12:18 218.82.245.54.hist.20060528_121605
```

　　查看命令记录
　
```
   # export HISTFILE=/var/log/.hist/root/222.72.16.204.hist.20060608_152551
　　# history
　　1 [2006.06.24 13:22:51] vi /etc/profile
　　2 [2006.06.24 13:23:25] cd /var/log/.hist
　　3 [2006.06.24 13:23:26] ls -al
　　4 [2006.06.24 13:23:30] cd sadmin
　　5 [2006.06.24 13:23:31] ls -al
　　6 [2006.06.24 13:24:22] more 58.35.169.51.hist.20060524_193219
　　7 [2006.06.24 13:24:35] 222.72.16.204.hist.20060622_143133
　　8 [2006.06.24 13:24:39] more 222.72.16.204.hist.20060622_143133
　　9 [2006.06.24 13:24:51] hist -f 222.72.16.204.hist.20060622_143133
 
    10 [2006.06.24 13:24:59] history -f 222.72.16.204.hist.20060622_143133
　　11 [2006.06.24 13:25:12] history 222.72.16.204.hist.20060622_143133
　　12 [2006.06.24 13:25:32] man histtory
　　13 [2006.06.24 13:25:38] man history
　　14 [2006.06.24 13:26:00] hist
　　15 [2006.06.24 13:26:04] history
　　16 [2006.06.24 13:26:16] ls
　　17 [2006.06.24 13:26:39] export 222.72.16.204.hist.20060622_143133
　　18 [2006.06.24 13:26:59] export HISTFILE=222.72.16.204.hist.20060608_152551
　　19 [2006.06.24 13:27:07] history
```
