---
title: Modsecurity 日志写入redis
date: 2017-07-12 18:00:10
categories: nginx
tags:
---

 Modsecurity 日志写入redis

1、要写入redis，机器上必须要安装有redis服务器。nginx+modsecurity的error.log和modsec_audit.log 原来都是写文件的因为频繁写入文件会造成nginx引擎性能下降（大流量测试流量存在瓶颈），故采用audit日志写入redis的方式。
该功能修改了modsecurity下的3个源文件。

```
modsecurity/standalone/api.c
modsecurity/apache2/msc_logging.h
modsecurity/apache2/msc_logging.c
```
[changeset.diff](https://github.com/jinri/jinri.github.io/blob/master/res/changeset_e87d1044b999b8048a175c843bb1047ed412316f.diff)

2、redis安装

```
unzip redis-3.2.3.tar.gz
tar -xvf redis-3.2.3.tar
cd redis-3.2.3
make
make install PREFIX=/usr/local/redis
```
* 环境配置

```
mkdir -p /var/log/redis
mkdir -p /var/lib/redis
cd /usr/local/redis
mkdir etc
cp /root/redis.conf etc/
```
* 启动redis

```
/usr/local/redis/bin/redis-server /usr/local/redis/etc/redis.conf
```
* 添加到开机启动

```
vi /etc/rc.local 
添加 /usr/local/redis/bin/redis-server /usr/local/redis/etc/redis.conf
```
redis版本2.XX,在使用过程中有redis占用内存持续增大至过大等问题。
故使用为3.XX,升级过程稍微有些区别。
Modsecurity audit日志写入redis，最重要的是使用了redis数据库一个轻量的C语言客户端库Hiredis。

3、hiredis 安装

```
unzip hiredis-master.zip
cd hiredis-master
make;
make install;
ln -s  /usr/local/lib/libhiredis.so.0.13 /usr/lib/x86_64-linux-gnu/libhiredis.so.0.13
```
4、hiredis 是以动态链接库的形式存在，所以必须要编译进nginx才可以。为此增加了一个nginx的编译选项（configure中加入编译选项）

```
--with-cust-ld-opt="-lhiredis"
```
以后在编译nginx的时候如果要加入redis功能需要更改make和options文件。
  
```
nginx-1.8.1/auto/make 
nginx-1.8.1/auto/options
```
写日志进redis采用的是Redis 发布订阅的消息通信模式. 发送者(pub)发送消息，订阅者(sub)接收消息.
Redis 客户端可以订阅任意数量的频道,nginx引擎写入的客户端频道名为：nginx
采用客户端连上redis服务器后，可采用SUBSCRIBE nginx 等待接收消息。
[modsecurity_redis_log.png](https://github.com/jinri/jinri.github.io/blob/master/res/modsecurity_redis_log.png)




