---
title: nginx 变量学习
date: 2017-01-02 10:00:00
categories: nginx
tags:
---

1、nginx改变编译选项，或增加模块

     niginx -V 可见版本信息，以及目前的编译信息

     重新configure make make install 会覆盖安装，但不会覆盖nginx.conf


2、设置用户变量

     set $a ‘hi’；

     （set会在进入{}时执行，类似js中预加载）


3、安装echo组件，在编译时，加上--add-module=/path…

     http://wiki.nginx.org/HttpEchoModule#Installation


4、服务器内部跳转location间set的变量是互相可见的，以一个请求为生命周期。


     location /a {

          set $a 'hi';

          rewrite ^ /b;     //内不跳转，不是301、302，浏览器端无察觉

     }

 

     location /b {

          echo $a;  //可见

     }

 
5、一些nginx预设变量

     http://localhost/soda?xx=xiaoxuan

 

     $uri     '/soda'     (经过解码，不含参数)

     $request_uri     '/soda?xx=xiaoxuan'     (原始请求，未解码，含参数)  

     $arg_xx     ‘xiaoxuan’     （对应参数key的值）

     $http_xx     (请求头中的变量群)

     $cookie_xx     （cookie变量群）

     $send_http_xx     （相应头中的变量群）

 

6、不要set nginx 自建变量的值，会出现崩溃或未知错误(少数变量除外，如args)


     对args的重新set值，会影响部分变量。

          -- 不会影响$uri, $request_url

          -- 会影响$arg_xx

 

     eg:

          location /soda{

               set $org_arg_a $arg_a;

               set $args 'a=1';

 

               echo 'org a : $org_arg_a';

               echo 'a : $arg_x';      

          }

     

      out : 

          curl 'http://localhost/soda/a=6'

          

          org a : 6

          a : 1

 

7、对$args的改写会影响proxy_pass



8、nginx对变量的读取，有两种：indexed or unindexed

     比如$args $ary_xx就是unindexed，即用的时候才去那块静态内存读取实时的值（可能已经被改写），类似的还有$cookie_xx


9、map 

     -- 仅在http段内使用

     -- 仅用到map的变量时才会映射（惰性求值），并且仅第一次用到时映射并缓存，后续对变量值的更改，不会影响之前映射的值

     

     eg：

     

     http{

          map $args $foo {

               default 0;

               soda 1;

          }

          server { 

               listen 80;

               location /soda {    

                    set $org_foo $foo;

                    set $args 'soda';

                    echo '$org_foo : $org_foo';

                    echo '$foo';

               }

          }

     }

 

     curl 'http://localhost/soda?soda'

     1 : 1

     1


     curl 'http://localhost/soda?xx'

     0 : 0

     0


     加载时，用到$foo变量（惰性，如果不用则不map），去map变量并缓存，然后set $args已经没用的

10、主动求值

     set $a '$b $b';

     这句则会在‘预加载’的过程就求值，而不是用到时才去惰性求值
