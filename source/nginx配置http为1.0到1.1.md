---
title: nginx配置http为1.0到1.1
date: 2017-10-28 22:00:10
tags: 
---

nginx配置http为1.0到1.1，主要是为了长连接有效。

对于HTTP代理，proxy_http_version指令应该设置为“1.1”，同时“Connection”头的值也应被清空。
```
upstream http_backend {
    server 127.0.0.1:8080;

    keepalive 16;
}

server {
    ...

    location /http/ {
        proxy_pass http://http_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        ...
    }
}
```
引用 http://nginx.org/cn/docs/http/ngx_http_upstream_module.html#keepalive