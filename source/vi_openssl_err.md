---
title: vim打开报openssl error 错误
date: 2017-02-17 12:50:10
tags:
---

#### vim打开报openssl错误

```
observer@bdwaf:~$ vi 
vi: /usr/local/lib/libcrypto.so.1.0.0: no version information available (required by /usr/lib/libpython2.7.so.1.0)
vi: /usr/local/lib/libssl.so.1.0.0: no version information available (required by /usr/lib/libpython2.7.so.1.0)
```

解决方案如下：   
进入openssl的源码目录 

```
cd /root/new/openssl

```
添加

```
vi openssl.ld
OPENSSL_1.0.0 {
global:
*;
};
```

```
./config --prefix=/usr/local --openssldir=/usr/local/openssl shared -Wl,--version-script=/root/new/openssl-1.0.1t/openssl.ld -Wl,-Bsymbolic-functions
make
make test
make install
ldconfig
```
