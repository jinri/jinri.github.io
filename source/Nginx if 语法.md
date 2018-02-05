---
title: Nginx if 语法
date: 2017-12-27 10:00:00
categories: nginx
tags:
---

### 介绍


```
语法：if(condition){………}
配置作用域：server,location
```

### 匹配条件


```
“=” 和““!=”” 变量等于不等于条件
“~” 和“~” 匹配到指定内容是否区分大小写
“!~”和“!~” 匹配到指定内容是否区分大小写
“-f”和“!-f” 检查一个文件是否存在
“-d”和“!-d” 检查一个目录是否存在
“-e”和“!-e” 检查一个文件，目录，软连接是否存在
“-x”和“!-x” 检查一个是否有执行权限
匹配的内容可以是字符串也可以是一个正则表达式。
如果一个正则表达式包含“}”或者“；”就必须包含在单引号或双引号里面。
```
nginx中的if无法进行&&、||等逻辑运算，所以我们需要一步一步的进行判断


```
if(condition){………}
    if($variable ~ '^/product' ){………}
    举例：
    if ($http_user_agent ~ MSIE) {                         #只要“$http_user_agent”配置MSIE的
        rewrite ^(.*)$ /msie/$1 break;                     #URL地址前面加"/msie"
    }

    if ($http_cookie ~* "id=([^;]+)(?:;|$)") {
        set $id $1;
    }

    if ($request_method = POST) {
        return 405;
    }

    if ($slow) {
        limit_rate 10k;
    }

    if ($request_uri ~) {
        return 403;
    }

    if ($request_uri ~ "/test.html") {                     #根据访问地址跳转到目标地址
            rewrite ^ http://new.ngins.net;
    }

    if (-x "/data/test.sh") {                              #根据文件是否有执行权限，跳转到目标
            rewrite ^ http://new.ngins.net;
      }
```
