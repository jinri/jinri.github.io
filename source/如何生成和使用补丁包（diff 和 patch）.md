---
title: 如何生成和使用补丁包（diff 和 patch）
date: 2016-09-27 10:00:10
categories: debug
tags: 
---
### 如何生成和使用补丁包（diff 和 patch）

在开发的过程中，源码好配置文件都必须经常改动，如果每修改一个文件，然后都需要通过覆盖旧文件的方式提交，就会变得很麻烦，因此可以通过打补丁包方便我们的提交过程。对于php，python， 源代码，配置文件可通过此方式，二进制文件则无能为力。

使用git仓库
1. 在git仓库生成补丁包
  
```
git diff > a.patch
```

2. 尝试把补丁包打到别的git仓库 
```
patch --dry-run -p1 < a.patch
```
 （--dry-run只显示过程，不会真正改动文件）
3. 第二步没报错，则真正打补丁  
```
patch  -p1 < a.patch
```

使用普通的目录（a目录为原目录，b目录为改动后的新目录）
1. 通过比对两个目录生成补丁包                 
```
diff -Nur a b > a.patch
```

2. 尝试把补丁包打到别的目录（要进入该目录）   
```
patch --dry-run -p1 < a.patch
```
 （如果diff时不小心写成了diff -Nur b a， 则要使用参数p2）
3. 第二步没报错，则真正打补丁                 
```
patch  -p1 < a.patch
```
（如果diff时不小心写成了diff -Nur b a， 则要使用参数p2）