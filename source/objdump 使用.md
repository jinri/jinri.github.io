---
title: objdump 使用
date: 2016-11-26 21:00:05
categories: debug
tags: 
---
#### objdump -h SimpleSection.o 
查看段表信息（objdump有省略）
#### objdump -x -d  SimpleSection.o 
-x Display the contents of all headers

-d Display assembler contents of executable sections

-s Display the full contents of all sections requested

#### objdump -s -d  SimpleSection.o 

readelf 用来查看ELF文件
#### readelf -h  SimpleSection.o 
readelf -S 查看真正的段表结构
#### readelf -S  SimpleSection.o 