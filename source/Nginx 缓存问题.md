---
title: Nginx 缓存问题
date: 2017-12-12 10:00:00
categories: nginx
tags:
---
* [#p1 1 expires浏览器缓存不一致]
* [#p2 2 缓存不全]
* [#p3 3 缓存过分]
* [#p4 4 缓存目录过多]
* [#p5 5 删除缓存配置有误]
* [#p6 6 多余配置]

### 1 expires浏览器缓存不一致
nginx 的网站配置中


```
expires 10m;
```



该配置影响浏览器缓存，主要影响Cache-Control Expires 这两个字段

```
Cache-Control: max-age=600
Content-Encoding: gzip
Content-Type: text/html; charset=utf-8
Date: Fri, 22 Dec 2017 02:13:12 GMT
Expires: Fri, 22 Dec 2017 02:23:12 GMT
```

在网站中配置了浏览器优化，发现相应包中并不是所有的响应包的浏览器缓存时间都一致。

经排查发现

1 并不是所有的访问链接都是源站链接，这些链接不会经过节点，所以不受节点配置控制。

2 在节点配置中 Expires 只配置在一些静态页面、图片、cs、js响应中，其它类型的响应不受此控制。

### 2 缓存不全

在配置缓存的过程中发现有时一些js css 文件配置了缓存，但是并没有缓存下来，正常情况下应该缓存下来的。

经查，是由于pagespeed的开启了 js css最小化导致，可能跟pagespeed 的功能有关。


```
pagespeed on;
pagespeed EnableFilters rewrite_css;
pagespeed EnableFilters rewrite_javascript;
```

还有一些缓存没有缓存下来的原因是在location /  开启了不缓存，这会导致一些网页不缓存

```
   location / 
    {   
       # Disable Proxy
       proxy_cache off;
    }  
```
 
### 3 缓存过分

在缓存中经常发现有一些登录页面和源网站设置为 Cache-Control: no-store, no-cache 的网页被缓存下来，这些网页可能涉及一些动态交互的过程，不缓存这些动态交互的页面会好一些，可以避免一些缓存所带来的问题。

可以加入以下配置不缓存登录或带有认证的页面

```
proxy_cache_bypass $cookie_nocache $arg_nocache$arg_comment;
proxy_cache_bypass $http_pragma $http_authorization;
if ($request_uri ~ ^/(login|register|password\/reset)/) { set $cookie_nocache 1; }
```

或者在云防线配置的

```
proxy_ignore_headers Set-Cookie Cache-Control Expires;
```
把Cache-Control去掉，让源网站控制它们想要控制的非缓存页面

### 4 缓存目录过多

在详细了解缓存的过程中发现云防线有多个缓存的目录

```
proxy_cache_path /data/proxy_cache/www.gengjunfei.com levels=1:2 keys_zone=cache_www_gengjunfei_com:10m inactive=10m max_size=100m;
proxy_temp_path /data/proxy_temp/www.gengjunfei.com;

pagespeed FileCachePath /data/ngx_pagespeed_cache;
```
其中前两个一个是ngx_cache_purge  模块的缓存文件目录和缓存文件临时目录，proxy_temp_path 目录下文件好像现在并用到，建议删除该配置
可采用如下配置，use_temp_path=off  会把临时缓存跟缓存放到一个目录下，可以避免文件系统中不必要的数据拷贝。
```
proxy_cache_path /data/proxy_cache/www.gengjunfei.com levels=1:2 keys_zone=cache_www_gengjunfei_com:10m inactive=10m max_size=100m use_temp_path=off;
```

pagespeed FileCachePath   是pagespeed配置的缓存文件目录，只知道开启pagespeed的功能需要该配置，至于具体的作用还有待了解。

### 5 删除缓存配置有误
在每个网站配置中开启缓存功能后都有
   
```
 # Reverse Proxy Cache Purge Policy
    location ^~ /purge/
    {   
         allow 127.0.0.1;
         allow 172.16.2.17;
         deny all;
         proxy_cache_purge cache_www_testupload_com $host$1$is_args$args;
    }   

```
该配置存在的功能是提供缓存删除功能，但是该配置有误
需把 ^~ /purge/  改为  ~ /purge(/.*) 配置才正常
访问删除缓存的链接后出现如下说明删除正常，注意删除的是内存中的缓存，不是实际目录中的缓存

```

Successful purge

Key : www.testupload.com/dashboard/javascripts/all.js
Path: /data/proxy_cache/www.testupload.com/d/a2/b7363eaf7d9093bad3940144f0076a2d
----
BDWAF/1.0
```

### 6 多余配置
发现在每个网站的配置文件中存在以下配置

```
    location ~ /purge(/.*)
    {   
         allow 127.0.0.1;
         allow 172.16.2.17;
         deny all;
         proxy_cache_purge cache_www_testupload_com $host$1$is_args$args;
    }   
# JS/CSS Optimizing internal redirect
    location ^~ /cloudfenceinter301/
    {
        # rewrite 80 to 443(if use ssl)

        # Setting Max-Age Expiry Headers For Client-Side Caching
        expires 15d;

        # Reverse Proxy
        rewrite ^/cloudfenceinter301/(.+)$ /$1 break;
        proxy_pass http://pool_www_testupload_com;
    }

    location /RequestDenied
    {
        return 405;
    }
```

这些配置其实并没有用到，缓存删除的建议保留使用，其余的不用的配置确认后建议在3.0中删除。

### 问题1

如果加入网站原来设置的是缓存1小时，访问网站，让网站内容也缓存下来。然后修改成缓存1分钟，这时候缓存会在1分钟后过期吗？

测试环境：火狐浏览器

测试步骤：


```
1 缓存时间初始设置为1小时，访问网站，缓存文件生成。
2 修改缓存时间为1分钟，reload ，不访问网站（关闭浏览器），缓存文件不消失。然后在一分钟之内访问，缓存仍可命中，但是一分钟后缓存会消失。
3 再次访问网站一次，如果接下来一分钟内没有访问网站，缓存文件消失.直至再次访问才会产生。
```



结论： 缓存设置为一分钟后，如果不去访问的话，缓存在一分钟后不会过期，需要再次去访问，然后中间间隔一分钟不访问缓存就会过期。

