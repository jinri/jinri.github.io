---
title: nginx 104 Connection reset by peer 问题
date: 2017-09-24 10:00:10
tags: nginx
---
### nginx 报 "recv() failed (104: Connection reset by peer)"问题排查

现象：nginx在加入[nginx_upstream_check_module](https://github.com/yaoweibin/nginx_upstream_check_module)健康检查模块后error.log中经常出现recv() failed (104: Connection reset by peer)错误

```
2378:2017/09/12 14:57:40 [error] 34722#0: recv() failed (104: Connection reset by peer)
```
- 1 刚开始怀疑是加入的模块中报的这个错误，经查找源码，该模块中并无该错误日志片段。
经打开和关闭iptables，已排除是iptables的影响
经调整/etc/sysctl.conf 一些内核参数，已排除是本机内核参数的影响。
经调整/etc/php5/fpm/php-fpm.conf php的一些配置参数，已排除php参数设置的影响
经调整健康检查模块的发包频率，已排除发包频率的影响

该模块中有该错误产生：

```
[error] 25592#0: enable check peer: 47.90.36.208:443
```
 （错误含义：对该ip启动健康检查），属于该模块的正常日志报错，在满足某种条件下才会产生（服务器初始为down，在该模块检查超过成功检查配置次数后，标记该服务器为up），
类似的还有：

```
[error] 41689#0: disable check peer: 47.90.36.208:443   （服务器初始为up，一般在该模块检查超过失败检查配置次数后，标记该服务器为down）   
[error] 41689#0: check time out with peer: 14.215.9.85:443 （检查超时时产生）
```
- 2 .接着查找104的错误，猜想应该在nginx源码中有这类错误，经查找和调试，定位到该错误出现在：

```
Breakpoint 1, ngx_unix_recv (c=0x7fffd00874c0, buf=0x7fffffffd210 "\220\006", size=4096) at src/os/unix/ngx_recv.c:136
136         rev = c->read;
(gdb) p errno
$1 = 11
(gdb) watch errno
Hardware watchpoint 2: errno
(gdb) n
139             n = recv(c->fd, buf, size, 0);
(gdb) 
Hardware watchpoint 2: errno

Old value = 11
New value = 104

函数原型：ngx_unix_recv(ngx_connection_t *c, u_char *buf, size_t size)
```
该函数读取tcp链接对端发送过来的数据 这里n返回-1，根据该函数的解释： These calls return the number of bytes received, or -1 if an error occurred. 表示读数据时发生一个错误。

在nginx中，当err不为 NGX_EAGAIN ，NGX_EINTR 这两种状态则认为出错，并打印出错误码，该错误码为linux系统错误码。

```
if (err == NGX_EAGAIN || err == NGX_EINTR) {  //这两种情况 ,需要继续读
            
            ngx_log_debug0(NGX_LOG_DEBUG_EVENT, c->log, err,
                           "recv() not ready"); //recv() not ready (11: Resource temporarily unavailable)
            n = NGX_AGAIN; //返回这个表示内核数据已有的数据已经读取完，需要重新add epoll event来触发新数据epoll返回

        } else {//TCP连接出错了
            n = ngx_connection_error(c, err, "recv() failed");
            break;
        }
```
- 3 尽管报错地方已找到，但显然./os/unix/ngx_recv.c这个地方是供其它地方调用，什么情况下产生该错误及为什么产生该错误依然需要探究
在报错的时候查看调用栈信息：

```
0x00007ffff7bcb813 in recv () from /lib/x86_64-linux-gnu/libpthread.so.0
(gdb) bt
#0  0x00007ffff7bcb813 in recv () from /lib/x86_64-linux-gnu/libpthread.so.0
#1  0x0000000000445706 in ngx_unix_recv (c=0x7fffd00874c0, buf=0x7fffffffd210 "\220\006", size=4096) at src/os/unix/ngx_recv.c:139
#2  0x000000000051295d in ngx_http_upstream_check_discard_handler (event=0x7fffcf65e218)
    at /home/gjf/cloudfence/bdwaf/nginx_upstream_check_module/ngx_http_upstream_check_module.c:1233
#3  0x000000000044c3c8 in ngx_epoll_process_events (cycle=0x133da80, timer=2500, flags=1) at src/event/modules/ngx_epoll_module.c:822
#4  0x000000000043ed17 in ngx_process_events_and_timers (cycle=0x133da80) at src/event/ngx_event.c:248
#5  0x00000000004492ce in ngx_single_process_cycle (cycle=0x133da80) at src/os/unix/ngx_process_cycle.c:308
#6  0x0000000000418cfb in main (argc=1, argv=0x7fffffffe628) at src/core/nginx.c:416
```
发现的确有ngx_http_upstream_check模块对ngx_unix_recv的调用， 查看ngx_http_upstream_check_discard_handler 该函数在后台健康检查的作用: 该函数在链接关闭前不断从链接中读取数据，读取的数据不做任何处理，相当于丢弃。 而104错误就是在这不断读取中造成的。

```
Breakpoint 1, ngx_http_upstream_check_discard_handler (event=0x7fffcf65e218) at /home/gjf/cloudfence/bdwaf/nginx_upstream_check_module/ngx_http_upstream_check_module.c:1233
1233            size = c->recv(c, buf, 4096);
gdb) p errno
$1 = 11
(gdb) watch errno
Hardware watchpoint 2: errno
(gdb) n
Hardware watchpoint 2: errno

Old value = 11
New value = 104
0x00007ffff7bcb813 in recv () from /lib/x86_64-linux-gnu/libpthread.so.0
(gdb) l
1228        }
1229
1230        peer = c->data;
1231
1232        while (1) {
1233            size = c->recv(c, buf, 4096);
1234
1235            if (size > 0) {
1236                continue;
1237
```
源码：

```
ngx_http_upstream_check_discard_handler(ngx_event_t *event)
{
    u_char                          buf[4096];
    ssize_t                         size;
    ngx_connection_t               *c;
    ngx_http_upstream_check_peer_t *peer;

    c = event->data;

    ngx_log_debug0(NGX_LOG_DEBUG_HTTP, c->log, 0,
                   "upstream check discard handler");

    if (ngx_http_upstream_check_need_exit()) {
        return;
    }

    peer = c->data;

    while (1) {
        size = c->recv(c, buf, 4096);

        if (size > 0) {
            continue;

        } else if (size == NGX_AGAIN) {
            break;

        } else {
            if (size == 0) {
                ngx_log_debug0(NGX_LOG_DEBUG_HTTP, c->log, 0,
                               "peer closed its half side of the connection");
            }

            goto check_discard_fail;
        }
    }

    if (ngx_handle_read_event(c->read, 0) != NGX_OK) {
        goto check_discard_fail;
    }

    return;

 check_discard_fail:
    c->error = 1;
    ngx_http_upstream_check_clean_event(peer);
}
ngx_http_upstream_check_discard_handler函数是在清理一个健康检查主动链接的事件时被调用，在清理前会注册一些对该链接的读写清理的函数。
而为什么会清理一个健康检查主动链接的事件，看源码得知，健康检查模块中在一些数据收取完毕或数据发送完毕后或者链接处理完毕（或者出错）后会清理该链接的一些监听读写事件。

static void
ngx_http_upstream_check_clean_event(ngx_http_upstream_check_peer_t *peer)
{
    ngx_connection_t                    *c;
    ngx_http_upstream_check_srv_conf_t  *ucscf;
    ngx_check_conf_t                    *cf;

    c = peer->pc.connection;
    ucscf = peer->conf;
    cf = ucscf->check_type_conf;

    if (c) {
        ngx_log_debug2(NGX_LOG_DEBUG_HTTP, c->log, 0,
                       "http check clean event: index:%i, fd: %d",
                       peer->index, c->fd);
        if (c->error == 0 &&
            cf->need_keepalive &&
            (c->requests < ucscf->check_keepalive_requests))
        {
            c->write->handler = ngx_http_upstream_check_dummy_handler;
            c->read->handler = ngx_http_upstream_check_discard_handler;
        } else {
            ngx_close_connection(c);
            peer->pc.connection = NULL;
        }
    }
```
接着查看是否跟后台服务器有关，发现只有个别服务器会产生104错误。经测试，在删除该服务器所对应网站在nginx的代理配置后，104的错误不在产生

```

Breakpoint 1, ngx_http_upstream_check_discard_handler (event=0x7fffcf65e218) at /home/gjf/cloudfence/bdwaf/nginx_upstream_check_module/ngx_http_upstream_check_module.c:1233
1233            size = c->recv(c, buf, 4096);
(gdb) p *(peer.pc.name)
$1 = {len = 16, data = 0x1effe50 "218.17.254.67:80"}
(gdb) watch errno
Hardware watchpoint 2: errno
(gdb) n
Hardware watchpoint 2: errno

Old value = 11
New value = 104
0x00007ffff7bcb813 in recv () from /lib/x86_64-linux-gnu/libpthread.so.0
(gdb) l
1228        }
1229
1230        peer = c->data;
1231
1232        while (1) {
1233            size = c->recv(c, buf, 4096);
1234
1235            if (size > 0) {
1236                continue;
1237
```

```
2017/09/12 11:48:23 [error] 31222#0: enable check peer: 218.17.254.67:80
2017/09/12 11:48:35 [error] 31222#0: recv() failed (104: Connection reset by peer)
```
由此猜想可能与后台服务器处理该链接健康检查模块的链接过程有关， 经查阅相关资料有关这样的描述：

errno = 104错误表明你在对一个对端socket已经关闭的的连接调用write或send方法，在这种情况下，调用write或send方法后， 对端socket便会向本端socket发送一个RESET信号，在此之后如果继续执行write或send操作，就会得到errno为104，错误描述为connection reset by peer。 

5 接着采用tcpdump对该服务进行抓包：

```
sudo tcpdump   -i  eth0  -s  0  -w  test.pcap   host 218.17.254.67
```
经多次抓包观察发现，发现该服务器经常会向109发送reset报文。 
[reset.png](https://github.com/jinri/jinri.github.io/blob/master/res/reset.png)

reset报文发送场景（可能还有更多）：

```
1 当尝试和未开放的服务器端口建立tcp连接时，服务器tcp将会直接向客户端发送reset报文
2 双方之前已经正常建立了通信通道，也可能进行过了交互，当某一方在交互的过程中发生了异常，如崩溃等，异常的一方会向对端发送reset报文，通知对方将连接关闭
3 当收到TCP报文，但是发现该报文不是已建立的TCP连接列表可处理的，则其直接向对端发送reset报文
4 ack报文丢失，并且超出一定的重传次数或时间后，会主动向对端发送reset报文释放该TCP连接
```
结论：

```
1 由此可基本确定为产生104该错误的原因为，对该模块发出的tcp方式的健康检查包，对端服务器的处理（关闭了该链接）。
2 查看该类服务器的健康状态：正常，网站也可正常访问。该错误应该不会影响bdwaf正常功能。
3 多数服务器不会产生该错误，如果改源码想屏蔽掉该错误，可能会影响其它正常功能。
4 发http方式或者https方式的健康检查包也会有相应错误产生，且http无法检测https的服务器，https服务器无法检查http的服务器 而tcp的可以同时做到。
```
参考链接：
- http://blog.csdn.net/alibo2008/article/details/45694845 
- http://blog.csdn.net/candyguy242/article/details/25699727 
- http://lovestblog.cn/blog/2014/05/20/tcp-broken-pipe/