---
title: Nginx+Modsecurity 403带规则跳转实现
date: 2017-07-24 10:00:10
categories: nginx
tags: 
---

## Nginx+Modsecurity 403带规则跳转实现 

Nginx+Modsecurity403跳转实现基于modsecurity重定向，而实现这个重定向必须解决之前出现的modsecurity bug [****post500****](https://github.com/SpiderLabs/ModSecurity/issues/582 )
- [modsecurity源码更改](https://github.com/jinri/jinri.github.io/blob/master/res/post500.diff)

为实现跳转，须在modsecurity配置文件中加入如下规则：
- 1、阶段1，阶段2的默认动作修改为pass才可以带规则跳转

```
SecDefaultAction phase:1,log,auditlog,pass
SecDefaultAction phase:2,log,auditlog,pass
```
- 2、定义变量hit_block_count，hit_all_ruleid并初始化。这两个变量的作用域为一次请求。

```
SecAction "id:'300101',phase:1,t:none,setvar:tx.hit_block_count=0,nolog,pass"
SecAction "id:'300102',phase:1,t:none,setvar:tx.hit_all_ruleid=,nolog,pass"
```
- 3、为实现规则ip的统计和命中次数的统计，需要在每条规则后加入

```
",setvar:tx.hit_block_count=+1,setvar:tx.hit_all_ruleid=%{tx.hit_all_ruleid}+%{rule.id}"
```
需要加入上述设置的规则较多，故采用脚本实现。
[modsec_rules_change.sh](https://github.com/jinri/jinri.github.io/blob/master/res/modsec_rules_change.sh)

本次加入上述配置的modsecurity核心配置文件为：

```
modsecurity_crs_20_protocol_violations.conf
modsecurity_crs_21_protocol_anomalies.conf  
modsecurity_crs_23_request_limits.conf 
modsecurity_crs_35_bad_robots.conf  
modsecurity_crs_40_generic_attacks.conf  
modsecurity_crs_41_sql_injection_attacks.conf  
modsecurity_crs_41_xss_attacks.conf  
modsecurity_crs_42_tight_security.conf  
modsecurity_crs_45_trojans.conf
```
以后有需想加入该设置的配置文件，把该脚本放在相同目录，配置conf_list.config，再运行modsec_rules_change.sh脚本即可。

- 4、在阶段2阻断

```
SecRule  TX:hit_block_count "@ge 1" "id:'300103',nolog, pass, phase:2, t:none, setvar:'tx.redirect_url_args=rule_id&%{tx.hit_block_count}%{tx.hit_all_ruleid}&ip&%{tx.real_ip}&time&%{TIME_EPOCH}&host&%{request_headers.host}',msg:'hit rule time hit_block_count=%{tx.hit_block_count},hit all rule id =%{tx.hit_all_ruleid}'"
SecRule  TX:redirect_url_args "!@streq 0" "nolog,deny,phase:2,id:'300104',t:none,t:base64Encode,msg:'hit rule time hit_block_count=%{tx.hit_block_count},hit all rule id =%{tx.hit_all_ruleid}',redirect:http://172.16.2.107?act=intercept&url=%{REQUEST_URI}&args=%{MATCHED_VAR}"
```
在阶段4阻断

```
SecRule  TX:hit_block_count "@ge 1" "id:'300105',nolog, pass, phase:4, t:none, setvar:'tx.redirect_url_args=rule_id&%{tx.hit_block_count}%{tx.hit_all_ruleid}&ip&%{tx.real_ip}&time&%{TIME_EPOCH}&host&%{request_headers.host}',msg:'hit rule time hit_block_count=%{tx.hit_block_count},hit all rule id =%{tx.hit_all_ruleid}'"
SecRule  TX:redirect_url_args "!@streq 0" "nolog,deny,phase:4,id:'300106',t:none,t:base64Encode,msg:'hit rule time hit_block_count=%{tx.hit_block_count},hit all rule id =%{tx.hit_all_ruleid}',redirect:http://172.16.2.107?act=intercept&url=%{REQUEST_URI}&args=%{MATCHED_VAR}"

```
- 5、重定向链接需要根据实际环境做相应修改，跳转链接参数部分做了base64编码。

- 6、测试： 节点代理一个网站 www.gengjunfei.com
浏览器中采用如下方式访问：

```
www.gengjunfei.com/?id=%27 or %271%27=%271
```

这时跳转至链接：

```
http://192.168.60.128/?act=intercept&url=/?id=%27%20or%20%271%27=%271&args=cnVsZV9pZCY1Kzk1MDkwMSs5NTkwNzErOTgxMjQ0Kzk4MTI0Mis5ODEyNDMmaXAmMTcyLjE2LjIuMTcmdGltZSYxNDk2NjQ1NzIxJmhvc3Qmd3d3LmdlbmdqdW5mZWkuY29t
```
对args=后面的参数base64解码得：

```
rule_id&5+950901+959071+981244+981242+981243&ip&172.16.2.17&time&1496645721&host&www.gengjunfei.com
```
查看nginx error日志 ，正好中了5条规则。

[nginx_403.error](https://github.com/jinri/jinri.github.io/blob/master/res/403_err.png)
