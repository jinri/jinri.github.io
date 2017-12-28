---
title: docker 介绍
date: 2017-11-01 22:00:10
categories: docker
tags: 
---
### docker 是什么？
Docker 最初是 dotCloud 公司创始人 Solomon Hykes 在法国期间发起的一个公司内部项目，它是基于 dotCloud 公司多年云服务技术的一次革新，并于 2013 年 3 月以 Apache 2.0 授权协议开源，主要项目代码在 GitHub 上进行维护。Docker 项目后来还加入了 Linux 基金会，并成立推动 开放容器联盟（OCI）。

Docker 自开源后受到广泛的关注和讨论，至今其 GitHub 项目已经超过 4 万 6 千个星标和一万多个 fork。甚至由于 Docker 项目的火爆，在 2013 年底，dotCloud 公司决定改名为 Docker。Docker 最初是在 Ubuntu 12.04 上开发实现的；Red Hat 则从 RHEL 6.5 开始对 Docker 进行支持；Google 也在其 PaaS 产品中广泛应用 Docker。

Docker 使用 Google 公司推出的 Go 语言 进行开发实现，基于 Linux 内核的 cgroup，namespace，以及 AUFS 类的 Union FS 等技术，对进程进行封装隔离，属于 操作系统层面的虚拟化技术。由于隔离的进程独立于宿主和其它的隔离的进程，因此也称其为容器。最初实现是基于 LXC，从 0.7 版本以后开始去除 LXC，转而使用自行开发的 libcontainer，从 1.11 开始，则进一步演进为使用 runC 和 containerd。

Docker 在容器的基础上，进行了进一步的封装，从文件系统、网络互联到进程隔离等等，极大的简化了容器的创建和维护。使得 Docker 技术比虚拟机技术更为轻便、快捷。

下面的图片比较了 Docker 和传统虚拟化方式的不同之处。传统虚拟机技术是虚拟出一套硬件后，在其上运行一个完整操作系统，在该系统上再运行所需应用进程；而容器内的应用进程直接运行于宿主的内核，容器内没有自己的内核，而且也没有进行硬件虚拟。因此容器要比传统虚拟机更为轻便。

[传统虚拟化](https://yeasy.gitbooks.io/docker_practice/content/introduction/_images/virtualization.png)

[Docker](https://yeasy.gitbooks.io/docker_practice/content/introduction/_images/docker.png)

作为一种新兴的虚拟化方式，Docker 跟传统的虚拟化方式相比具有众多的优势。

- 更高效的利用系统资源
- 更快速的启动时间
- 一致的运行环境
- 持续交付和部署
- 更轻松的迁移
- 更轻松的维护和扩展


### dokcer 基本概念
Docker 包括三个基本概念
##### 镜像（Image）
##### 容器（Container）
##### 仓库（Repository）
理解了这三个概念，就理解了 Docker 的整个生命周期

Docker 镜像是一个特殊的文件系统，除了提供容器运行时所需的程序、库、资
源、配置等文件外，还包含了一些为运行时准备的一些配置参数（如匿名卷、环境
变量、用户等）。镜像不包含任何动态数据，其内容在构建之后也不会被改变。

操作系统分为内核和用户空间。对于 Linux 而言，内核启动后，会挂
载 root 文件系统为其提供用户空间支持。而 Docker 镜像（Image），就相当于
是一个  root  文件系统。

因为镜像包含操作系统完整的  root  文件系统，其体积往往是庞大的，因此在
Docker 设计时，就充分利用 Union FS 的技术，将其设计为分层存储的架构。

镜像（Image）和容器（Container）的关系，就像是面向对象程序设计中
的 类  和 实例  一样，镜像是静态的定义，容器是镜像运行时的实体。容器可以被
创建、启动、停止、删除、暂停等。
容器的实质是进程，但与直接在宿主执行的进程不同，容器进程运行于属于自己的
独立的 命名空间。因此容器可以拥有自己的  root  文件系统、自己的网络配置、
自己的进程空间，甚至自己的用户 ID 空间。容器内的进程是运行在一个隔离的环
境里，使用起来，就好像是在一个独立于宿主的系统下操作一样。这种特性使得容
器封装的应用比直接在宿主运行更加安全。也因为这种隔离的特性，很多人初学
Docker 时常常会把容器和虚拟机搞混。

前面讲过镜像使用的是分层存储，容器也是如此。每一个容器运行时，是以镜像为
基础层，在其上创建一个当前容器的存储层，我们可以称这个为容器运行时读写而
准备的存储层为容器存储层。

镜像构建完成后，可以很容易的在当前宿主上运行，但是，如果需要在其它服务器
上使用这个镜像，我们就需要一个集中的存储、分发镜像的服务，Docker Registry
就是这样的服务。
一个 Docker Registry 中可以包含多个仓库（Repository）；每个仓库可以包含多
个标签（Tag）；每个标签对应一个镜像。
通常，一个仓库会包含同一个软件不同版本的镜像，而标签就常用于对应该软件的
各个版本。我们可以通过  <仓库名>:<标签>  的格式来指定具体是这个软件哪个版
本的镜像。如果不给出标签，将以  latest  作为默认标签。

以 Ubuntu 镜像 为例，ubuntu是仓库的名字，其内包含有不同的版本标签，如， 14.04  ,  16.04  。我们可以通过 ubuntu:14.04 ，或者 ubuntu:16.04
来具体指定所需哪个版本的镜像。如果忽略了标签，比如 ubuntu ，那将视为ubuntu:latest 。

### docker深入理解

Docker做的事情就是将的软件隔离起来，让它们即使出了问题也不会互相影响。这并不是什么横空出世的新思想。
你很可能会说内核控制的进程不就这样玩么？每一个进程都有自己的内存空间，并且在一个进程自身看来，内存
空间与所处在的计算机的内存空间是一样的。然而内核欺骗了进程，在背后将内存地址重新映射到了真实的内存
空间中。想想今天高速运转处理器，任何地方见到的系统都能同时运行多个进程。今天的文明社会比人类历史任
何一个时间点制造的谎言数量级都要很多的量级。

Docker将进程的隔离模型的进行了扩展，让隔离性变得更强。Docker是在Linux内核的基础上打造的一系列工具。
整个文件系统被抽象了，网络被虚拟化了，其它进程被隐藏了，并且从理论上，不可能逃脱容器去对在一个机器
上的其他进程搞破坏。实际中，每个人对于怎么才能逃脱容器，至少去收集一点运行容器的机器的相关信息，持
开放的态度。跟虚拟机比较起来，容器的隔离性还是较弱。
但换个角度看，进程比容器性能更好，容器性能比虚拟机性能更佳。原因很简单，隔离性更高，在每一个上下文
中就需要运行更多的东西，从而拖慢速度。选择一个隔离性的过程，实际就是决定你对要运行进程的信任有多少
的过程 - 它会不会去干扰其他的进程？如运行的进程都是自己的亲儿子，那你对他们会有一个很高的信任度，对
他们用最少的隔离，运行在一个进程中就行了。如果是SAP，那么你很可能需要尽可能高的隔离性：将电脑装在封
存在箱子里，绑在火箭上发射到月球。

Docker另一个很好的特性是，容器可以作为一个整体交付。他们不会像虚拟机那么臃肿。这大大的提高了部署的简易度。

Docker 底层的核心技术包括 Linux 上的命名空间（Namespaces）、控制组
（Control groups）、Union 文件系统（Union file systems）和容器格式
（Container format）

镜像是一种层叠的只读文件系统。容器中程序的执行仍然是使用本机操作系统的，容器并不自己构建操作系统，而是以某种隔离的方式依赖本机操作系统工作。这就是Docker和虚拟机的本质区别。

### 简单总结
什么是容器

依托于linux内核的虚拟化技术

什么是Docker

能够把应用程序自动部署到容器的开源引擎

Docker的目标

创建软件程序可移植的轻量容器，让其可以在任何安装了Docker的机器上运行，而不用关心底层操作系统，类似于船舶使用的集装箱．

对 Docker 应用最广泛的三个领域分别是：Test/QA 应用；Web 应用；大数据，企业应用。

命名空间（Namespace）：Docker 有五个命名空间：进程、网络、挂
载、宿主和共享内存，为了隔离有问题的应用，Docker 运用 Namespace 将进
程隔离，为进程或进程组创建已隔离的运行空间，为进程提供不同的命名空间视
图。这样，每一个隔离出来的进程组，对外就表现为一个 container(容器)。需
要注意的是，Docker 让用户误以为自己占据了全部资源，但这并不是"虚拟机"
内核 namesapce 从内核 2.6.15 之后被引入。

Docker 让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，
然后发布到任何流行的 Linux 机器上，便可以实现虚拟化

### ubuntu Docker 安装


```
Ubuntu 14.04 LTS部署 (不同版本见部署方式略有差别)

#uname -a //检查内核版本
#apt-get install -y --install-recommends linux-generic-lts-xenial  //升级内核版本
#apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual // 安装内核驱动(AUFS) 可选
#update-grub //更新 GRUB
#reboot
#apt-get install apt-transport-https ca-certificates //添加使用 HTTPS 传输的软件包以及 CA 证书
#apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D  //为了确认所下载软件包的合法性，需要添加 Docker 官方软件源的 GPG 密钥
#echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main"| sudo tee /etc/apt/sources.list.d/docker.list               // 添加最新源 推荐使用官方推荐的软件源
#apt-get update
#apt-get install docker-engine
#service docker start
```

### docker源码编译

```
git clone https://github.com/docker/docker.git
cd docker
make docs //编译文档，本地8080端口可查看
```



#安装好配置镜像加速器（阿里云）

```
 vi /etc/default/docker
 DOCKER_OPTS="--registry-mirror=https://wsc9k2xq.mirror.aliyuncs.com"
```
### docker常用命令

#查看仓库中镜像
```
docker search ubuntu
docker search -s 10 ubuntu
```


#从官方仓库中下载image

```
docker pull centos
docker pull ubuntu
```

 
#查看本地可用的image

```
docker images
docker images --digests
```
 
#启动一个ubuntu的dokcer容器，直接进入bash

```
docker  run  -it  ubuntu  bash
```

#后台启动一个ubuntu的dokcer容器

```
docke  run  -d  -it  ubuntu
```
 
#后台启动一个ubuntu的dokcer容器，监听80端口，映射到容器里的8080端口


```
docke run -p 80:8080  -d  -it  ubuntu

```
docker run  参数
--name  标记可以为容器自定义命名。
--rm  标记，则容器在终止后会立刻删
除。注意， --rm  和  -d  参数不能同时使用。
 
#查看正在运行的docker容器

```
docker ps
```
 
#查看所有docker容器

```
docker ps -a
```
#获取所有容器ID

```
docker ps -a -q
```

#然后停掉所有的容器

```
docker kill $(docker ps -a -q)
```

#在运行状态的容器里启动一个bash（进入正在运行的容器）

```
docker  exec  -it  $container_id  bash
```
 
#启动/关闭/重启容器

```
docker  start/stop/restart  $container_id
```

#Docker 容器镜像删除，停止所有的container，这样才能够删除其中的images

```
docker stop $(docker ps -a -q)
```

#删除容器

```
docker  rm  $container_id
```

#如果想要删除所有container的话再加一个指令

```
docker rm $(docker ps -a -q)
```
#删除images，通过image的id来指定删除谁

```
docker rmi <image id>
```

#想要删除untagged images，也就是那些id为<None>的image的话可以用
 
```
docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
```
#要删除全部image的话


```
docker rmi $(docker images -q)
```
#查看悬挂镜像

```
docker images -f dangling=true
```

#查看容器运行前后不同

```
docker diff webserver
```
#容器与主机之间复制文件
```
docker cp foo.txt mycontainer:/foo.txt
docker cp mycontainer:/foo.txt foo.txt
```
#在主机里使用以下命令可以查看指定容器的信息

```
docker inspect container
```

#获取容器的log信息
```
sudo docker logs [container ID or NAMES]
```



#创建自定义镜像，打包应用

```
mkdir test_image
cd  test_image
```

#创建Dockerfile

```
vi  Dockerfile
```

#自定义image
#继承一个已有的镜像，这里用nginx1.8.1作为基础

```
FROM nginx:1.8.1
COPY jinri.github.io/ /usr/share/nginx/html/
```
#打包镜像，镜像名为web，版本为1.0

```
docker build -t web:v1 .
```
#启动镜像，并启动web，把本机的8080端口映射到容器的80端口

```
docker run --name web -d -p 8080:80 web:v1
```

#push到docker hub，先登录，打标签，push

```
#docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username (jinri): jinri
Password: 
Login Succeeded

#docker tag myweb:v1  jinri/web:v1
#docker push jinri/web:v1
```
#导出镜像，导入镜像（直接通过文件来分发镜像到其他机器）

```
docker save -o myweb1.0.image myweb:v1

docker load -i myweb1.0.image
```

*Run anywhere
Docker：Build once，Run anywhere*

---


- Docker  码头工人 集装箱
- docker不是容器，是管理容器的开源的引擎。- Docker为应用打包、部署的平台，而非单纯的虚拟化技术。
- paas 平台及服务
- caas 容器及服务



附录：客户端命令
可以通过  man docker-COMMAND  或  docker help COMMAND  来查看这些命令的具体用法。

```
attach：依附到一个正在运行的容器中；
build：从一个 Dockerfile 创建一个镜像；
commit：从一个容器的修改中创建一个新的镜像；
cp：在容器和本地宿主系统之间复制文件中；
create：创建一个新容器，但并不运行它；
diff：检查一个容器内文件系统的修改，包括修改和增加；
events：从服务端获取实时的事件；
exec：在运行的容器内执行命令；
export：导出容器内容为一个 tar 包；
history：显示一个镜像的历史信息；
images：列出存在的镜像；
import：导入一个文件（典型为 tar 包）路径或目录来创建一个本地镜像；
info：显示一些相关的系统信息；
inspect：显示一个容器的具体配置信息；
kill：关闭一个运行中的容器 (包括进程和所有相关资源)；
load：从一个 tar 包中加载一个镜像；
login：注册或登录到一个 Docker 的仓库服务器；
logout：从 Docker 的仓库服务器登出；
logs：获取容器的 log 信息；
network：管理 Docker 的网络，包括查看、创建、删除、挂载、卸载等；
node：管理 swarm 集群中的节点，包括查看、更新、删除、提升/取消管理节点等；
pause：暂停一个容器中的所有进程；
port：查找一个 nat 到一个私有网口的公共口；
ps：列出主机上的容器；
pull：从一个Docker的仓库服务器下拉一个镜像或仓库；
push：将一个镜像或者仓库推送到一个 Docker 的注册服务器；
rename：重命名一个容器；
restart：重启一个运行中的容器；
rm：删除给定的若干个容器；
rmi：删除给定的若干个镜像；
run：创建一个新容器，并在其中运行给定命令；
save：保存一个镜像为 tar 包文件；
search：在 Docker index 中搜索一个镜像；
service：管理 Docker 所启动的应用服务，包括创建、更新、删除等；
start：启动一个容器；
stats：输出（一个或多个）容器的资源使用统计信息；
stop：终止一个运行中的容器；
swarm：管理 Docker swarm 集群，包括创建、加入、退出、更新等；
tag：为一个镜像打标签；
top：查看一个容器中的正在运行的进程信息；
unpause：将一个容器内所有的进程从暂停状态中恢复；
update：更新指定的若干容器的配置信息；
version：输出 Docker 的版本信息；
volume：管理 Docker volume，包括查看、创建、删除等；
wait：阻塞直到一个容器终止，然后输出它的退出符。
```


https://hub.docker.com/

https://dockerfile.github.io/

https://docs.docker-cn.com/get-started/

https://yeasy.gitbooks.io/docker_practice/content/basic_concept/

https://github.com/widuu/chinese_docker/blob/master/SUMMARY.md

https://docs-cn.docker.octowhale.com/get_started/001.Orientation.html

https://github.com/DeanXu/Docker-introduce/blob/master/README.md

https://www.zhihu.com/question/28300645

https://blog.lab99.org/post/docker-2016-07-14-faq.html

http://www.csdn.net/article/2014-07-02/2820497-what's-docker 
 
https://docs.docker-cn.com/get-started/

https://linux.cn/article-8192-1.html

http://www.jianshu.com/p/420c66d4d361
