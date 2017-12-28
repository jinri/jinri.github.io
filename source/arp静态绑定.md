---
title: arp静态绑定
date: 2017-10-26 22:00:10
categories: windows
tags: 
---
- Windows的命令提示符下，键入命令
```
ipconfig /all
```
查看一下本机电脑的IP地址信息，还能看到网关及DNS信息。
- 在DOS命令提示符下输入命令
```
arp -a
```
来获取网关（即路由器）的IP地址和MAC地址。
- 针对WindowXP用户，其操作方法是在DOS命令提示符下输入命令
```
arp -s 192.168.1.1  00-19-e0-aa-9b-e4 
```
即可实现邦定。
- 对于Windows7用户来说，实现方面为在DOS命令提示符下输入命令
```
netsh interface ipv4 show interface
```
回车，查看你电脑所有网卡的idx，然后从中确定你要进行邦定的idx,在本机网络环境中我们需要进行邦定的idx为11，然后输入命令
```
netsh interface ipv4 set neighbors 11 192.168.1.1 00-19-e0-aa-9b-e4
```
实现静态邦定。