---
title: Waf docker镜像构建
date: 2017-11-02 22:00:10
categories: docker
tags: 
---
### 1、基于Ubuntu12.04的waf docker镜像构建

```
FROM ubuntu:12.04
MAINTAINER The bdwaf project <gjf@chinabluedon.cn>
COPY sources.list /etc/apt/ 
RUN apt-get update \ 
&& apt-get -y install gcc make vim libtool autoconf automake libfuzzy-dev libgeoip-dev psmisc \
&& apt-get -y install libgmp-dev libmpfr4 libmpfr-dev libmpc-dev libmpc2 libtool m4 bison flex \
&& apt-get install python-software-properties -y && apt-get install software-properties-common -y \
&& echo '\n'|add-apt-repository ppa:ubuntu-toolchain-r/test \
&& apt-get update && apt-get -y install gcc-4.8 g++-4.8 \
&& update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 20 \
&& update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 20 \
&& update-alternatives --config gcc && update-alternatives --config g++
COPY local/bluedon/bdwaf /usr/local/bluedon/bdwaf
WORKDIR /root/new/
ADD libxml2-2.7.2.tar.gz apr-util-1.5.3.tar.gz apr-1.5.0.tar.gz curl-7.51.0.tar.gz redis_install_packet.tar.gz /root/new/
RUN cd /root/new/apr-1.5.0/ && sed -i '29525s/\$RM/\$RM -f/' configure && ./configure --prefix=/usr/local/apr && make && make install \
&&  cd /root/new/apr-util-1.5.3/ && ./configure --prefix=/usr/local/apr-util --with-apr=/usr/local/apr && make && make install \
&&  cd /root/new/curl-7.51.0/ && ./configure --prefix=/usr/local/curl && make && make install \
&&  cd /root/new/libxml2-2.7.2/ && ./configure --prefix=/usr/local/libxml && make && make install \
&&  cd /root/new/redis_install_packet/ && ./RpProxyRedis.sh && echo $?
COPY libc.conf /etc/ld.so.conf.d/libc.conf 
RUN  ldconfig \
&& chmod a+x /usr/local/bluedon/bdwaf/sbin/bdwaf \
&& mkdir -p /data/proxy_cache \
&& mkdir -p /data/proxy_temp \
&& rm -rf /var/lib/apt/lists/* 
EXPOSE 80 443  
CMD ["/usr/local/bluedon/bdwaf/sbin/bdwaf"]
```

### 2、基于Ubuntu14.04的waf docker镜像构建

```
FROM ubuntu:14.04
MAINTAINER The bdwaf project <gjf@chinabluedon.cn>
COPY sources.list /etc/apt/ 
RUN apt-get update \
&& apt-get -y install gcc make wget lrzsz libtool autoconf automake libfuzzy-dev libgeoip-dev psmisc \
&& rm -rf /var/lib/apt/lists/* 
COPY local/bluedon/bdwaf /usr/local/bluedon/bdwaf
WORKDIR /root/new/
ADD libxml2-2.7.2.tar.gz apr-util-1.5.3.tar.gz apr-1.5.0.tar.gz curl-7.51.0.tar.gz redis_install_packet.tar.gz /root/new/
RUN cd /root/new/apr-1.5.0/ && sed -i '29525s/\$RM/\$RM -f/' configure && ./configure --prefix=/usr/local/apr && make && make install \
&&  cd /root/new/apr-util-1.5.3/ && ./configure --prefix=/usr/local/apr-util --with-apr=/usr/local/apr && make && make install \
&&  cd /root/new/curl-7.51.0/ && ./configure --prefix=/usr/local/curl && make && make install \
&&  cd /root/new/libxml2-2.7.2/ && ./configure --prefix=/usr/local/libxml && make && make install \
&&  cd /root/new/redis_install_packet/ && ./RpProxyRedis.sh && echo $?
COPY libc.conf /etc/ld.so.conf.d/libc.conf 
RUN  ldconfig \
&& chmod a+x /usr/local/bluedon/bdwaf/sbin/bdwaf \
&& mkdir -p /data/proxy_cache \
&& mkdir -p /data/proxy_temp
EXPOSE 80 443  
VOLUME /usr/local/bluedon/bdwaf/sbin/bdwaf/log
CMD ["/usr/local/bluedon/bdwaf/sbin/bdwaf"]
```
