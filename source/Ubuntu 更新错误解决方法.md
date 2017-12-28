---
title: Ubuntu 更新错误解决方法
date: 2017-11-23 22:00:10
tags: 
---
- 在Ubuntu和其它基于Ubuntu的Linux发行版中，更新错误是一个共性的错误，也经常发生。这些错误出现的原因多种多样，修复起来也很简单。在本文中，我们将见到Ubuntu中各种类型频繁发生的更新错误以及它们的修复方法。
 
1. 合并列表问题。
    当你在终端中运行更新命令时，你可能会碰到这个错误“合并列表错误”，就像下面这样：

```
E:Encountered a section with no Package: header,
E:Problem with MergeList /var/lib/apt/lists/archive.ubuntu.comubuntudistspreciseuniversebinary-i386Packages,
E:The package lists or status file could not be parsed or opened.’
```

可以使用以下命令来修复该错误：
  
```
1. sudo rm -r /var/lib/apt/lists/*
2. sudo apt-get clean && sudo apt-get update
```

 
2. 下载仓库信息失败 -1.
实际上，有两种类型的下载仓库信息失败错误。如果你的错误是这样的：

```
W:Failed to fetch bzip2:/var/lib/apt/lists/partial/in.archive.ubuntu.comubuntudistsoneiricrestrictedbinary-i386Packages Hash Sum mismatch,
W:Failed to fetch bzip2:/var/lib/apt/lists/partial/in.archive.ubuntu.comubuntudistsoneiricmultiversebinary-i386Packages Hash Sum mismatch,
E:Some index files failed to download. They have been ignored, or old ones used instead
```

那么，你可以用以下命令修复：
 
```
1. sudo rm -rf /var/lib/apt/lists/*
2. sudo apt-get update
```

3. 部分更新错误.
在终端中运行更新会出现部分更新错误：

```
Not all updates can be installed
Run a partial upgrade, to install as many updates as possible
```

在终端中运行以下命令来修复该错误：
  
```
1. sudo apt-get install -f
```

4. 加载共享库时发生错误.
该错误更多是安装错误，而不是更新错误。如果尝试从源码安装程序，你可能会碰到这个错误：

```
error while loading shared libraries:
cannot open shared object file: No such file or directory
```

该错误可以通过在终端中运行以下命令来修复：
 
```
1. sudo /sbin/ldconfig -v
```

你可以在这里查找到更多详细内容加载共享库时发生错误。
 
5. 无法获取锁 /var/cache/apt/archives/lock.
在另一个程序在使用APT时，会发生该错误。假定你正在Ubuntu软件中心安装某个东西，然后你又试着在终端中运行apt。

```
E: Could not get lock /var/cache/apt/archives/lock – open (11: Resource temporarily unavailable)
E: Unable to lock directory /var/cache/apt/archives/
```

通常，只要你把所有其它使用apt的程序关了，这个问题就会好的。但是，如果问题持续，可以使用以下命令：
 
```
1. sudo rm /var/lib/apt/lists/lock
```

如果上面的命令不起作用，可以试试这个命令：
 
```
1. sudo killall apt-get
```

关于该错误的更多信息，可以在这里找到。
 
6. GPG错误： 下列签名无法验证.
在添加一个PPA时，可能会导致以下错误GPG错误： 下列签名无法验证，这通常发生在终端中运行更新时：

```
W: GPG error: http://repo.mate-desktop.org saucy InRelease: The following signatures couldn’t be verified because the public key is not available: NO_PUBKEY 68980A0EA10B4DE8
```

我们所要做的，就是获取系统中的这个公钥，从信息中获取密钥号。在上述信息中，密钥号为68980A0EA10B4DE8。该密钥可通过以下方式使用：
 
```
1. sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 68980A0EA10B4DE8
```

在添加密钥后，再次运行更新就没有问题了。
 
7. BADSIG错误
另外一个与签名相关的Ubuntu更新错误是BADSIG错误，它看起来像这样：

```
W: A error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error: http://extras.ubuntu.com precise Release: The following signatures were invalid: BADSIG 16126D3A3E5C1192 Ubuntu Extras Archive Automatic Signing Key
W: GPG error: http://ppa.launchpad.net precise Release:
The following signatures were invalid: BADSIG 4C1CBC1B69B0E2F4 Launchpad PPA for Jonathan French W: Failed to fetch http://extras.ubuntu.com/ubuntu/dists/precise/Release
```

要修复该BADSIG错误，请在终端中使用以下命令：
 
```
1. sudo apt-get clean
  2. cd /var/lib/apt
  3. sudo mv lists oldlist
  4. sudo mkdir -p lists/partial
  5. sudo apt-get clean
  6. sudo apt-get update
```
invalid: KEYEXPIRED 错误

```
W: GPG error: http://repo.mysql.com precise Release: The following signatures were invalid: KEYEXPIRED 1487236823 KEYEXPIRED 1487236823 KEYEXPIRED 1487236823
```
解决方法

```
sudo apt-key list | grep "expired: "
sudo apt-key adv --keyserver keys.gnupg.net --recv-keys [KEY]

sudo apt-key list  | grep "expired: " | sed -ne 's|pub .*/\([^ ]*\) .*|\1|gp' | xargs -n1 sudo apt-key adv --keyserver keys.gnupg.net --recv-keys

sudo apt-get update
```

Can't locate Debconf/Db.pm 12.04
No file name for libpam0g
```
sudo apt-get upgrade
sudo dpkg -i /var/cache/apt/archives/*.deb
sudo dpkg --configure -a
sudo apt-get upgrade

sudo rm -f /etc/apt/sources.list.d/*
sudo dpkg --configure -a
```



本文汇集了可能会碰到的Ubuntu更新错误,希望这会对你处理这些错误有所帮助。