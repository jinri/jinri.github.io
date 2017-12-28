---
title: openssh nginx 升级
date: 2016-11-29 21:00:05
tags: 
---
## Linux ubuntu 升级openssh nginx



### 1. 升级openssh 

查看已安装的版本信息：
```
#ssh -V
 OpenSSH_5.9p1 Debian-5ubuntu1, OpenSSL 1.0.1 14 Mar 2012
```

这里把openssh升级到7.6p1版本：

```
cd /tmp
cp /etc/ssh/ /etc/ssh_bak/
wget https://openbsd.hk/pub/OpenBSD/OpenSSH/portable/openssh-7.6p1.tar.gz 
sudo apt-get remove openssh-server 
tar -zxvf openssh-7.6p1.tar.gz
./configure --prefix=/usr --sysconfdir=/etc/ssh --with-md5-passwords --with-privsep-path=/var/lib/sshd  
make 
make install
service ssh restart

```

升级后

```
ssh -V
OpenSSH_7.6p1, OpenSSL 1.0.1f 6 Jan 2014
```

### 2. 升级nginx
升级前
```
nginx -v
nginx version: nginx/1.1.19
```

升级
```
cp /etc/nginx  /etc/nginx_bak
cd /tmp
wget http://nginx.org/keys/nginx_signing.key
apt-key add nginx_signing.key
echo  deb http://nginx.org/packages/mainline/ubuntu/ precise nginx >> /etc/apt/sources.list.d/nginx.list
echo  deb-src http://nginx.org/packages/mainline/ubuntu/ precise nginx >> /etc/apt/sources.list.d/nginx.list
apt-get remove nginx-common
apt-get update  
apt-get install nginx
service nginx restart

```

升级后
```
nginx -v
nginx version: nginx/1.13.0
```



