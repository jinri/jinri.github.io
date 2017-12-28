---
title: Nginx配置相关结构划分的技巧
date: 2017-11-26 22:00:05
categories: nginx
tags: 
---
### Nginx配置相关结构划分的技巧

- Nginx配置需要一定的技巧，在不断的使用和维护中就会发现这些，接下来就向大家介绍下有关Nginx配置的相关技巧。Nginx配置是按结构划分，这样可以便于在很多个虚拟主机和目录里重用部分配置。


```
conf/   
      nginx.conf   
      proxy.conf   
      rewrite.conf   
      location.conf   
      port.conf   
      upstream.conf   
      servers/   
              www.qq.com   
              www.163.com
```
1. nginx.conf 这就是Nginx配置读取的主文件，没特殊情况是通用的。
2. proxy.conf 代理的选项配置，也是通用的。
3. rewrite.conf 所有主机的根目录公用的rewrite规则，默认是空文件，可以不使用。
4. location.conf 所有主机都会用到的location目录结构，默认是空文件，可以不使用。
5. port.conf 配置服务器绑定ip和端口，因为Nginx配置如果各个主机ip端口配置有不同会有bug，所以最好是统一设定。
6. upstream.conf upstream写在这里面，和业务分开，易于控制。
7. servers目录 这个目录下面放的是所有的虚拟主机配置，每个虚拟主机一个文件，由Nginx.conf去include，这样处理这些配置变得很灵活。
