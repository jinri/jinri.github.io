---
title: F5 与 Ctrl+F5 区别
date: 2018-01-01 10:00:00
categories: nginx
tags:
---

　　在浏览器里中，按F5键或者点击Toobar上的Refresh/Reload图标(简称F5)，和做F5同时按住Ctrl键（简称Ctrl+F5），效果是明显不一样的，通常Ctrl+F5明显要让网页Refresh慢一些，到底两者有什么区别呢？

Expires、Last-Modified/If-Modified-Since和ETag/If-None-Match这些HTTP Headers，F5/Ctrl+F5和这些有莫大关系。

假如我第一次访问过==http://www.example.com==，这个网页是个动态网页，每次访问都会去访问Server，但是它包含一个一个静态资源==http://www.example.com/logo.gif==，浏览器在显示这个网页之前需要发HTTP请求获取这个logo.gif文件，返回的HTTP response包含这样的Headers:


```
Expires: Thu 27 Nov 2008 07:00:00 GMT 
Last-Modified: Fri 30 Nov 2007 00:00:00 GMT
```


那么浏览器就会cache住这个logo.gif文件，直到2008年11月27日7点整，或者直到用户有意清空cache。

下次我再通过bookmark或者通过在URI输入栏直接敲字的方法访问==http://www.example.com==的时候，浏览器一看本地有个logo.gif，而且它还没过期呢，就不会发HTTP request给server，而是直接把本地cache中的logo.gif显示了。

**F5的作用和直接在URI输入栏中输入然后回车是不一样的**，F5会让浏览器无论如何都发一个HTTP Request给Server，即使先前的Response中有Expires Header。所以，当我在当前==http://www.example.com==网页中按F5的时候，浏览器会发送一个HTTP Request给Server，但是包含这样的Headers:

```
If-Modified-Since: Fri 30 Nov 2007 00:00:00 GMT
```

实际上Server没有修改这个logo.gif文件，所以返回一个304 (Not Modified)，这样的Response很小，所以round-trip耗时不多，网页很快就刷新了。

--- 

上面的例子中没有考虑ETag，如同在上一篇技术文章中所说，最好就不要用ETag，但是如果Response中包含ETag，F5引发的Http Request中也是会包含If-None-Match的。

那么Ctrl+F5呢？ **Ctrl+F5要的是彻底的从Server拿一份新的资源过来**，所以不光要发送HTTP request给Server，而且这个请求里面连If-Modified-Since/If-None-Match都没有，这样就逼着Server不能返回304，而是把整个资源原原本本地返回一份，这样，Ctrl+F5引发的传输时间变长了，自然网页Refresh的也慢一些。

实际上，为了保证拿到的是从Server上最新的，Ctrl+F5不只是去掉了If-Modified-Since/If-None-Match，还需要添加一些HTTP Headers。按照HTTP/1.1协议，Cache不光只是存在Browser终端，从Browser到Server之间的中间节点(比如Proxy)也可能扮演Cache的作用，为了防止获得的只是这些中间节点的Cache，需要告诉他们，别用自己的Cache敷衍我，往Upstream的节点要一个最新的copy吧。

在IE6中，Ctrl+F5会添加一个Header


```
Pragma: no-cache
```


在Firefox 2.0中，Ctrl+F5会添加两个


```
Pragma: no-cache 
Cache-Control: max-age=0
```


作用就是让中间的Cache对这个请求失效，这样返回的绝对是新鲜的资源。

引用[巴别塔上的雇工](https://mocheng.wordpress.com/2007/11/30/browser-f5-vs-ctrlf5/)
