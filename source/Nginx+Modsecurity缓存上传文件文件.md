---
title: Nginx+Modsecurity缓存上传文件文件
date: 2017-09-25 10:00:10
categories: nginx
tags: 
---
创建上传文件目录

```
mkdir /root/uploadfile
mkdir /usr/gjf/tmp/uploaddir
```


安装 lua5.1 包

```
sudo apt-get install lua5.1
```

modsecurity.conf配置更改


```
SecUploadDir /usr/gjf/tmp/uploaddir
SecUploadKeepFiles On
SecUploadFileMode 0600
SecDebugLogLevel 4
```

7测试

在本地host添加：

```
172.16.2.109 www.testupload.com
```
浏览器访问 http://www.testupload.com/dvwa/login.php ，admin/password
