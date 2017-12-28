---
title: ubuntu12.04默认gcc4.6.3升级到gcc4.8
date: 2017-10-26 22:00:10
categories: ubuntu
tags: 
---
```
apt-get update
apt-get install libgmp-dev libmpfr4 libmpfr-dev libmpc-dev libmpc2 libtool m4 bison flex autoconf

apt-get install python-software-properties -y
apt-get install software-properties-common -y
add-apt-repository ppa:ubuntu-toolchain-r/test

apt-get update
apt-get install gcc-4.8 g++-4.8
#apt-get install gcc-4.8-multilib g++-4.8-multilib gcc-4.8-doc

#update-alternatives --remove-all gcc 
#update-alternatives --remove-all g++

update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 20

update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 20

update-alternatives --config gcc

update-alternatives --config g++

gcc --version

#apt-get update
#apt-get upgrade -y 
#apt-get dist-upgrade
```
