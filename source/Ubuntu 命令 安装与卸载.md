---
title: Ubuntu 命令 安装与卸载
date: 2017-5-26 22:00:05
tags: 
---
Ubuntu是最常用的Linux系统之一，其中很多新手在安装软件的过程中，由于对Linux不熟悉，往往不知道如何卸载干净。

---

废话不多说，直接上干货！
命令

```
# apt-cache search
```

  ● 最佳卸载命令

```
apt-get remove packagename --purge && apt-get autoremove --purge && apt-get clean
```
 
卸载程序(包括配置文件)、卸载依赖、删除/var/cache/apt/archives下所有安装包
 
 ● 最佳升级软件命令

```
apt-get update && apt-get upgrade
```


这样就可以完全卸载掉nginx包括配置文件



apt卸载nginx方法


```
sudo apt-get –purge remove nginx
sudo apt-get autoremove dpkg –get-selections|grep nginx 罗列出与nginx相关的软件
sudo apt-get –purge remove nginx-common
sudo apt-get –purge remove nginx
sudo apt-get --purge remove nginx-core
ps -ef |grep nginx
killall nginx 
sudo  find  /  -name  nginx*
sudo rm -rf file
```

1. 卸载方法

```
# 删除nginx，保留配置文件
sudo apt-get remove nginx
#删除配置文件
rm -rf /etc/nginx
卸载方法2.
#删除nginx连带配置文件
sudo apt-get purge nginx # Removes everything.
#卸载不再需要的nginx依赖程序
sudo apt-get autoremove
```

2. 删除nginx连带配置文件

```
sudo apt-get purge nginx # Removes everything.
卸载不再需要的nginx依赖程序
sudo apt-get autoremove
这时候查看版本 nginx -v
可以看到No such file
这时候，如果系统还有些nginx文件
这时候，如果系统还有些nginx文件没有删除，需要手动删除
rm -rf /etc/nginx
rm -rf /etc/init.d/nginx
rm -rf /var/lib/nginx
rm -rf /var/log/nginx
rm -rf /etc/logrotate.d/nginx
```


扩展知识
apt常用命令
 
```
● apt-cache show packagename 获取包的相关信息，如说明、大小、版本等
  ● apt-cache depends packagename 了解使用依赖
  ● apt-cache rdepends packagename 是查看该包被哪些包依赖
  ● apt-get install packagename 安装包
  ● apt-get install package=version 指定安装版本
  ● apt-get install packagename --reinstall 重新安装包
  ● apt-get remove packagename --purge 卸载程序，包括删除配置文件等
  ● apt-get update 更新源,更新 /etc/apt/sources.list里的链接地址
  ● apt-get upgrade -u 升级程序(不包括依赖关系改变的) -u 完整显示列表
  ● apt-get dist-upgrade 升级程序(包括依赖关系改变的并且重新组织依赖关系)
  ● apt-get clean 删除安装包(节约硬盘空间,下次安装需要重新下载包，软件包位置：/var/cache/apt/archives/)
  ● apt-get autoclean 删除已卸载的安装包(Ubuntu14.04测试发现没起作用)
  ● apt-get autoremove 卸载依赖的程序apt-get 安装位置
  ● 下载的软件存放位置 /var/cache/apt/archives
  ● 安装后软件默认位置 /usr/share
  ● 可执行文件位置 /usr/bin
  ● lib文件位置 /usr/lib
```

Linux 常用目录
 
```
● /boot 引导程序，内核等存放的目录
  ● /sbin 超级用户可以使用的命令的目录
  ● /bin 普通用户使用的命令
  ● /lib 共享库目录
  ● /dev 设备目录
  ● /root 用户root的home目录
  ● /etc 全局配置文件目录
  ● /usr 用户安装目录
  ● /usr/include C程序语言编译使用的头文件
  ● /proc 系统内部一些信息
  ● /var 经常变化目录 经常放日志文件，缓存文件
  ● /tmp 临时目录 系统断电 或许目录被会清空
  ● /lost+found 当系统崩溃的时候，在系统修复过程中需要恢复的文件，可能就会在这里被找到了，这个目录一般为空
```

