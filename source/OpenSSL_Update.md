---
title: OpenSSL升级
date: 2017-02-12 10:50:10
tags:
---

 升级版本为OpenSSL-1.0.1t,操作系统为ubuntu12.04

查看已安装的版本信息：
```
#openssl version
 OpenSSL 1.0.1g 01 Jul 2014
```

1 这里把openSSL升级到1.0.1t版本：

```
# wget https://www.openssl.org/source/openssl-1.0.1t.tar.gz
# tar zvxf openssl-1.0.1t.tar.gz 
# cd openssl-1.0.1t
# ls
# ./config shared zlib
# make
# make install
# /usr/local/ssh/bin/openssl version
 OpenSSL 1.0.1t 3 May 2016
```


2 替换旧的OpenSSL：

```
# mv /usr/bin/openssl /usr/bin/openssl-old
# mv /usr/include/openssl /usr/include/openssl-old
# ln -s /usr/local/ssl/bin/openssl /usr/bin/openssl
# ln -s /usr/local/ssl/include/openssl/ /usr/include/openssl
# echo "/usr/local/ssl/lib" >> /etc/ld.so.conf
# ldconfig 
# openssl version
 OpenSSL 1.0.1t 3 May 2016
```

3 Ubuntu系统升级OpenSSL：

```
# apt-get update
# apt-get install openssl libssl
```
